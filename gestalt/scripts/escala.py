"""Gera uma escala de espaçamento e verifica o princípio G01 (Proximidade).

Uso:
  python escala.py --base 8
  python escala.py --base 8 --interno 8 --externo 16

G01 diz que o espaço entre grupos deve ser pelo menos 2 vezes o espaço dentro do grupo.
Assim, os olhos percebem quais elementos estão juntos.
"""
import argparse
import sys

BASES_VALIDAS = (4, 8)
RAZAO_MINIMA = 2.0
MULTIPLOS = (1, 2, 3, 4, 6, 8, 12, 16)


class EscalaEspacamento:
    """Valores de espaçamento múltiplos de uma base."""

    def __init__(self, base):
        if base not in BASES_VALIDAS:
            raise ValueError(f"Base inválida: {base}. Use 4 ou 8.")
        self.base = base

    def valores(self):
        return [self.base * multiplo for multiplo in MULTIPLOS]


class VerificacaoG01:
    """Compara o espaço externo de um grupo com o espaço interno dele."""

    def __init__(self, interno, externo):
        if interno <= 0:
            raise ValueError("O espaço interno precisa ser maior que zero.")
        self.razao = externo / interno

    def passa(self):
        return self.razao >= RAZAO_MINIMA

    def relatorio(self):
        resultado = "passa" if self.passa() else "falha"
        razao = f"{self.razao:.1f}".replace(".", ",")
        minimo = f"{RAZAO_MINIMA:.1f}".replace(".", ",")
        return f"G01: {resultado} (razão {razao}; mínimo {minimo})"


class Programa:
    """Interface de linha de comando."""

    def executar(self, argumentos):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
        leitor = argparse.ArgumentParser(description="Escala de espaçamento e verificação de G01.")
        leitor.add_argument("--base", type=int, required=True, choices=BASES_VALIDAS)
        leitor.add_argument("--interno", type=float)
        leitor.add_argument("--externo", type=float)
        lidos = leitor.parse_args(argumentos)
        if (lidos.interno is None) != (lidos.externo is None):
            leitor.error("informe --interno e --externo juntos")
        escala = EscalaEspacamento(lidos.base)
        print("Escala: " + ", ".join(str(v) for v in escala.valores()))
        if lidos.interno is None:
            return 0
        return self._verificar(lidos.interno, lidos.externo)

    @staticmethod
    def _verificar(interno, externo):
        try:
            print(VerificacaoG01(interno, externo).relatorio())
        except ValueError as erro:
            print(erro, file=sys.stderr)
            return 2
        return 0


if __name__ == "__main__":
    sys.exit(Programa().executar(sys.argv[1:]))
