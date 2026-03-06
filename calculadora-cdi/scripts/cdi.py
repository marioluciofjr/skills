"""
cdi.py — Calculadora de valor futuro para investimentos atrelados ao CDI.

Uso:
    python cdi.py --valor 10000 --percentual-cdi 110 --periodo 12 --unidade meses
    python cdi.py --valor 10000 --percentual-cdi 110 --periodo 1 --unidade anos --taxa-cdi 10.40

Saída: JSON com valor_investido, periodo, taxa_efetiva_aa, valor_futuro, taxa_cdi_usada

Fontes de scraping (tentadas nesta ordem):
    1. API do Banco Central do Brasil (BCB) — mais confiável e estruturada
    2. melhorcambio.com/cdi — fallback via parsing de HTML

Se ambas as fontes falharem, o script encerra com erro — sem taxa padrão.
"""

import argparse
import json
import sys
import urllib.request
import re

# URL da API oficial do Banco Central (série 4389 = CDI acumulado diário, últimos registros)
BCB_API_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4389/dados/ultimos/1?formato=json"

# URL alternativa via scraping de HTML
CDI_SCRAPING_URL = "https://www.melhorcambio.com/cdi"

# Timeout em segundos para as requisições de rede
REQUEST_TIMEOUT = 8


def buscar_taxa_bcb() -> float | None:
    """
    Tenta obter a taxa CDI diária mais recente via API oficial do Banco Central.
    Converte a taxa diária para anual equivalente via capitalização composta.

    Retorna a taxa anual em % ou None se a requisição falhar.
    """
    try:
        req = urllib.request.Request(
            BCB_API_URL,
            headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as response:
            dados = json.loads(response.read().decode("utf-8"))

        # Resposta esperada: [{"data": "DD/MM/AAAA", "valor": "0.040018"}]
        taxa_diaria_pct = float(dados[0]["valor"])

        # Converte taxa diária para anual: (1 + i_diária)^252 - 1
        # 252 = número de dias úteis no ano (convenção do mercado brasileiro)
        taxa_diaria_dec = taxa_diaria_pct / 100
        taxa_anual_dec = (1 + taxa_diaria_dec) ** 252 - 1
        taxa_anual_pct = round(taxa_anual_dec * 100, 2)

        return taxa_anual_pct

    except Exception:
        # Falha silenciosa — a função chamadora tentará a próxima fonte
        return None


def buscar_taxa_scraping() -> float | None:
    """
    Tenta obter a taxa CDI via scraping da página melhorcambio.com/cdi.

    Retorna a taxa anual em % ou None se o parsing falhar.
    """
    try:
        req = urllib.request.Request(
            CDI_SCRAPING_URL,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as response:
            html = response.read().decode("utf-8", errors="ignore")

        # Padrão primário: número decimal seguido de "% a.a." na página
        match = re.search(r"(\d{1,2}[.,]\d{2})\s*%?\s*a\.a", html, re.IGNORECASE)
        if match:
            # Normaliza vírgula para ponto antes de converter para float
            return float(match.group(1).replace(",", "."))

        # Padrão secundário: valor próximo a elemento com "cdi" no nome
        match2 = re.search(r'"cdi[^"]*"[^>]*>[\s\S]*?(\d{1,2}[.,]\d{2})', html, re.IGNORECASE)
        if match2:
            return float(match2.group(1).replace(",", "."))

    except Exception:
        pass

    return None


def buscar_taxa_cdi() -> float:
    """
    Orquestra a busca da taxa CDI tentando as fontes disponíveis em ordem de prioridade:
        1. API do Banco Central
        2. Scraping do melhorcambio.com

    Encerra o script com código de erro se todas as fontes falharem.
    Não utiliza taxa padrão — a taxa deve sempre vir de uma fonte atualizada.
    """
    # Tentativa 1: API do Banco Central (fonte oficial)
    taxa = buscar_taxa_bcb()
    if taxa is not None:
        return taxa

    # Tentativa 2: scraping HTML do melhorcambio.com
    taxa = buscar_taxa_scraping()
    if taxa is not None:
        return taxa

    # Nenhuma fonte retornou dados — encerra com erro explícito
    print(
        json.dumps(
            {
                "erro": "Não foi possível obter a taxa CDI vigente. "
                        "Verifique a conexão com a internet ou informe a taxa manualmente com --taxa-cdi."
            },
            ensure_ascii=False,
        )
    )
    sys.exit(1)


def calcular_valor_futuro(
    valor: float,
    percentual_cdi: float,
    n_periodos: int,
    unidade: str,
    taxa_cdi_aa: float,
) -> dict:
    """
    Calcula o valor futuro de um investimento atrelado ao CDI usando juros compostos.

    Metodologia (padrão do mercado financeiro brasileiro):
        1. Taxa efetiva a.a. = (percentual_cdi / 100) × taxa_cdi_aa
        2. Taxa mensal equivalente = (1 + taxa_efetiva_aa)^(1/12) - 1
        3. Valor Futuro = valor × (1 + taxa_mensal)^n_meses

    Args:
        valor:          Valor investido em R$
        percentual_cdi: Percentual do CDI contratado (ex: 110 para 110% do CDI)
        n_periodos:     Quantidade de períodos (meses ou anos, conforme 'unidade')
        unidade:        'meses' ou 'anos'
        taxa_cdi_aa:    Taxa CDI anual em % (ex: 10.40 para 10,40% a.a.)

    Returns:
        Dicionário com valor_investido, periodo, taxa_efetiva_aa, valor_futuro, taxa_cdi_usada.
    """

    # Calcula a taxa efetiva anual aplicada ao produto (em %)
    taxa_efetiva_aa = (percentual_cdi / 100) * taxa_cdi_aa

    # Converte para decimal para uso nos cálculos
    taxa_efetiva_dec = taxa_efetiva_aa / 100

    # Converte o período para meses e monta o rótulo de exibição
    if unidade == "anos":
        n_meses = n_periodos * 12
        periodo_label = f"{n_periodos} {'ano' if n_periodos == 1 else 'anos'}"
    else:
        n_meses = n_periodos
        periodo_label = f"{n_periodos} {'mês' if n_periodos == 1 else 'meses'}"

    # Converte a taxa anual para mensal equivalente via capitalização composta
    # Fórmula: (1 + i_aa)^(1/12) - 1
    taxa_mensal = (1 + taxa_efetiva_dec) ** (1 / 12) - 1

    # Aplica juros compostos para calcular o montante final
    valor_futuro = valor * (1 + taxa_mensal) ** n_meses

    # Monta o rótulo da taxa — inclui o percentual do CDI quando diferente de 100%
    taxa_label = f"{taxa_efetiva_aa:.2f}%"
    if percentual_cdi != 100:
        taxa_label += f" ({percentual_cdi:.0f}% CDI)"

    return {
        "valor_investido": round(valor, 2),
        "periodo": periodo_label,
        "taxa_efetiva_aa": taxa_label,
        "valor_futuro": round(valor_futuro, 2),
        "taxa_cdi_usada": round(taxa_cdi_aa, 2),
    }


def formatar_brl(valor: float) -> str:
    """
    Formata um valor numérico no padrão monetário brasileiro (R$ X.XXX,XX).
    Utilizado para exibição amigável — não afeta os cálculos.
    """
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def main():
    # Define os argumentos aceitos pela linha de comando
    parser = argparse.ArgumentParser(description="Calculadora de valor futuro atrelado ao CDI")
    parser.add_argument("--valor",          type=float, required=True, help="Valor investido em R$")
    parser.add_argument("--percentual-cdi", type=float, default=100,  help="Percentual do CDI contratado (ex: 110)")
    parser.add_argument("--periodo",        type=int,   required=True, help="Número de períodos")
    parser.add_argument("--unidade",        choices=["meses", "anos"], default="meses", help="Unidade do período")
    parser.add_argument(
        "--taxa-cdi",
        type=float,
        default=None,
        help="Taxa CDI anual em %% (opcional; se omitida, busca via API do BCB ou scraping)",
    )
    args = parser.parse_args()

    # Determina a taxa CDI: argumento explícito tem prioridade sobre scraping
    if args.taxa_cdi is not None:
        taxa_cdi = args.taxa_cdi
    else:
        # Busca a taxa via fontes externas — encerra com erro se nenhuma funcionar
        taxa_cdi = buscar_taxa_cdi()

    # Executa o cálculo principal
    resultado = calcular_valor_futuro(
        valor=args.valor,
        percentual_cdi=args.percentual_cdi,
        n_periodos=args.periodo,
        unidade=args.unidade,
        taxa_cdi_aa=taxa_cdi,
    )

    # Saída em JSON para consumo pelo modelo de linguagem
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
