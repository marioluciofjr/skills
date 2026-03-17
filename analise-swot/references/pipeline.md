# Pipeline da Skill: Análise SWOT Profissional

## Visão Geral

```
Usuário descreve o projeto
        │
        ▼
[ETAPA 1] agente-análise
  → Identifica contexto
  → Formula 5 perguntas
        │
        ▼
[HUMAN IN THE LOOP] Usuário responde as 5 perguntas
        │
        ▼
[ETAPA 2] Debate Multiagente — Rodada 1
  ┌─────────────────────────────┐
  │  agente-força   (paralelo)  │
  │  agente-fraqueza (paralelo) │  ← Debates internos e cruzamentos
  │  agente-oportunidade (par.) │
  │  agente-ameaça   (paralelo) │
  └─────────────────────────────┘
  + agente-pesquisa (web em paralelo)
        │
        ▼
[HUMAN IN THE LOOP] Feedback da Rodada 1
        │
        ▼
[ETAPA 2] Debate Multiagente — Rodada 2
  (mais sofisticado, incorpora feedback e pesquisa)
        │
        ▼
[HUMAN IN THE LOOP] Feedback da Rodada 2
        │
        ▼
[ETAPA 2] Debate Multiagente — Rodada 3
  (refinamento final, cruzamentos estratégicos)
        │
        ▼
[HUMAN IN THE LOOP] Feedback da Rodada 3
        │
        ▼
[ETAPA 3] agente-compilador
  → Consolida todas as rodadas
  → Prioriza e elimina redundâncias
  → Gera análise SWOT estruturada
  → Sugere próximos passos estratégicos
        │
        ▼
Output final usando template assets/analise-swot.md
+ Sugestão de gerar visualização com scripts/gerar-swot-visual.py
```

---

## Detalhamento de cada Etapa

### Etapa 1: Identificação

**Agente:** `agente-análise`
**Input:** Descrição inicial do projeto pela pessoa usuária
**Output:** 5 perguntas numeradas para o usuário responder

As perguntas devem cobrir:
1. Segmento / mercado de atuação
2. Público-alvo e proposta de valor
3. Situação atual (início, crescimento, crise, expansão etc.)
4. Recursos disponíveis (financeiros, humanos, tecnológicos)
5. Objetivo estratégico com esta análise

---

### Etapa 2: Debate Multiagente

**Rodada 1 — Mapeamento Inicial**
- Cada agente apresenta os pontos mais evidentes de sua categoria
- O agente-pesquisa busca dados de mercado, concorrência e contexto
- Os agentes fazem as primeiras inter-relações

**Rodada 2 — Aprofundamento**
- Os agentes questionam e refinam os pontos levantados na rodada anterior
- Incorporam o feedback do usuário
- O agente-pesquisa aprofunda as buscas com base nos pontos mais polêmicos
- Surgem os cruzamentos estratégicos (Força+Oportunidade, Fraqueza+Ameaça etc.)

**Rodada 3 — Priorização**
- Os agentes priorizam os 3-5 pontos mais relevantes de cada quadrante
- Identificam os cruzamentos com maior impacto estratégico
- Consolidam argumentos para o compilador

**Formato de apresentação de cada rodada:**
```
--- RODADA [N] DE 3 ---

🔵 AGENTE FORÇA:
[argumentos e pontos levantados]

🔴 AGENTE FRAQUEZA:
[argumentos e pontos levantados, incluindo contestações]

🟢 AGENTE OPORTUNIDADE:
[argumentos e pontos levantados]

🟠 AGENTE AMEAÇA:
[argumentos e pontos levantados, incluindo contestações]

🔍 PESQUISA (dados e fontes):
[insights da web que alimentam o debate]

--- HUMAN IN THE LOOP ---
💬 Resumo da rodada: [síntese de 2-3 linhas]
❓ O que você quer reforçar, corrigir ou acrescentar antes da próxima rodada?
```

---

### Etapa 3: Compilação Final

**Agente:** `agente-compilador`
**Input:** Transcrição completa das 3 rodadas + feedback do usuário
**Output:** Análise SWOT estruturada no formato de `assets/analise-swot.md`

O compilador deve:
- Organizar os pontos por relevância (mais impactantes primeiro)
- Apresentar evidências ou raciocínios para cada ponto
- Cruzar os quadrantes para sugerir estratégias
- Listar próximos passos acionist
