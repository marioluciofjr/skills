"""Calcula a razão de contraste entre duas cores, conforme a WCAG 2.2.

Uso: python contraste.py "#767676" "#FFFFFF"

Razão de contraste é a diferença de luminosidade entre duas cores. Vai de 1:1 (cores
iguais) a 21:1 (preto sobre branco).
"""
import argparse
import re
import sys

LIMIAR_TEXTO_NORMAL = 4.5
LIMIAR_TEXTO_GRANDE = 3.0
LIMIAR_COMPONENTE = 3.0


class CorHex:
    """Uma cor em hexadecimal, com ou sem "#", na forma longa ou curta."""

    _FORMATO = re.compile(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")

    def __init__(self, texto):
        achado = self._FORMATO.match(texto.strip())
        if not achado:
            raise ValueError(f"Cor inválida: {texto}. Use o formato #RRGGBB ou #RGB.")
        digitos = achado.group(1)
        if len(digitos) == 3:
            digitos = "".join(d * 2 for d in digitos)
        self._rgb = tuple(int(digitos[i:i + 2], 16) for i in (0, 2, 4))

    def rgb(self):
        return self._rgb

    def luminancia(self):
        """Luminância relativa: quanta luz a cor reflete, de 0 (preto) a 1 (branco)."""
        vermelho, verde, azul = (self._linear(canal / 255) for canal in self._rgb)
        return 0.2126 * vermelho + 0.7152 * verde + 0.0722 * azul

    @staticmethod
    def _linear(canal):
        # A tela não mostra a luz de forma proporcional; esta fórmula desfaz essa curva.
        return canal / 12.92 if canal <= 0.04045 else ((canal + 0.055) / 1.055) ** 2.4


class RazaoContraste:
    """Compara duas cores e responde aos limiares da WCAG."""

    def __init__(self, cor_a, cor_b):
        clara, escura = sorted((cor_a.luminancia(), cor_b.luminancia()), reverse=True)
        self._valor = (clara + 0.05) / (escura + 0.05)

    def valor(self):
        return self._valor

    # Os limiares usam o valor exato: 4,48 não pode virar 4,5 por arredondamento.
    def passa_texto_normal(self):
        return self._valor >= LIMIAR_TEXTO_NORMAL

    def passa_texto_grande(self):
        return self._valor >= LIMIAR_TEXTO_GRANDE

    def passa_componente(self):
        return self._valor >= LIMIAR_COMPONENTE


class Programa:
    """Interface de linha de comando."""

    def executar(self, argumentos):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
        leitor = argparse.ArgumentParser(description="Razão de contraste entre duas cores.")
        leitor.add_argument("cor_a")
        leitor.add_argument("cor_b")
        lidos = leitor.parse_args(argumentos)
        try:
            razao = RazaoContraste(CorHex(lidos.cor_a), CorHex(lidos.cor_b))
        except ValueError as erro:
            print(erro, file=sys.stderr)
            return 2
        print(self._relatorio(razao))
        return 0

    def _relatorio(self, razao):
        return "\n".join([
            f"Razão de contraste: {razao.valor():.2f}:1".replace(".", ","),
            f"AA texto normal: {self._resultado(razao.passa_texto_normal())}",
            f"AA texto grande: {self._resultado(razao.passa_texto_grande())}",
            f"AA componente não textual: {self._resultado(razao.passa_componente())}",
        ])

    @staticmethod
    def _resultado(passou):
        return "passa" if passou else "falha"


if __name__ == "__main__":
    sys.exit(Programa().executar(sys.argv[1:]))
