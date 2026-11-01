"""Procura problemas de design em arquivos de interface, sem alterá-los (RF-23).

Uso: python lint_design.py arquivo.html outro.css

Lint é uma verificação automática que lê o arquivo sem executá-lo. Cada regra LD-01 a
LD-08 é uma classe própria (padrão Strategy): mudar uma regra não afeta as outras.
A leitura é por padrões de texto, então o lint aponta suspeitas, não garantias.
"""
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from contraste import CorHex, RazaoContraste  # noqa: E402

EXTENSOES = {".html", ".css", ".js", ".jsx", ".tsx", ".svg"}
MAX_MICROINTERACAO_MS = 1000
MIN_ALVO_PX = 24
HEX = r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b"
GENERICAS = {"serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui", "ui-sans-serif",
             "ui-serif", "ui-monospace", "-apple-system", "inherit", "initial", "unset", "revert"}


@dataclass(frozen=True)
class Aviso:
    """Um problema encontrado em uma linha do arquivo."""

    codigo: str
    severidade: str
    lei: str
    linha: int
    mensagem: str


class Texto:
    """O conteúdo analisado, sem comentários e com os números de linha preservados."""

    _COMENTARIOS = re.compile(r"/\*.*?\*/|<!--.*?-->", re.S)

    def __init__(self, bruto):
        self.conteudo = self._COMENTARIOS.sub(self._apaga_mantendo_linhas, bruto)

    @staticmethod
    def _apaga_mantendo_linhas(achado):
        return "\n" * achado.group(0).count("\n")

    def linha_de(self, posicao):
        return self.conteudo.count("\n", 0, posicao) + 1

    def blocos(self):
        """Devolve (seletor, declarações, posição) de cada regra de estilo e de cada style inline."""
        for achado in re.finditer(r"([^{}]*)\{([^{}]*)\}", self.conteudo):
            # Fica só o último trecho: em "nav > a", o alvo é "a"; e o HTML antes de <style> sai.
            seletor = re.split(r"[>;]", achado.group(1))[-1].strip()
            yield seletor, achado.group(2), achado.start(2)
        for achado in re.finditer(r"<([a-zA-Z][\w-]*)\b[^>]*?\bstyle\s*=\s*\"([^\"]*)\"", self.conteudo):
            yield achado.group(1), achado.group(2), achado.start(2)


class Regra:
    """Base das regras: cada subclasse define seus dados e o método avaliar."""

    codigo = ""
    severidade = ""
    lei = ""

    def avaliar(self, texto):
        raise NotImplementedError

    def _aviso(self, texto, posicao, mensagem):
        return Aviso(self.codigo, self.severidade, self.lei, texto.linha_de(posicao), mensagem)


class AnimacaoSemReducao(Regra):
    codigo, severidade, lei = "LD-01", "Média", "L19, WCAG 2.3.3"
    _ANIMA = re.compile(r"@keyframes|\b(?:transition|animation)(?:-[a-z-]+)?\s*:(?!\s*none)|\bgsap\.")

    def avaliar(self, texto):
        achado = self._ANIMA.search(texto.conteudo)
        if not achado or "prefers-reduced-motion" in texto.conteudo:
            return []
        return [self._aviso(texto, achado.start(), "Animação sem tratamento de prefers-reduced-motion.")]


class MicrointeracaoLonga(Regra):
    codigo, severidade, lei = "LD-02", "Baixa", "L19"
    _NUMERO = r"(\d*\.?\d+)\s*(ms|s)?\b"
    _DURACOES = (
        re.compile(rf"transition-duration\s*:\s*{_NUMERO}"),
        re.compile(r"\btransition\s*:\s*[^;}]*?(\d*\.?\d+)(ms|s)\b"),
        re.compile(rf"(?<![-\w])duration\s*:\s*{_NUMERO}"),
    )

    def avaliar(self, texto):
        avisos = []
        for padrao in self._DURACOES:
            for achado in padrao.finditer(texto.conteudo):
                milissegundos = self._em_ms(float(achado.group(1)), achado.group(2))
                if milissegundos > MAX_MICROINTERACAO_MS:
                    avisos.append(self._aviso(texto, achado.start(),
                                              f"Duração de {milissegundos:.0f} ms, acima de {MAX_MICROINTERACAO_MS} ms."))
        return avisos

    @staticmethod
    def _em_ms(valor, unidade):
        if unidade == "ms":
            return valor
        if unidade == "s":
            return valor * 1000
        # Sem unidade: GSAP usa segundos (0.3) e a Web Animations API usa milissegundos (300).
        return valor if valor >= 100 else valor * 1000


class FocoRemovido(Regra):
    codigo, severidade, lei = "LD-03", "Alta", "L18, WCAG 2.4.7"
    _SEM_CONTORNO = re.compile(r"\boutline\s*:\s*['\"]?(?:none|0(?:px)?)\b")

    def avaliar(self, texto):
        achado = self._SEM_CONTORNO.search(texto.conteudo)
        if not achado or ":focus-visible" in texto.conteudo:
            return []
        return [self._aviso(texto, achado.start(), "Contorno de foco removido sem regra :focus-visible.")]


class ZoomBloqueado(Regra):
    codigo, severidade, lei = "LD-04", "Alta", "WCAG 1.4.4"
    _META = re.compile(r"<meta\b[^>]*\bname\s*=\s*[\"']viewport[\"'][^>]*>", re.I)
    _BLOQUEIO = re.compile(r"user-scalable\s*=\s*(?:no|0)\b|maximum-scale\s*=\s*1(?:\.0*)?(?![\d.])", re.I)

    def avaliar(self, texto):
        return [self._aviso(texto, m.start(), "A meta viewport bloqueia o zoom.")
                for m in self._META.finditer(texto.conteudo) if self._BLOQUEIO.search(m.group(0))]


class ImagemSemAlt(Regra):
    codigo, severidade, lei = "LD-05", "Alta", "WCAG 1.1.1"
    _IMG = re.compile(r"<img\b[^>]*>", re.I)

    def avaliar(self, texto):
        return [self._aviso(texto, m.start(), "Imagem sem atributo alt.")
                for m in self._IMG.finditer(texto.conteudo) if not re.search(r"\balt\s*=", m.group(0))]


class FamiliasDemais(Regra):
    codigo, severidade, lei = "LD-06", "Baixa", "L12"
    _DECLARACAO = re.compile(r"font-?family\s*:\s*([^;}\n]+)", re.I)
    _LIMITE = 2

    def avaliar(self, texto):
        # Conta só a primeira família de cada declaração: as demais são reservas (fallback).
        vistas = {}
        for achado in self._DECLARACAO.finditer(texto.conteudo):
            familia = achado.group(1).split(",")[0].strip(" '\"`")
            if familia.lower() not in GENERICAS and not familia.startswith("var("):
                vistas.setdefault(familia.lower(), achado.start())
        if len(vistas) <= self._LIMITE:
            return []
        terceira = sorted(vistas.values())[self._LIMITE]
        return [self._aviso(texto, terceira, f"{len(vistas)} famílias tipográficas; o limite é {self._LIMITE}.")]


class ContrasteBaixo(Regra):
    codigo, severidade, lei = "LD-07", "Alta", "WCAG 1.4.3"
    _TEXTO = re.compile(rf"(?<![-\w])color\s*:\s*['\"]?({HEX})")
    _FUNDO = re.compile(rf"(?<![-\w])background(?:-color)?\s*:\s*['\"]?({HEX})")

    def avaliar(self, texto):
        avisos = []
        for _, declaracoes, posicao in texto.blocos():
            cor, fundo = self._TEXTO.search(declaracoes), self._FUNDO.search(declaracoes)
            if cor and fundo:
                razao = RazaoContraste(CorHex(cor.group(1)), CorHex(fundo.group(1)))
                if not razao.passa_texto_normal():
                    valor = f"{razao.valor():.2f}".replace(".", ",")
                    avisos.append(self._aviso(texto, posicao, f"Contraste de {valor}:1, abaixo de 4,5:1."))
        return avisos


class AlvoPequeno(Regra):
    codigo, severidade, lei = "LD-08", "Alta", "L18, WCAG 2.5.8"
    _INTERATIVO = re.compile(r"(?<![\w.#-])(?:button|a|input|select|textarea|summary)(?![-\w])"
                             r"|\.btn\b|\.button\b|\[role=[\"']?button")
    _LARGURA = re.compile(r"(?<![-\w])width\s*:\s*['\"]?(\d*\.?\d+)px")
    _ALTURA = re.compile(r"(?<![-\w])height\s*:\s*['\"]?(\d*\.?\d+)px")

    def avaliar(self, texto):
        avisos = []
        for seletor, declaracoes, posicao in texto.blocos():
            largura, altura = self._LARGURA.search(declaracoes), self._ALTURA.search(declaracoes)
            if largura and altura and self._INTERATIVO.search(seletor):
                if min(float(largura.group(1)), float(altura.group(1))) < MIN_ALVO_PX:
                    avisos.append(self._aviso(texto, posicao, f"Alvo interativo abaixo de {MIN_ALVO_PX} px."))
        return avisos


class LintDesign:
    """Aplica todas as regras a um arquivo ou a um trecho de texto."""

    def __init__(self):
        self.regras = [AnimacaoSemReducao(), MicrointeracaoLonga(), FocoRemovido(), ZoomBloqueado(),
                       ImagemSemAlt(), FamiliasDemais(), ContrasteBaixo(), AlvoPequeno()]

    def analisar_arquivo(self, caminho):
        caminho = Path(caminho)
        if caminho.suffix.lower() not in EXTENSOES:
            return []
        return self.analisar_texto(caminho.read_text(encoding="utf-8", errors="replace"), caminho.suffix)

    def analisar_texto(self, bruto, _extensao=".html"):
        texto = Texto(bruto)
        avisos = []
        for regra in self.regras:
            avisos.extend(regra.avaliar(texto))
        return sorted(avisos, key=lambda a: (a.linha, a.codigo))


class Programa:
    """Interface de linha de comando. Avisos não são erro: o código de saída só muda se faltar arquivo."""

    @staticmethod
    def executar(argumentos):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
        if not argumentos:
            print("Uso: python lint_design.py arquivo [arquivo...]", file=sys.stderr)
            return 2
        lint = LintDesign()
        codigo_saida = 0
        for nome in argumentos:
            caminho = Path(nome)
            if not caminho.is_file():
                print(f"Arquivo não encontrado: {nome}", file=sys.stderr)
                codigo_saida = 2
                continue
            for aviso in lint.analisar_arquivo(caminho):
                print(f"{aviso.codigo} [{aviso.severidade}] {caminho.name}:{aviso.linha}: "
                      f"{aviso.mensagem} ({aviso.lei})")
        return codigo_saida


if __name__ == "__main__":
    sys.exit(Programa().executar(sys.argv[1:]))
