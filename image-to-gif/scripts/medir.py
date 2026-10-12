"""
medir.py - Ferramenta de medição de pixels para a skill image-to-gif.

Por que existe: antes de animar qualquer elemento, é preciso saber ONDE ele
está com precisão de pixel. Estimar coordenadas "no olho" gera tracejados
desalinhados. Esta ferramenta mede e devolve números em JSON.

Subcomandos (todos imprimem JSON):
    info     IMG                              -> tamanho, modo e cor de fundo
    linha    IMG Y [--ate Y2] [--x0 --x1]     -> sequências de pixels escuros em linhas
    coluna   IMG X [--ate X2] [--y0 --y1]     -> o mesmo, em colunas
    cor      IMG X0 Y0 X1 Y1                  -> cor mais escura de uma região (a "tinta")
    recorte  IMG X0 Y0 X1 Y1 --saida A.png    -> recorte ampliado para conferência visual
    texto    IMG X0 Y0 X1 Y1 [--limiar 150]   -> linhas de texto da região (caixa, altura, cor)

Exemplo:
    python medir.py linha diagrama.png 290 --x0 100 --x1 400
"""

import argparse
import json
import sys
from collections import Counter

import numpy as np
from PIL import Image


class ImagemFonte:
    """Carrega a imagem e a entrega sempre em RGB.

    Alta coesão: esta classe só sabe abrir e normalizar a imagem. Quem mede
    ou recorta recebe a imagem pronta e não precisa conhecer formatos.
    """

    def __init__(self, caminho: str):
        self.caminho = caminho
        self.original = Image.open(caminho)
        self.rgb = self._normalizar(self.original)
        self.largura, self.altura = self.rgb.size

    @staticmethod
    def pixels_de(imagem: Image.Image) -> list:
        """Lista de pixels, compatível com Pillow antigo e novo (getdata foi descontinuado)."""
        ler = getattr(imagem, "get_flattened_data", None) or imagem.getdata
        return list(ler())

    @classmethod
    def cor_predominante(cls, imagem: Image.Image) -> tuple:
        """Cor mais frequente da imagem; em diagramas, quase sempre é o fundo."""
        amostra = imagem.convert("RGB").resize((200, 200), Image.NEAREST)
        return Counter(cls.pixels_de(amostra)).most_common(1)[0][0]

    @classmethod
    def _normalizar(cls, imagem: Image.Image) -> Image.Image:
        """Converte para RGB sem escurecer áreas transparentes.

        convert("RGB") simplesmente descarta o canal alfa: o que era
        transparente pode virar preto. Por isso, quando há alfa, a imagem é
        composta antes sobre a cor de fundo predominante.
        """
        tem_alfa = imagem.mode in ("RGBA", "LA") or (
            imagem.mode == "P" and "transparency" in imagem.info
        )
        if not tem_alfa:
            return imagem.convert("RGB")
        rgba = imagem.convert("RGBA")
        fundo = Image.new("RGBA", rgba.size, cls.cor_predominante(rgba) + (255,))
        return Image.alpha_composite(fundo, rgba).convert("RGB")

    def pixel(self, x: int, y: int) -> tuple:
        """Cor RGB de um pixel. Quem usa não precisa saber como a imagem é guardada."""
        return self.rgb.getpixel((x, y))

    def recortar(self, caixa: tuple) -> Image.Image:
        """Recorte RGB de uma caixa (x0, y0, x1, y1)."""
        return self.rgb.crop(caixa)

    def info(self) -> dict:
        return {
            "arquivo": self.caminho,
            "largura": self.largura,
            "altura": self.altura,
            "modo_original": self.original.mode,
            "cor_fundo": list(self.cor_predominante(self.rgb)),
        }


class MedidorDeRuns:
    """Encontra sequências contínuas (runs) de pixels escuros.

    Um "run" é um trecho de pixels vizinhos que passam no critério de
    escuridão. Num tracejado horizontal, cada traço vira um run; a distância
    entre o início de dois runs seguidos é o período (traço + espaço).
    """

    def __init__(self, imagem: ImagemFonte, limiar: int = 350):
        self.imagem = imagem
        # Pixel "escuro" = soma R+G+B abaixo do limiar (0 a 765).
        self.limiar = limiar

    def _escuro(self, x: int, y: int) -> bool:
        return sum(self.imagem.pixel(x, y)) < self.limiar

    @staticmethod
    def agrupar(indices) -> list:
        """Transforma [3,4,5,9,10] em [(3,5),(9,10)]."""
        runs, inicio, anterior = [], None, None
        for i in indices:
            if inicio is None:
                inicio = anterior = i
            elif i == anterior + 1:
                anterior = i
            else:
                runs.append((inicio, anterior))
                inicio = anterior = i
        if inicio is not None:
            runs.append((inicio, anterior))
        return runs

    def na_linha(self, y: int, x0: int, x1: int) -> list:
        return self.agrupar([x for x in range(x0, x1) if self._escuro(x, y)])

    def na_coluna(self, x: int, y0: int, y1: int) -> list:
        return self.agrupar([y for y in range(y0, y1) if self._escuro(x, y)])

    @staticmethod
    def resumo(runs: list) -> dict:
        """Estatísticas úteis para um tracejado: traço e período medianos."""
        if len(runs) < 2:
            return {}
        tracos = sorted(b - a + 1 for a, b in runs)
        periodos = sorted(runs[i + 1][0] - runs[i][0] for i in range(len(runs) - 1))
        return {
            "traco_mediano": tracos[len(tracos) // 2],
            "periodo_mediano": periodos[len(periodos) // 2],
        }


class AmostradorDeCor:
    """Descobre a cor real do traço (a "tinta") numa região."""

    def __init__(self, imagem: ImagemFonte):
        self.imagem = imagem

    def mais_escura(self, caixa: tuple) -> dict:
        pixels = ImagemFonte.pixels_de(self.imagem.recortar(caixa))
        escura = min(pixels, key=sum)
        # A cor escura mais comum é mais robusta que o pixel extremo isolado.
        escuras = [p for p in pixels if sum(p) <= sum(escura) + 60]
        return {
            "mais_escura": list(escura),
            "escura_mais_comum": list(Counter(escuras).most_common(1)[0][0]),
        }


class GeradorDeRecortes:
    """Gera recortes ampliados sem suavização, para conferir formas pixel a pixel."""

    def __init__(self, imagem: ImagemFonte):
        self.imagem = imagem

    def salvar(self, caixa: tuple, zoom: int, saida: str) -> dict:
        recorte = self.imagem.recortar(caixa)
        # NEAREST preserva cada pixel como um bloco nítido (sem borrar).
        ampliado = recorte.resize((recorte.width * zoom, recorte.height * zoom), Image.NEAREST)
        ampliado.save(saida)
        return {"saida": saida, "caixa": list(caixa), "zoom": zoom}


class DetectorDeLinhasDeTexto:
    """Encontra as linhas de texto de uma região (usado na tradução).

    Pixel de "tinta" = cor bem diferente do fundo da região. Linhas de pixels
    com tinta, separadas por faixas vazias, viram linhas de texto. Para cada
    linha devolve a caixa, a altura e a cor típica da tinta.
    """

    def __init__(self, imagem: ImagemFonte, limiar: int = 150):
        self.imagem = imagem
        # Soma das diferenças |R-Rf| + |G-Gf| + |B-Bf| acima disso = tinta.
        self.limiar = limiar

    def detectar(self, caixa: tuple) -> dict:
        recorte = self.imagem.recortar(caixa)
        fundo = np.array(ImagemFonte.cor_predominante(recorte))
        arr = np.array(recorte).astype(int)
        tinta = np.abs(arr - fundo).sum(2) > self.limiar
        linhas = []
        for y0, y1 in MedidorDeRuns.agrupar(np.nonzero(tinta.any(1))[0].tolist()):
            xs = np.nonzero(tinta[y0:y1 + 1].any(0))[0]
            cores = arr[y0:y1 + 1][tinta[y0:y1 + 1]]
            # A cor mediana dos 30% de pixels mais distantes do fundo é a tinta "cheia".
            distancia = np.abs(cores - fundo).sum(1)
            cheia = cores[distancia >= np.percentile(distancia, 70)]
            linhas.append({
                "caixa": [int(xs.min()) + caixa[0], y0 + caixa[1], int(xs.max()) + caixa[0] + 1, y1 + caixa[1] + 1],
                "altura": y1 - y0 + 1,
                "cor": [int(c) for c in np.median(cheia, 0)],
            })
        return {"fundo": [int(c) for c in fundo], "linhas": linhas}


class CliMedir:
    """Interface de linha de comando: só traduz argumentos em chamadas."""

    def __init__(self):
        self.parser = self._montar_parser()

    @staticmethod
    def _montar_parser() -> argparse.ArgumentParser:
        p = argparse.ArgumentParser(description="Medição de pixels para a skill image-to-gif")
        sub = p.add_subparsers(dest="comando", required=True)

        s = sub.add_parser("info"); s.add_argument("imagem")

        for nome, eixo in (("linha", "y"), ("coluna", "x")):
            s = sub.add_parser(nome)
            s.add_argument("imagem"); s.add_argument("pos", type=int)
            s.add_argument("--ate", type=int, help="última linha/coluna (varre um intervalo)")
            s.add_argument("--inicio", type=int, default=0, help="início do trecho no outro eixo")
            s.add_argument("--fim", type=int, help="fim do trecho no outro eixo")
            s.add_argument("--limiar", type=int, default=350)

        for nome in ("cor", "recorte", "texto"):
            s = sub.add_parser(nome)
            s.add_argument("imagem")
            for c in ("x0", "y0", "x1", "y1"):
                s.add_argument(c, type=int)
            if nome == "recorte":
                s.add_argument("--zoom", type=int, default=4)
                s.add_argument("--saida", required=True)
            if nome == "texto":
                s.add_argument("--limiar", type=int, default=150)
        return p

    def executar(self, argv=None) -> dict:
        a = self.parser.parse_args(argv)
        img = ImagemFonte(a.imagem)
        if a.comando == "info":
            return img.info()
        if a.comando in ("linha", "coluna"):
            return self._varrer(img, a)
        caixa = (a.x0, a.y0, a.x1, a.y1)
        if a.comando == "cor":
            return AmostradorDeCor(img).mais_escura(caixa)
        if a.comando == "texto":
            return DetectorDeLinhasDeTexto(img, a.limiar).detectar(caixa)
        return GeradorDeRecortes(img).salvar(caixa, a.zoom, a.saida)

    @staticmethod
    def _varrer(img: ImagemFonte, a) -> dict:
        medidor = MedidorDeRuns(img, a.limiar)
        horizontal = a.comando == "linha"
        limite = img.largura if horizontal else img.altura
        fim = a.fim if a.fim is not None else limite
        resultado = {}
        for pos in range(a.pos, (a.ate if a.ate is not None else a.pos) + 1):
            runs = medidor.na_linha(pos, a.inicio, fim) if horizontal else medidor.na_coluna(pos, a.inicio, fim)
            resultado[str(pos)] = {"runs": runs, **MedidorDeRuns.resumo(runs)}
        return resultado


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(CliMedir().executar(), ensure_ascii=False))
