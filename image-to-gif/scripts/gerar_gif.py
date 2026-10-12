"""
gerar_gif.py - Gera o GIF animado da skill image-to-gif a partir de uma especificação JSON.

Ideia central: o que muda de uma imagem para outra são DADOS (coordenadas,
cores, tempos). O resto (limpar o original, desenhar os quadros, montar e
verificar o GIF) é sempre igual e fica aqui, testado. Quem usa a skill só
mede a imagem e escreve o JSON.

Uso:
    python gerar_gif.py especificacao.json [--previa PASTA]

--previa salva limpa.png (imagem sem os elementos animados) e quadro0.png,
para conferência em recortes ampliados com medir.py.

Tipos de animação (todos opcionais, combináveis no mesmo JSON):

    "caminhos"         tracejado andando ("formigas") no sentido do caminho
    "setas_piscantes"  a seta some e é redesenhada da cauda para a ponta
    "cards"            brilho suave acende e apaga na borda de um card

Formato (exemplos completos em assets/):
    {
      "entrada": "diagrama.png", "saida": "saida.gif",    relativos ao JSON
      "quadros": 12, "ms_por_quadro": 60,
      "etapas": 7,                     opcional: divide o loop em 7 janelas iguais
      "tracejado": {"traco": 8, "periodo": 18, "espessura": 2.6,
                    "cor": [72, 77, 80], "limiar_limpeza": 728},
      "caminhos": [
        {"nome": "seta com curva",
         "pontos": [[968.6, 710], [968.6, 726],
                    {"controle": [968.6, 745.6], "ate": [947, 745.6]}, [749, 745.6]],
         "tracejado": {"cor": [37, 31, 26]}}
      ],
      "setas_piscantes": [
        {"nome": "seta 1", "pontos": [[363, 517], [407, 517]], "largura": 12,
         "limiar_limpeza": 700, "etapa": 0}
      ],
      "cards": [
        {"nome": "card 1", "caixa": [7.5, 67.5, 970.5, 229.5], "raio": 24,
         "cor": [46, 184, 140], "etapa": 0}
      ]
    }

Tempo: cada seta ou card age só dentro da sua janela, dada por
"janela": [inicio, fim] (frações do loop, de 0 a 1) ou por "etapa": i quando
há "etapas": N (janela = [i/N, (i+1)/N]). Sem janela, age o loop inteiro.

Caminhos (tracejados e setas) seguem o sentido do fluxo. No tracejado, o
caminho termina ANTES da ponta da seta; na seta piscante, vai até a ponta.
Um item {"controle", "ate"} é uma curva Bézier quadrática do ponto anterior
até "ate".
"""

import argparse
import json
import math
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, replace
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

# Reaproveita o carregador de imagem de medir.py (mesma pasta), sem duplicar código.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from medir import ImagemFonte  # noqa: E402


# ---------------------------------------------------------------------------
# Modelos de dados
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class EstiloTracejado:
    """Aparência de um tracejado. Imutável: ajustes geram um novo objeto."""

    traco: float = 8.0            # comprimento de cada traço, em px
    periodo: float = 18.0         # traço + espaço, em px
    espessura: float = 2.6        # largura da linha, em px
    cor: tuple = (72, 77, 80)     # cor real amostrada do traço original
    limiar_limpeza: int = 728     # soma RGB abaixo disso = pixel do traço a apagar

    def combinar(self, ajustes: dict) -> "EstiloTracejado":
        """Devolve uma cópia com os campos de `ajustes` sobrescritos."""
        campos = dict(ajustes)
        if "cor" in campos:
            campos["cor"] = tuple(campos["cor"])
        return replace(self, **campos)


class Caminho:
    """Polilinha percorrida por comprimento de arco.

    "Comprimento de arco" é a distância andada ao longo do caminho. Com ele,
    o tracejado tem traços do mesmo tamanho nas retas e nas curvas, e a seta
    piscante é revelada no ritmo certo mesmo quando faz curva.
    """

    PONTOS_POR_CURVA = 12

    def __init__(self, nome: str, itens: list):
        self.nome = nome
        self.pontos = self._expandir(itens)
        self._segmentos, self.comprimento = self._medir_segmentos(self.pontos)

    @classmethod
    def _expandir(cls, itens: list) -> list:
        """Converte a lista do JSON em pontos, amostrando as curvas."""
        pontos = []
        for item in itens:
            if isinstance(item, dict):
                pontos += cls._bezier(pontos[-1], tuple(item["controle"]), tuple(item["ate"]),
                                      item.get("n", cls.PONTOS_POR_CURVA))
            else:
                pontos.append(tuple(item))
        return pontos

    @staticmethod
    def _bezier(p0, p1, p2, n):
        """Bézier quadrática: curva suave de p0 a p2 "puxada" pelo controle p1."""
        return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
                 (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])
                for t in [i / n for i in range(1, n + 1)]]

    @staticmethod
    def _medir_segmentos(pontos):
        segmentos, total = [], 0.0
        for a, b in zip(pontos, pontos[1:]):
            L = math.dist(a, b)
            segmentos.append((a, b, total, L))
            total += L
        return segmentos, total

    def ponto_em(self, s: float) -> tuple:
        """Ponto que fica a `s` px do início, andando sobre o caminho."""
        for a, b, s0, L in self._segmentos:
            if s <= s0 + L or (a, b, s0, L) == self._segmentos[-1]:
                t = 0 if L == 0 else (s - s0) / L
                return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        return self.pontos[0]

    def trecho(self, inicio: float, fim: float, passo: float = 0.5) -> list:
        """Pontos densos entre duas distâncias; vira um traço desenhado."""
        pts, s = [], inicio
        while s < fim:
            pts.append(self.ponto_em(s))
            s += passo
        return pts + [self.ponto_em(fim)]

    def projetar(self, xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
        """Para cada pixel, a distância (sobre o caminho) do ponto mais próximo."""
        melhor_d = np.full(xs.shape, np.inf)
        melhor_s = np.zeros(xs.shape)
        for (ax, ay), (bx, by), s0, L in self._segmentos:
            if L == 0:
                continue
            t = np.clip(((xs - ax) * (bx - ax) + (ys - ay) * (by - ay)) / (L * L), 0, 1)
            d = np.hypot(xs - (ax + t * (bx - ax)), ys - (ay + t * (by - ay)))
            perto = d < melhor_d
            melhor_d[perto], melhor_s[perto] = d[perto], s0 + t[perto] * L
        return melhor_s


@dataclass(frozen=True)
class JanelaDeTempo:
    """Trecho do loop em que uma animação age, em frações de 0 a 1."""

    inicio: float = 0.0
    fim: float = 1.0

    def _limites(self, total: int) -> tuple:
        return round(self.inicio * total), round(self.fim * total)

    def contem(self, quadro: int, total: int) -> bool:
        f0, f1 = self._limites(total)
        return f0 <= quadro < f1

    def progresso(self, quadro: int, total: int, centrado: bool = False) -> float:
        """0 no primeiro quadro da janela até perto de 1 no último.

        centrado=True mede pelo meio de cada quadro: útil para curvas como
        seno, que assim nunca caem exatamente em zero dentro da janela.
        """
        f0, f1 = self._limites(total)
        return (quadro - f0 + (0.5 if centrado else 0.0)) / max(1, f1 - f0)


class Mascaras:
    """Utilitários de máscara compartilhados pelas animações."""

    @staticmethod
    def faixa(tamanho: tuple, pontos: list, largura: float) -> np.ndarray:
        """Máscara booleana de uma faixa de `largura` px sobre a polilinha."""
        imagem = Image.new("L", tamanho, 0)
        ImageDraw.Draw(imagem).line(pontos, fill=255, width=int(largura), joint="curve")
        return np.array(imagem) > 0


# ---------------------------------------------------------------------------
# Animações (cada uma sabe se aplicar a um quadro)
# ---------------------------------------------------------------------------

class Animacao(ABC):
    """Contrato de qualquer animação.

    Para criar um efeito novo, basta uma subclasse que implemente estes
    métodos; renderizador, montador e verificador não mudam (baixo acoplamento).
    """

    nome = "animação"
    cria_cores_novas = False   # True se pinta cores que não existem no original

    @abstractmethod
    def aplicar(self, imagem: Image.Image, quadro: int, total: int) -> Image.Image:
        """Devolve o quadro com esta animação aplicada por cima de `imagem`."""

    @abstractmethod
    def area(self, tamanho: tuple) -> np.ndarray:
        """Máscara booleana dos pixels que esta animação pode alterar."""

    def regioes_limpeza(self, tamanho: tuple) -> list:
        """Pares (máscara, limiar) a apagar da imagem antes de animar."""
        return []


class TracejadoAndando:
    """Um caminho tracejado "formigas andando" (peça de CamadaDeTracejados).

    No quadro f, os traços se deslocam período x f / N. Depois de N quadros
    o deslocamento é exatamente um período: o desenho volta ao início e o
    loop fica sem salto.
    """

    def __init__(self, caminho: Caminho, estilo: EstiloTracejado):
        self.caminho = caminho
        self.estilo = estilo

    def desenhar(self, desenho, quadro, total, escala):
        e, c = self.estilo, self.caminho
        deslocamento = e.periodo * quadro / total
        k = -1  # começa um período antes para cobrir o traço que entra pela borda
        while (s0 := deslocamento + k * e.periodo) <= c.comprimento:
            a, b = max(0.0, s0), min(c.comprimento, s0 + e.traco)
            if b - a > 0.3:  # ignora pedaços minúsculos nas pontas
                desenho.line([(x * escala, y * escala) for x, y in c.trecho(a, b)],
                             fill=255, width=int(e.espessura * escala), joint="curve")
            k += 1


class CamadaDeTracejados(Animacao):
    """Todos os tracejados de uma mesma cor, desenhados numa única camada.

    Supersampling: desenha numa tela N vezes maior e reduz com LANCZOS. A
    redução gera bordas suaves (anti-aliasing), iguais às do traço original.
    Uma camada por cor evita escurecer onde dois caminhos se sobrepõem
    (como no tronco comum de uma ramificação).
    """

    def __init__(self, cor: tuple, itens: list, supersampling: int, largura_faixa: int):
        self.cor = cor
        self.itens = itens
        self.ss = supersampling
        self.largura_faixa = largura_faixa
        self.nome = ", ".join(i.caminho.nome for i in itens)

    def aplicar(self, imagem, quadro, total):
        W, H = imagem.size
        camada = Image.new("L", (W * self.ss, H * self.ss), 0)
        desenho = ImageDraw.Draw(camada)
        for item in self.itens:
            item.desenhar(desenho, quadro, total, self.ss)
        alfa = camada.resize((W, H), Image.LANCZOS)
        return Image.composite(Image.new("RGB", (W, H), self.cor), imagem, alfa)

    def _faixa(self, tamanho, item):
        return Mascaras.faixa(tamanho, item.caminho.pontos, self.largura_faixa)

    def area(self, tamanho):
        return np.logical_or.reduce([self._faixa(tamanho, i) for i in self.itens])

    def regioes_limpeza(self, tamanho):
        return [(self._faixa(tamanho, i), i.estilo.limiar_limpeza) for i in self.itens]


class SetaPiscante(Animacao):
    """A seta some no início da janela e é redesenhada da cauda até a ponta.

    Não redesenha nada "à mão": a seta é apagada da imagem limpa e, a cada
    quadro, os pixels ORIGINAIS dela voltam até a distância já revelada.
    Por isso funciona com seta reta, em L ou curva, de qualquer cor.
    Fora da janela, a seta fica exatamente como no original.
    """

    BORDA_SUAVE = 2.0   # px de transição entre a parte revelada e a apagada

    def __init__(self, nome: str, caminho: Caminho, original: Image.Image, config: dict):
        self.nome = nome
        self.caminho = caminho
        self.original = original
        self.largura = float(config.get("largura", 12))
        self.limiar = int(config.get("limiar_limpeza", 700))
        self.janela = config["janela"]
        self.varredura = float(config.get("varredura", 0.7))  # fração da janela gasta revelando
        self._faixa = Mascaras.faixa(original.size, caminho.pontos, self.largura)
        ys, xs = np.nonzero(self._faixa)
        self._ys, self._xs = ys, xs
        self._s = caminho.projetar(xs + 0.5, ys + 0.5)

    def _alfa(self, quadro: int, total: int) -> np.ndarray:
        """Opacidade (0 a 1) dos pixels originais da seta neste quadro."""
        if not self.janela.contem(quadro, total):
            return np.ones(self._s.shape)
        p = min(1.0, self.janela.progresso(quadro, total) / self.varredura)
        return np.clip((p * self.caminho.comprimento - self._s) / self.BORDA_SUAVE + 0.5, 0, 1)

    def aplicar(self, imagem, quadro, total):
        alfa = np.zeros(self._faixa.shape, np.uint8)
        alfa[self._ys, self._xs] = np.round(self._alfa(quadro, total) * 255).astype(np.uint8)
        return Image.composite(self.original, imagem, Image.fromarray(alfa))

    def area(self, tamanho):
        return self._faixa

    def regioes_limpeza(self, tamanho):
        return [(self._faixa, self.limiar)]


class CardIluminado(Animacao):
    """Brilho suave que acende e apaga na borda de um card arredondado.

    O brilho é a borda engrossada e desfocada (como neon), mais um leve
    tom da mesma cor no interior. A intensidade segue um seno dentro da
    janela: sobe, chega ao máximo no meio e volta a zero, sem salto.
    """

    cria_cores_novas = True

    def __init__(self, nome: str, tamanho: tuple, config: dict, supersampling: int):
        self.nome = nome
        self.cor = tuple(config["cor"])
        self.janela = config["janela"]
        self.forca = float(config.get("forca", 0.9))
        self.preenchimento = float(config.get("preenchimento", 0.10))
        self._halo, self._interior = self._mascaras(tamanho, config, supersampling)

    @staticmethod
    def _mascaras(tamanho, config, ss):
        x0, y0, x1, y1 = config["caixa"]
        raio, largura, desfoque = config.get("raio", 24), config.get("largura", 5), config.get("desfoque", 5)
        W, H = tamanho
        borda = Image.new("L", (W * ss, H * ss), 0)
        ImageDraw.Draw(borda).rounded_rectangle([x0 * ss, y0 * ss, x1 * ss, y1 * ss], radius=raio * ss,
                                                outline=255, width=int(largura * ss))
        borda = borda.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(desfoque))
        halo = np.asarray(borda, float) / max(1, np.asarray(borda).max())
        interior = Image.new("L", (W, H), 0)
        ImageDraw.Draw(interior).rounded_rectangle([x0, y0, x1, y1], radius=raio, fill=255)
        return halo, np.asarray(interior, float) / 255

    def intensidade(self, quadro: int, total: int) -> float:
        if not self.janela.contem(quadro, total):
            return 0.0
        return math.sin(math.pi * self.janela.progresso(quadro, total, centrado=True))

    def aplicar(self, imagem, quadro, total):
        i = self.intensidade(quadro, total)
        if i <= 0:
            return imagem
        alfa = np.clip(self._halo * self.forca * i + self._interior * self.preenchimento * i, 0, 1)
        mascara = Image.fromarray(np.round(alfa * 255).astype(np.uint8))
        return Image.composite(Image.new("RGB", imagem.size, self.cor), imagem, mascara)

    def area(self, tamanho):
        return (self._halo > 1 / 255) | (self._interior > 0)


# ---------------------------------------------------------------------------
# Especificação e montagem das animações
# ---------------------------------------------------------------------------

class Especificacao:
    """Lê e interpreta o JSON. Único lugar que conhece o formato do arquivo."""

    def __init__(self, arquivo: str):
        self.pasta = Path(arquivo).resolve().parent
        dados = json.loads(Path(arquivo).read_text(encoding="utf-8"))
        self.entrada = str(self.pasta / dados["entrada"])
        self.saida = str(self.pasta / dados.get("saida", "saida.gif"))
        self.quadros = int(dados.get("quadros", 12))
        self.ms_por_quadro = int(dados.get("ms_por_quadro", 60))
        self.supersampling = int(dados.get("supersampling", 4))
        self.largura_faixa = int(dados.get("largura_faixa", 7))
        self.raio_inpaint = int(dados.get("raio_inpaint", 5))
        self.etapas = int(dados.get("etapas", 1))
        padrao = EstiloTracejado().combinar(dados.get("tracejado", {}))
        self.trilhas = [
            (Caminho(c.get("nome", f"caminho {i + 1}"), c["pontos"]), padrao.combinar(c.get("tracejado", {})))
            for i, c in enumerate(dados.get("caminhos", []))
        ]
        self.setas = [self._com_janela(s) for s in dados.get("setas_piscantes", [])]
        self.cards = [self._com_janela(c) for c in dados.get("cards", [])]

    def _com_janela(self, item: dict) -> dict:
        """Converte "etapa" ou "janela" do JSON num objeto JanelaDeTempo."""
        if "etapa" in item:
            janela = JanelaDeTempo(item["etapa"] / self.etapas, (item["etapa"] + 1) / self.etapas)
        else:
            janela = JanelaDeTempo(*item.get("janela", (0.0, 1.0)))
        return {**item, "janela": janela}


class FabricaDeAnimacoes:
    """Cria os objetos de animação a partir da especificação.

    Ordem de aplicação: tracejados e setas primeiro, cards por último, para
    o brilho do card cobrir de forma uniforme tudo o que está dentro dele.
    """

    def __init__(self, especificacao: Especificacao, original: Image.Image):
        self.esp = especificacao
        self.original = original

    def criar(self) -> list:
        esp, tamanho = self.esp, self.original.size
        grupos = {}
        for caminho, estilo in esp.trilhas:
            grupos.setdefault(estilo.cor, []).append(TracejadoAndando(caminho, estilo))
        animacoes = [CamadaDeTracejados(cor, itens, esp.supersampling, esp.largura_faixa)
                     for cor, itens in grupos.items()]
        for i, s in enumerate(esp.setas):
            nome = s.get("nome", f"seta {i + 1}")
            animacoes.append(SetaPiscante(nome, Caminho(nome, s["pontos"]), self.original, s))
        for i, c in enumerate(esp.cards):
            animacoes.append(CardIluminado(c.get("nome", f"card {i + 1}"), tamanho, c, esp.supersampling))
        return animacoes


# ---------------------------------------------------------------------------
# Etapas do processamento (cada classe faz uma coisa)
# ---------------------------------------------------------------------------

class LimpadorDeTraco:
    """Apaga do original só o que as animações vão redesenhar.

    1. Junta as regiões pedidas pelas animações (faixas sobre caminhos e setas).
    2. Marca, dentro delas, os pixels mais escuros que o limiar de cada uma.
    3. Preenche esses pixels com inpainting: o OpenCV "pinta" o buraco
       copiando o entorno, como um corretor inteligente.
    """

    def __init__(self, raio_inpaint: int):
        self.raio_inpaint = raio_inpaint

    def limpar(self, base: Image.Image, regioes: list) -> Image.Image:
        if not regioes:
            return base.copy()
        arr = np.array(base)
        soma = arr.astype(int).sum(2)
        uniao = np.logical_or.reduce([m for m, _ in regioes])
        mascara = np.zeros(soma.shape, bool)
        for regiao, limiar in regioes:
            mascara |= regiao & (soma < limiar)
        mascara = cv2.dilate(mascara.astype(np.uint8) * 255, np.ones((3, 3), np.uint8))
        mascara[~uniao] = 0  # nunca apagar fora das regiões
        limpa = cv2.inpaint(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), mascara, self.raio_inpaint, cv2.INPAINT_TELEA)
        return Image.fromarray(cv2.cvtColor(limpa, cv2.COLOR_BGR2RGB))


class RenderizadorDeQuadros:
    """Aplica, em ordem, todas as animações sobre a imagem limpa."""

    def __init__(self, limpa: Image.Image, animacoes: list):
        self.limpa = limpa
        self.animacoes = animacoes

    def quadro(self, f: int, total: int) -> Image.Image:
        resultado = self.limpa
        for animacao in self.animacoes:
            resultado = animacao.aplicar(resultado, f, total)
        return resultado

    def todos(self, total: int) -> list:
        return [self.quadro(f, total) for f in range(total)]


class MontadorDeGif:
    """Quantiza todos os quadros com UMA paleta e salva o GIF em loop.

    GIF aceita no máximo 256 cores. Se cada quadro tivesse a própria paleta,
    as cores "pulariam" entre quadros (cintilação). Paleta única e sem
    dithering (pontilhado) evitam isso. Escolha da paleta:
      - imagem original em modo P e nenhuma cor nova: a paleta original;
      - nenhuma cor nova: a imagem original reduzida a 256 cores;
      - há cores novas (brilhos): original + amostra dos quadros, juntos.
    """

    AMOSTRAS = 6

    def __init__(self, fonte: ImagemFonte, quadros: list, cria_cores_novas: bool):
        if not cria_cores_novas:
            original = fonte.original
            self.paleta = original if original.mode == "P" else fonte.rgb.quantize(256)
            return
        passo = max(1, len(quadros) // self.AMOSTRAS)
        amostra = [fonte.rgb] + quadros[::passo]
        W, H = fonte.rgb.size
        mosaico = Image.new("RGB", (W, H * len(amostra)))
        for i, q in enumerate(amostra):
            mosaico.paste(q, (0, i * H))
        self.paleta = mosaico.quantize(256)

    def quantizar(self, imagem: Image.Image) -> Image.Image:
        return imagem.quantize(palette=self.paleta, dither=Image.Dither.NONE)

    def salvar(self, quadros: list, saida: str, ms: int) -> None:
        p = [self.quantizar(q) for q in quadros]
        p[0].save(saida, save_all=True, append_images=p[1:], duration=ms, loop=0,
                  optimize=False, disposal=1)


class VerificadorDeGif:
    """Confere o GIF salvo contra as regras de entrega da skill."""

    LIMITE_MB = 5.0
    # O filtro LANCZOS espalha uma borda suave de até 3 px ao redor do traço
    # redesenhado (inclusive além das pontas do caminho). Essa margem não
    # conta como "mudança fora da animação".
    MARGEM_PX = 3

    def __init__(self, montador: MontadorDeGif, quadros: int, ms: int):
        self.montador = montador
        # Valores esperados: o GIF salvo precisa bater com o que foi pedido.
        self.quadros = quadros
        self.ms = ms

    def verificar(self, saida: str, base: Image.Image, area: np.ndarray) -> dict:
        quadros, ms = self.quadros, self.ms
        gif = Image.open(saida)
        # Fora da área animada nada pode mudar: compara com o original
        # quantizado (a mesma conversão para 256 cores que os quadros sofreram).
        referencia = np.array(self.montador.quantizar(base).convert("RGB"))
        nucleo = np.ones((2 * self.MARGEM_PX + 1,) * 2, np.uint8)
        fora = ~cv2.dilate(area.astype(np.uint8), nucleo).astype(bool)
        alterados = 0
        for i in range(gif.n_frames):
            gif.seek(i)
            alterados = max(alterados, int((np.array(gif.convert("RGB")) != referencia).any(2)[fora].sum()))
        mb = Path(saida).stat().st_size / 1_000_000
        gif.seek(0)
        relatorio = {
            "arquivo": saida,
            "resolucao": f"{gif.size[0]} x {gif.size[1]}",
            "quadros": gif.n_frames,
            "ms_por_quadro": gif.info.get("duration"),
            "loop": "infinito" if gif.info.get("loop") == 0 else gif.info.get("loop"),
            "tamanho_mb": round(mb, 2),
            "pixels_alterados_fora_da_animacao": alterados,
        }
        problemas = []
        if gif.size != base.size: problemas.append("resolução diferente da original")
        if gif.n_frames != quadros: problemas.append("número de quadros diferente do pedido")
        if gif.info.get("duration") != ms: problemas.append("duração por quadro diferente da pedida")
        if gif.info.get("loop") != 0: problemas.append("GIF sem loop infinito")
        if alterados: problemas.append("há pixels alterados fora da área animada")
        if mb > self.LIMITE_MB: problemas.append("arquivo acima de 5 MB: reduza quadros ou recorte a área animada")
        relatorio["aprovado"] = not problemas
        relatorio["problemas"] = problemas
        return relatorio


# ---------------------------------------------------------------------------
# Orquestração
# ---------------------------------------------------------------------------

class PipelineImageToGif:
    """Liga as etapas na ordem. Não sabe COMO cada etapa funciona, só a sequência."""

    def __init__(self, especificacao: Especificacao):
        self.esp = especificacao

    def executar(self, pasta_previa: str = None) -> dict:
        esp = self.esp
        fonte = ImagemFonte(esp.entrada)
        tamanho = fonte.rgb.size
        animacoes = FabricaDeAnimacoes(esp, fonte.rgb).criar()
        regioes = [r for a in animacoes for r in a.regioes_limpeza(tamanho)]
        limpa = LimpadorDeTraco(esp.raio_inpaint).limpar(fonte.rgb, regioes)
        quadros = RenderizadorDeQuadros(limpa, animacoes).todos(esp.quadros)
        montador = MontadorDeGif(fonte, quadros, any(a.cria_cores_novas for a in animacoes))
        montador.salvar(quadros, esp.saida, esp.ms_por_quadro)
        if pasta_previa:
            Path(pasta_previa).mkdir(parents=True, exist_ok=True)
            limpa.save(Path(pasta_previa) / "limpa.png")
            quadros[0].save(Path(pasta_previa) / "quadro0.png")
        area = np.logical_or.reduce([a.area(tamanho) for a in animacoes])
        verificador = VerificadorDeGif(montador, esp.quadros, esp.ms_por_quadro)
        relatorio = verificador.verificar(esp.saida, fonte.rgb, area)
        relatorio["elementos_animados"] = [a.nome for a in animacoes]
        return relatorio


class CliGerarGif:
    """Interface de linha de comando: só traduz argumentos em chamadas."""

    @staticmethod
    def executar(argv=None) -> dict:
        p = argparse.ArgumentParser(description="Gera o GIF animado da skill image-to-gif")
        p.add_argument("especificacao", help="arquivo JSON com entrada, saída e animações")
        p.add_argument("--previa", help="pasta para salvar limpa.png e quadro0.png")
        a = p.parse_args(argv)
        return PipelineImageToGif(Especificacao(a.especificacao)).executar(a.previa)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(CliGerarGif.executar(), ensure_ascii=False, indent=2))
