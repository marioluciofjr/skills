"""
traduzir.py - Etapa OPCIONAL da skill image-to-gif: traduz os textos da imagem.

Só é usada quando a pessoa pede a tradução. Roda ANTES da animação: gera uma
nova imagem (PNG, sem perdas) com os textos trocados, e essa imagem vira a
"entrada" do gerar_gif.py.

Como funciona:
    1. Apaga cada bloco de texto original com inpainting (o OpenCV pinta o
       buraco copiando o fundo ao redor, inclusive fundos coloridos).
    2. Escreve o texto traduzido com a fonte escolhida, na mesma posição,
       cor e alinhamento. Se não couber, reduz o tamanho e avisa no relatório.

Uso:
    python traduzir.py especificacao_traducao.json [--previa PASTA]
    python traduzir.py calibrar FONTE "texto original de uma linha" LARGURA_PX

"calibrar" devolve o tamanho de fonte que reproduz a largura de uma linha
original: é assim que o texto novo fica com o mesmo "corpo" do antigo.

Formato do JSON (exemplo completo em assets/exemplo_traducao.json):
    {
      "entrada": "original.jpg", "saida": "traduzida.png",
      "fonte": "Excalifont.ttf",
      "padrao": {"cor": [20, 22, 21], "tamanho": 23, "alinhamento": "centro"},
      "blocos": [
        {"nome": "descrição 1", "caixa": [650, 96, 892, 202],
         "linhas": ["Limite máximo de", "tokens que o", "modelo gera."]},
        {"nome": "texto com destaque", "caixa": [460, 830, 570, 948],
         "linhas": ["Cães adoram", [["e", [52, 150, 122]], [" latir", null]]]},
        {"nome": "rótulo girado", "caixa": [410, 322, 424, 362], "rotacao": 90,
         "linhas": ["Maçã"], "tamanho": 11}
      ]
    }

Campos de um bloco (os de "padrao" valem para todos, e o bloco pode sobrescrever):
    caixa         área do texto original, que será apagada
    area          área onde escrever o novo texto (padrão: a própria caixa)
    linhas        lista de linhas; cada linha é um texto ou uma lista de
                  segmentos [texto, cor] (cor null = cor do bloco)
    cor, tamanho, alinhamento ("centro", "esquerda", "direita"),
    entrelinha (múltiplo do tamanho, padrão 1.15), rotacao (0 ou 90),
    negrito (true engrossa o traço), limiar_limpeza (padrão 110),
    apagar (false = não apaga nada; útil para só escrever),
    caixas_apagar (lista de caixas usada no lugar de "caixa" para apagar;
                   serve para contornar algo vizinho, como a ponta de uma seta)
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from medir import ImagemFonte  # noqa: E402


class CarregadorDeFonte:
    """Abre a fonte uma vez por tamanho e mede textos.

    Se a fonte pedida não existir, tenta fontes manuscritas comuns do
    sistema. O relatório informa qual fonte foi usada de fato.
    """

    ALTERNATIVAS = [
        "C:/Windows/Fonts/Inkfree.ttf", "C:/Windows/Fonts/segoepr.ttf", "C:/Windows/Fonts/comic.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/System/Library/Fonts/Supplemental/Chalkboard.ttc",
    ]

    def __init__(self, caminho: str = None):
        candidatos = ([caminho] if caminho else []) + self.ALTERNATIVAS
        self.caminho = next((c for c in candidatos if c and Path(c).exists()), None)
        self._cache = {}

    def fonte(self, tamanho: int) -> ImageFont.FreeTypeFont:
        if tamanho not in self._cache:
            self._cache[tamanho] = (ImageFont.truetype(self.caminho, tamanho) if self.caminho
                                    else ImageFont.load_default(tamanho))
        return self._cache[tamanho]

    def largura(self, texto: str, tamanho: int) -> float:
        return self.fonte(tamanho).getlength(texto)


@dataclass
class BlocoDeTexto:
    """Um bloco de texto a traduzir. Só guarda dados; não sabe desenhar."""

    nome: str
    caixa: tuple
    linhas: list                  # lista de linhas; cada linha = lista de (texto, cor)
    cor: tuple = (20, 22, 21)
    tamanho: int = 20
    alinhamento: str = "centro"
    entrelinha: float = 1.15
    rotacao: int = 0
    negrito: bool = False
    limiar_limpeza: int = 110
    apagar: bool = True
    area: tuple = None
    caixas_apagar: list = None    # várias caixas, para contornar algo que não pode ser apagado
    relatorio: dict = field(default_factory=dict)

    def __post_init__(self):
        self.area = tuple(self.area) if self.area else tuple(self.caixa)
        self.caixas_apagar = [tuple(c) for c in self.caixas_apagar] if self.caixas_apagar else [tuple(self.caixa)]

    @classmethod
    def de_dict(cls, dados: dict, padrao: dict) -> "BlocoDeTexto":
        campos = {**padrao, **dados}
        cor = tuple(campos.get("cor", cls.cor))
        linhas = []
        for linha in campos["linhas"]:
            segmentos = [[linha, None]] if isinstance(linha, str) else linha
            linhas.append([(texto, tuple(c) if c else cor) for texto, c in segmentos])
        campos.update(cor=cor, linhas=linhas, caixa=tuple(campos["caixa"]))
        conhecidos = set(cls.__dataclass_fields__) - {"relatorio"}
        return cls(**{k: v for k, v in campos.items() if k in conhecidos})

    @staticmethod
    def texto_da_linha(linha: list) -> str:
        return "".join(t for t, _ in linha)


class ApagadorDeTexto:
    """Apaga os textos originais de todos os blocos com um único inpainting.

    Em cada caixa, o fundo é a cor mais comum; "tinta" é tudo que se afasta
    dele além do limiar. A máscara é dilatada 2 px para levar junto o halo
    que a compressão JPEG deixa em volta das letras.
    """

    def __init__(self, raio_inpaint: int = 3, dilatacao: int = 2):
        self.raio = raio_inpaint
        self.dilatacao = dilatacao

    def mascara(self, arr: np.ndarray, blocos: list) -> np.ndarray:
        total = np.zeros(arr.shape[:2], np.uint8)
        for b in blocos:
            if b.apagar:
                for caixa in b.caixas_apagar:
                    self._marcar(arr, total, caixa, b.limiar_limpeza)
        return total

    def _marcar(self, arr: np.ndarray, total: np.ndarray, caixa: tuple, limiar: int) -> None:
        """Marca na máscara a tinta de uma caixa. A dilatação não sai da caixa."""
        x0, y0, x1, y1 = (int(round(v)) for v in caixa)
        regiao = arr[y0:y1, x0:x1].astype(int)
        fundo = np.array(ImagemFonte.cor_predominante(Image.fromarray(arr[y0:y1, x0:x1])))
        tinta = (np.abs(regiao - fundo).sum(2) > limiar).astype(np.uint8) * 255
        nucleo = np.ones((2 * self.dilatacao + 1,) * 2, np.uint8)
        total[y0:y1, x0:x1] |= cv2.dilate(tinta, nucleo)

    def apagar(self, imagem: Image.Image, blocos: list) -> tuple:
        arr = np.array(imagem)
        mascara = self.mascara(arr, blocos)
        limpa = cv2.inpaint(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), mascara, self.raio, cv2.INPAINT_TELEA)
        return Image.fromarray(cv2.cvtColor(limpa, cv2.COLOR_BGR2RGB)), mascara


class DiagramadorDeTexto:
    """Escreve um bloco traduzido dentro da sua área.

    Diagramar = decidir tamanho, quebra e posição. Se a linha mais longa não
    couber na largura (ou o bloco na altura), o tamanho cai 1 px por vez até
    caber, com piso de 60% do tamanho pedido.
    """

    PISO = 0.6

    def __init__(self, fontes: CarregadorDeFonte):
        self.fontes = fontes

    def _cabe(self, b: BlocoDeTexto, tamanho: int, largura: float, altura: float) -> bool:
        maior = max(self.fontes.largura(b.texto_da_linha(l), tamanho) for l in b.linhas)
        return maior <= largura and len(b.linhas) * tamanho * b.entrelinha <= altura * 1.08

    def _tamanho_que_cabe(self, b: BlocoDeTexto, largura: float, altura: float) -> int:
        tamanho = b.tamanho
        while tamanho > max(6, int(b.tamanho * self.PISO)) and not self._cabe(b, tamanho, largura, altura):
            tamanho -= 1
        return tamanho

    def _desenhar_linhas(self, desenho, b, tamanho, moldura):
        """moldura = (x, y, largura, altura) do espaço onde o bloco é centralizado."""
        x_origem, y_origem, largura, altura = moldura
        fonte = self.fontes.fonte(tamanho)
        passo = tamanho * b.entrelinha
        topo = y_origem + (altura - passo * len(b.linhas)) / 2 + passo / 2
        traco = max(1, round(tamanho / 22)) if b.negrito else 0
        for i, linha in enumerate(b.linhas):
            w = self.fontes.largura(b.texto_da_linha(linha), tamanho)
            x = {"esquerda": x_origem, "direita": x_origem + largura - w}.get(
                b.alinhamento, x_origem + (largura - w) / 2)
            for texto, cor in linha:
                desenho.text((x, topo + i * passo), texto, font=fonte, fill=cor, anchor="lm",
                             stroke_width=traco, stroke_fill=cor)
                x += self.fontes.largura(texto, tamanho)

    def desenhar(self, imagem: Image.Image, b: BlocoDeTexto) -> Image.Image:
        x0, y0, x1, y1 = b.area
        largura, altura = x1 - x0, y1 - y0
        if b.rotacao in (90, 270):
            largura, altura = altura, largura  # diagrama "deitado" e gira depois
        tamanho = self._tamanho_que_cabe(b, largura, altura)
        b.relatorio = {"bloco": b.nome, "tamanho_pedido": b.tamanho, "tamanho_usado": tamanho,
                       "cabe": self._cabe(b, tamanho, largura, altura)}
        camada = Image.new("RGBA", (int(np.ceil(largura)), int(np.ceil(altura))), (0, 0, 0, 0))
        self._desenhar_linhas(ImageDraw.Draw(camada), b, tamanho, (0, 0, largura, altura))
        if b.rotacao:
            camada = camada.rotate(b.rotacao, expand=True, resample=Image.BICUBIC)
        base = imagem.convert("RGBA")
        base.alpha_composite(camada, (int(round(x0)), int(round(y0))))
        return base.convert("RGB")


class EspecificacaoTraducao:
    """Lê o JSON da tradução. Único lugar que conhece o formato do arquivo."""

    def __init__(self, arquivo: str):
        pasta = Path(arquivo).resolve().parent
        dados = json.loads(Path(arquivo).read_text(encoding="utf-8"))
        self.entrada = str(pasta / dados["entrada"])
        self.saida = str(pasta / dados.get("saida", "traduzida.png"))
        fonte = dados.get("fonte")
        self.fonte = str(pasta / fonte) if fonte and not Path(fonte).is_absolute() else fonte
        padrao = dados.get("padrao", {})
        self.blocos = [BlocoDeTexto.de_dict({"nome": f"bloco {i + 1}", **b}, padrao)
                       for i, b in enumerate(dados["blocos"])]


class PipelineTraducao:
    """Apaga tudo de uma vez, depois escreve bloco a bloco, e relata."""

    def __init__(self, especificacao: EspecificacaoTraducao):
        self.esp = especificacao

    def executar(self, pasta_previa: str = None) -> dict:
        fontes = CarregadorDeFonte(self.esp.fonte)
        limpa, mascara = ApagadorDeTexto().apagar(ImagemFonte(self.esp.entrada).rgb, self.esp.blocos)
        diagramador = DiagramadorDeTexto(fontes)
        resultado = limpa
        for bloco in self.esp.blocos:
            resultado = diagramador.desenhar(resultado, bloco)
        resultado.save(self.esp.saida)
        if pasta_previa:
            Path(pasta_previa).mkdir(parents=True, exist_ok=True)
            limpa.save(Path(pasta_previa) / "sem_texto.png")
            Image.fromarray(mascara).save(Path(pasta_previa) / "mascara_texto.png")
        relatorios = [b.relatorio for b in self.esp.blocos]
        return {
            "arquivo": self.esp.saida,
            "fonte_usada": fontes.caminho or "fonte padrão do Pillow",
            "blocos": len(relatorios),
            "reduzidos": [r for r in relatorios if r["tamanho_usado"] < r["tamanho_pedido"]],
            "nao_couberam": [r["bloco"] for r in relatorios if not r["cabe"]],
        }


class CalibradorDeTamanho:
    """Acha o tamanho de fonte cuja largura do texto mais se aproxima da original."""

    def __init__(self, fontes: CarregadorDeFonte):
        self.fontes = fontes

    def calibrar(self, texto: str, largura: float) -> dict:
        tamanho = min(range(6, 120), key=lambda t: abs(self.fontes.largura(texto, t) - largura))
        return {"fonte": self.fontes.caminho, "texto": texto, "largura_original": largura,
                "tamanho": tamanho, "largura_obtida": round(self.fontes.largura(texto, tamanho), 1)}


class CliTraduzir:
    """Interface de linha de comando: só traduz argumentos em chamadas."""

    @staticmethod
    def executar(argv=None) -> dict:
        argv = sys.argv[1:] if argv is None else argv
        if argv and argv[0] == "calibrar":
            p = argparse.ArgumentParser(prog="traduzir.py calibrar")
            p.add_argument("fonte"); p.add_argument("texto"); p.add_argument("largura", type=float)
            a = p.parse_args(argv[1:])
            return CalibradorDeTamanho(CarregadorDeFonte(a.fonte)).calibrar(a.texto, a.largura)
        p = argparse.ArgumentParser(description="Traduz os textos de uma imagem (etapa opcional)")
        p.add_argument("especificacao"); p.add_argument("--previa")
        a = p.parse_args(argv)
        return PipelineTraducao(EspecificacaoTraducao(a.especificacao)).executar(a.previa)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(CliTraduzir.executar(), ensure_ascii=False, indent=2))
