# Catálogo: qual UI para cada frase

Escolha pelo **tipo de pergunta** que a frase-título responde. A coluna "Motion sugerido" aponta o tipo
herói mais natural para a UI (fichas em `tipos-de-motion.md`). Os snippets estão em `scripts/components/`
e cada um tem uma receita em `Motion.recipes`.

| A frase fala de... | Componente | Receita | Dados necessários | Motion sugerido |
|---|---|---|---|---|
| Resultados gerais, “o que encontramos”, panorama, crescimento | `phone-stats.html` + `notif-card.html` | `phone`, `floatCard` | 1 KPI principal com comparação, 2 KPIs secundários, 2–3 valores para barras com meta | flutuação 3D num `div` em volta do `.phone`, contador |
| Temas, palavras-chave, termos, assuntos, buscas | `search-list.html` | `searchList` | termo buscado, 4–6 itens com contagem, 1 item sinalizado (exceção) | digitação, marcador de destaque |
| Pessoas, líderes, clientes, empresas, top N | `leaderboard.html` + `notif-card.html` (variante huge) | `leaderboard`, `floatCard` | 4–6 nomes, organização, métrica; 1 recorde em outra métrica | contador, micro-interação de cursor |
| Método, processo, jornada, como funciona, etapas | `pipeline.html` + `terminal.html` | `pipeline`, `terminal` | 3–4 etapas com título e descrição curta; 1 fórmula ou regra | desenho de traço no trilho, digitação |
| Comparação de duas visões, setores, segmentos, antes x depois | `segmented-bars.html` | `segmentedBars` | 2 séries com 4–6 itens cada (rótulo, valor, proporção) | micro-interação de cursor |
| Um único número impactante | `notif-card.html` (huge) sozinho, grande | `floatCard` | valor, unidade, contexto de uma linha | push de câmera, morphing (`dot` para `card`) |
| Linha do tempo, evolução | `pipeline.html` com anos nos nós | `pipeline` | 3–4 marcos com ano e fato | desenho de traço |
| Fórmula, regra, critério | `terminal.html` | `terminal` | texto de até ~70 caracteres | digitação |

## Combinações que funcionam

- Painel principal + card flutuante sobreposto (profundidade e um segundo foco).
- Janela com interação (cursor) na cena do meio, para quebrar o ritmo.
- A última cena antes do encerramento deve ter barras ou elementos discretos que possam virar partículas
  (`segmented-bars.html` é o padrão; listas com `.fill` também servem).

## Quando nenhum componente serve

Crie um novo seguindo o mesmo contrato: snippet em `scripts/components/` (classes, sem ids de estilo,
dados em `data-*`), estilos em `scripts/runtime/components.css`, receita em
`scripts/runtime/motion-recipes.js` com assinatura `(escopo, t, opções)` que devolve o instante final.
Exemplos de novos componentes: mapa de pontos, calendário, chat com mensagens, kanban, gráfico de linha.
