#!/usr/bin/env python3
"""
detectar_paralelismo.py

Varredura DETERMINÍSTICA (por regex) de candidatos a paralelismo negativo
("não é X, é Y" e variações), em português e inglês.

Por que este script existe:
Uma varredura feita só por raciocínio livre da IA, sem checklist estruturada,
pode encontrar quantidades diferentes de ocorrências em execuções diferentes
sobre o MESMO texto (ex.: 6 numa vez, 8 noutra). Este script existe para dar
um PISO MÍNIMO determinístico: os mesmos padrões, aplicados ao mesmo texto,
sempre retornam o mesmo resultado. A IA (guardrails 1 e 2 de metodo-doctor.md)
nunca deve reportar menos ocorrências do que este script encontrar, e ainda
deve complementar o resultado com julgamento contextual (outros idiomas,
variações semânticas sem conector explícito, uso legítimo vs. tique de IA).

Escopo coberto (alta confiança):
  - Conectores adversativos explícitos: "mas", "mas sim", "e sim", "senão",
    "porém", "contudo" (PT) / "but", "but rather", "instead" (EN).
  - "não apenas X, mas Y" / "not just X, but Y".
  - "no A, no B, just C" / "sem A, sem B, só C".
  - Antítese por repetição do mesmo verbo/palavra logo após a negação
    (ex.: "não compram... elas compram...", "It's not X. It's Y.").

Fora do escopo (fica a cargo do julgamento da IA, guardrail 1 e 2):
  - Antíteses só por ponto-e-vírgula/vírgula, sem conector explícito e sem
    repetição de palavra (ex.: "Vulnerabilidade não é fraqueza; é coragem"
    quando o verbo/palavra não se repete de forma detectável por regex).
  - Ordem invertida: "Y, não X" em vez de "não X, Y" (ex.: "Venho para
    enterrar César, não para elogiá-lo").
  - Repetição que ocorre ANTES da negação em vez de depois (ex.: "The target
    was never a man. The target was the truth.").
  - Contraste introduzido sem conector nem repetição (travessão, dois-pontos
    etc.), como em "not just a win for the bank—it's a win for everyone".
  - Idiomas além de português e inglês.

Uso:
    python detectar_paralelismo.py --file caminho/para/texto.txt
    echo "algum texto" | python detectar_paralelismo.py
    python detectar_paralelismo.py --file texto.txt --janela 150

Saída: JSON no stdout com o total de candidatos e a lista de ocorrências,
cada uma com o trecho citável (expandido até a pontuação de frase mais
próxima), o padrão que disparou o alerta e o idioma provável do disparo.
"""

import argparse
import json
import re
import sys

# ─────────────────────────────────────────────
# PADRÕES (nome legível, regex compilado, idioma)
# ─────────────────────────────────────────────

JANELA_PADRAO = 150  # distância máxima (em caracteres) entre a negação e o conector/repetição


def construir_padroes(janela: int):
    w = janela
    return [
        # Conectores adversativos explícitos — português
        ("PT: 'não ... mas sim'", re.compile(rf"\bnão\b.{{1,{w}}}?\bmas sim\b", re.IGNORECASE | re.DOTALL), "pt"),
        ("PT: 'não ... e sim'", re.compile(rf"\bnão\b.{{1,{w}}}?\be sim\b", re.IGNORECASE | re.DOTALL), "pt"),
        ("PT: 'não ... mas'", re.compile(rf"\bnão\b.{{1,{w}}}?\bmas\b", re.IGNORECASE | re.DOTALL), "pt"),
        ("PT: 'não ... porém'", re.compile(rf"\bnão\b.{{1,{w}}}?\bporém\b", re.IGNORECASE | re.DOTALL), "pt"),
        ("PT: 'não ... contudo'", re.compile(rf"\bnão\b.{{1,{w}}}?\bcontudo\b", re.IGNORECASE | re.DOTALL), "pt"),
        ("PT: 'não ... senão'", re.compile(rf"\bnão\b.{{1,{w}}}?\bsenão\b", re.IGNORECASE | re.DOTALL), "pt"),
        ("PT: 'não apenas ... mas'", re.compile(rf"\bnão apenas\b.{{1,{w}}}?\bmas\b", re.IGNORECASE | re.DOTALL), "pt"),
        ("PT: 'sem A, sem B, só C'", re.compile(rf"\bsem\s+\w+,\s*sem\s+\w+,?\s*só\s+\w+", re.IGNORECASE), "pt"),

        # Conectores adversativos explícitos — inglês
        ("EN: 'not ... but rather'", re.compile(rf"\bnot\b.{{1,{w}}}?\bbut rather\b", re.IGNORECASE | re.DOTALL), "en"),
        ("EN: 'not just ... but'", re.compile(rf"\bnot just\b.{{1,{w}}}?\bbut\b", re.IGNORECASE | re.DOTALL), "en"),
        ("EN: 'not ... but'", re.compile(rf"\bnot\b.{{1,{w}}}?\bbut\b", re.IGNORECASE | re.DOTALL), "en"),
        ("EN: 'not ... instead'", re.compile(rf"\bnot\b.{{1,{w}}}?\binstead\b", re.IGNORECASE | re.DOTALL), "en"),
        ("EN: 'no A, no B, just C'", re.compile(rf"\bno\s+\w+,\s*no\s+\w+,?\s*just\s+\w+", re.IGNORECASE), "en"),
        ("EN: 'isn't/wasn't ... it's'", re.compile(rf"\b\w+\s+(?:isn'?t|wasn'?t|aren'?t|weren'?t)\b.{{1,{w}}}?\b(?:it'?s|it is|this is|that is)\b", re.IGNORECASE | re.DOTALL), "en"),

        # Antítese por repetição da mesma palavra logo após a negação
        ("PT: repetição após 'não'", re.compile(rf"\bnão\s+(\w+)\b.{{1,{w}}}?\b\1\b", re.IGNORECASE | re.DOTALL), "pt"),
        ("EN: repetição após 'not/never'", re.compile(rf"\b(?:not|never|isn'?t|wasn'?t|aren'?t|weren'?t|doesn'?t|didn'?t)\s+(\w+)\b.{{1,{w}}}?\b\1\b", re.IGNORECASE | re.DOTALL), "en"),
        ("EN: repetição 'it's not ... it's'", re.compile(rf"\b(?:it'?s|it is|this is|that is)\s+not\b.{{1,{w}}}?\b(?:it'?s|it is|this is|that is)\b", re.IGNORECASE | re.DOTALL), "en"),
    ]


LIMITES_FRASE = re.compile(r"[.!?;\n]")


def expandir_para_frase(texto: str, inicio: int, fim: int, maximo: int = 300) -> str:
    """Expande o trecho encontrado até a pontuação de frase mais próxima, para citação legível."""
    ini_busca = max(0, inicio - maximo)
    fim_busca = min(len(texto), fim + maximo)

    antes = texto[ini_busca:inicio]
    pos_ponto_antes = [m.end() for m in LIMITES_FRASE.finditer(antes)]
    novo_inicio = ini_busca + (pos_ponto_antes[-1] if pos_ponto_antes else 0)

    depois = texto[fim:fim_busca]
    m_ponto_depois = LIMITES_FRASE.search(depois)
    novo_fim = fim + (m_ponto_depois.end() if m_ponto_depois else len(depois))

    return texto[novo_inicio:novo_fim].strip()


QUEBRA_DE_PARAGRAFO = re.compile(r"\n\s*\n+")


def escanear_paragrafo(paragrafo: str, padroes) -> list:
    encontrados = []
    spans_ja_cobertos = []

    for nome, regex, idioma in padroes:
        for m in regex.finditer(paragrafo):
            inicio, fim = m.span()
            # Evita reportar o mesmo trecho de texto duas vezes por padrões sobrepostos
            se_ja_coberto = any(
                inicio < s_fim and fim > s_ini for s_ini, s_fim in spans_ja_cobertos
            )
            if se_ja_coberto:
                continue
            spans_ja_cobertos.append((inicio, fim))
            encontrados.append({
                "trecho": expandir_para_frase(paragrafo, inicio, fim),
                "padrao": nome,
                "idioma_detectado": idioma,
                "_offset": inicio,
            })

    return encontrados


def escanear(texto: str, janela: int = JANELA_PADRAO) -> dict:
    padroes = construir_padroes(janela)
    encontrados = []

    # Varre parágrafo por parágrafo: um conector/repetição só conta como a mesma
    # ocorrência se estiver dentro do mesmo parágrafo — evita misturar citações
    # ou frases não relacionadas separadas por uma quebra de parágrafo.
    for paragrafo in QUEBRA_DE_PARAGRAFO.split(texto):
        if not paragrafo.strip():
            continue
        encontrados.extend(escanear_paragrafo(paragrafo, padroes))

    for oc in encontrados:
        oc.pop("_offset", None)

    return {
        "total_candidatos": len(encontrados),
        "ocorrencias": encontrados,
        "observacao": (
            "Este é um piso mínimo determinístico. A IA deve incluir todas estas "
            "ocorrências no diagnóstico (salvo justificativa explícita de falso "
            "positivo) e complementar com julgamento contextual para variações "
            "que este script não cobre (outros idiomas, antíteses sem conector "
            "explícito, ordem invertida)."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description="Varredura determinística de paralelismo negativo")
    parser.add_argument("--file", help="Caminho para o arquivo de texto a analisar. Se omitido, lê do stdin.")
    parser.add_argument("--janela", type=int, default=JANELA_PADRAO, help="Distância máxima em caracteres entre negação e conector/repetição.")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            texto = f.read()
    else:
        if hasattr(sys.stdin, "reconfigure"):
            sys.stdin.reconfigure(encoding="utf-8")
        texto = sys.stdin.read()

    resultado = escanear(texto, janela=args.janela)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
