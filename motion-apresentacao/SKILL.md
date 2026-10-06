---
name: motion-apresentacao
description: Cria apresentações em motion estilo lançamento de app (HTML 1920x1080 com GSAP, headlines palavra por palavra, mockups de UI, echo trail, partículas que formam o logo) e renderiza o MP4 quadro a quadro. Use SEMPRE que a pessoa pedir "motion", "apresentação em motion", "vídeo de lançamento", "motion de relatório", "animar uma apresentação", "transformar relatório/pesquisa/deck em vídeo", "motion graphics em HTML", "vídeo com GSAP", "vídeo de produto", "apresentação pessoal em vídeo", "tipos de motion", "/motion", ou quiser apresentar dados, resultados ou um produto em vídeo curto animado, mesmo sem usar a palavra motion.
---

# Motion de apresentação (HTML + MP4)

Transforma um conteúdo (relatório, pesquisa, deck, lançamento) em um filme curto de 20 a 60 s com cara de
lançamento de app: fundo escuro, headlines grandes reveladas palavra por palavra, uma UI desenhada para
cada frase, transições rápidas com echo trail e sem cortes secos, e um encerramento em que os elementos
da última cena se transformam no logo da marca. Entrega um HTML que roda em loop e, se pedido, um MP4
renderizado quadro a quadro.

Todo o código está em `scripts/` (o diretório desta skill). As decisões de design estão em `references/`.
O processo de produção por trás das etapas (o que fecha cada fase e como evitar retrabalho) está em
`references/guia-motion-graphics.md`.

## Etapa 1 — Faça as 5 perguntas iniciais (sempre)

A elicitação de requisitos é **sempre em múltipla escolha**, no estilo do Claude Code: cada pergunta tem
de 2 a 4 opções, a primeira é a recomendada e leva "(Recomendado)" no fim do rótulo, e a pessoa sempre
pode digitar uma resposta própria. Nada de perguntas abertas nesta etapa.

Antes de montar as opções, leia o pedido e os anexos. As opções devem ser **específicas do material**
(ex.: "Executivos e investidores — despertar interesse pelo relatório completo", "Logo extraído da capa
do PDF"), não genéricas. A opção recomendada é a que melhor combina com o que a pessoa já disse; se ela
já respondeu algo explicitamente, a recomendada é exatamente essa resposta, para ela só confirmar.

**Como perguntar**

- Com a ferramenta `AskUserQuestion` disponível: faça duas chamadas seguidas, porque cada chamada aceita
  até 4 perguntas. Primeira chamada: perguntas 1 a 3. Segunda chamada: perguntas 4 e 5. Use `header`
  curto (até 12 caracteres), `multiSelect: false` (exceto nas mensagens-chave, que podem ser múltiplas)
  e uma `description` de uma linha quando o rótulo sozinho for ambíguo.
- Sem a ferramenta: envie as 5 perguntas numa única mensagem, cada uma com opções A, B, C (e D), a
  recomendada marcada com "(Recomendado)" e sempre na letra A, e peça a resposta no formato "1A 2B 3A 4C 5A"
  ou "aceito as recomendadas".
- Espere as respostas antes de criar qualquer arquivo. Se a sessão estiver sem ninguém acompanhando,
  assuma todas as recomendadas, diga no topo do trabalho quais assumiu e siga.

**As 5 perguntas** (bancos de opções, com exemplos, em `references/perguntas-iniciais.md`)

| # | header | Pergunta | Recomendado padrão |
|---|---|---|---|
| 1 | Público | Para quem é o motion e qual ação ele deve provocar? | Público profissional; despertar interesse pelo conteúdo completo |
| 2 | Mensagens | Quais mensagens-chave não podem faltar? (múltipla) | Os 3 a 6 dados mais fortes do material |
| 3 | Marca | De onde vem o logo e o que entra na tela final? | Logo do próprio material + nome + tagline do site da marca |
| 4 | Estrutura | Quantas cenas, qual duração e qual comportamento ao final? | Abertura + 5 cenas + encerramento com logo; 30 s; em loop |
| 5 | Entrega | Qual estética, formato e arquivos de saída? | P&B minimalista; 16:9 1920x1080; HTML + MP4 |

Como transformar as respostas em decisões: seção "Das respostas às decisões" em
`references/boas-praticas-motion.md`.

## Etapa 2 — Extraia o conteúdo

Leia o material inteiro. Para cada cena, separe: a frase-título (headline), um subtítulo de uma linha com
o insight e de 3 a 6 dados exatos (números, nomes, rankings). Copie os números exatamente como estão na
fonte e mantenha a formatação local (8.116; 36,07; 742,4k). Não invente dados para preencher UI.

## Etapa 3 — Prepare o logo

Siga `references/marca-e-logo.md`. O resultado é `logo.png` (silhueta luminosa sobre transparente) e
`logo.json` (proporção e onde termina o símbolo e começa o nome), gerados por `scripts/extract_logo.py`.

## Etapa 4 — Monte o storyboard

1. Para cada frase-título, escolha a UI em `references/catalogo-ui.md`: a UI precisa *demonstrar* a frase
   (ranking para "líderes", busca de termos para "temas", pipeline para "metodologia" etc.).
2. Para cada cena, escolha em `references/tipos-de-motion.md` um tipo de motion herói (o movimento que
   carrega a mensagem) e no máximo dois de apoio. Alterne os tipos herói entre cenas para criar ritmo e
   confira a tabela de conflitos antes de combinar dois tipos no mesmo elemento.
3. Distribua o tempo com as regras de `references/boas-praticas-motion.md` (abertura ~3 s, cenas de
   ~4 s com 0,2 s de sobreposição, encerramento ~5,6 s).
4. Mostre o mapa de tempo numa tabela curta no chat (cena, tempo, UI, motion, dado principal) e siga sem
   esperar aprovação, a menos que a pessoa tenha pedido para revisar antes.

## Etapa 5 — Escreva o projeto

Crie uma pasta de projeto (por exemplo `motion-<tema>/`) com quatro arquivos, partindo de
`scripts/example/` como modelo:

- `config.json` — título, idioma, tamanho, tema, fontes, marca e chrome (esquema em `references/arquitetura-e-api.md`)
- `scenes.html` — uma `<section class="scene" id="...">` por cena, montada com os snippets de `scripts/components/`
- `scenes.js` — a coreografia, registrada com `Motion.compose`, usando só a API pública: `M.*`, `M.recipes.*`
  (componentes) e `M.types.*` (tipos de motion); detalhes em `references/arquitetura-e-api.md`
- `logo.png` + `logo.json` — da etapa 3

Regras que evitam os erros mais comuns (detalhes em `references/arquitetura-e-api.md`):
estilize sempre por classe, nunca por id; use `fromTo` com estados explícitos; toda cena tem entrada
(`M.sceneIn`) e saída (`M.sceneOut`); a última cena entrega elementos de origem para `M.brand.outro`.
Para layout e hierarquia visual, siga `references/boas-praticas-ui.md`.

## Etapa 6 — Gere o HTML

Execute, a partir do diretório da skill (no Windows, troque `python3` por `python`):

1. `python3 scripts/prepare_deps.py <projeto> --dir <deps>` — baixa GSAP e fontes via npm (uma vez por projeto)
2. `python3 scripts/build_motion.py <projeto> --out <saida>.html` — HTML com GSAP e fontes por CDN
3. Para um HTML 100% offline, acrescente `--inline-gsap <deps>/gsap.min.js --inline-fonts <deps>/fonts.css`

## Etapa 7 — Revise antes de entregar

`python3 scripts/preview_frames.py <saida>.html --times <instantes> --out <pasta> --deps <deps>` captura
quadros com o relógio virtual e monta `sheet.png`. Escolha instantes no meio de cada cena, no meio de
cada transição e nas fases do encerramento. Abra a grade e confira a lista de QA de
`references/renderizacao-e-qa.md`. Corrija e repita até a grade passar.

## Etapa 8 — Renderize o MP4 (se pedido)

`python3 scripts/render_mp4.py <saida>.html --out <saida>.mp4 --deps <deps>` (30 fps, H.264, CRF 16).
O render leva cerca de 3 a 5 s por segundo de filme. Rode em segundo plano e acompanhe o log. Depois,
`python3 scripts/contact_sheet.py --video <saida>.mp4 --times ... --out check.png` para conferir o vídeo.

## Etapa 9 — Entregue

Envie o HTML e o MP4 como arquivos. Na resposta: uma linha com o que foi entregue, a tabela do mapa de
tempo e no máximo um próximo passo real (ex.: versão vertical, versão que termina congelada no logo).

## Dependências do ambiente

Python 3.10+, Pillow, NumPy, Playwright com Chromium, ffmpeg, poppler-utils (pdftoppm, pdfinfo) e npm.
GSAP e Google Fonts costumam ser bloqueados em sandboxes: `prepare_deps.py` busca os dois pelo registro
npm e `browser_session.py` os serve localmente durante preview e render.

## Mapa dos arquivos

| Caminho | Para que serve |
|---|---|
| `references/guia-motion-graphics.md` | Processo de produção: fases, critério de pronto, roteiros-modelo por formato, revisões |
| `references/tipos-de-motion.md` | Os 15 tipos de motion: escolha rápida, fichas com tempo e chamada, princípios, conflitos |
| `references/perguntas-iniciais.md` | Bancos de opções de múltipla escolha das 5 perguntas, regras da opção recomendada e exemplo |
| `references/arquitetura-e-api.md` | Módulos do runtime, contrato do projeto, esquema do config, API `Motion` e receitas, armadilhas |
| `references/boas-praticas-motion.md` | Tempo, easing, stagger, transições, echo trail, ritmo, das respostas às decisões |
| `references/boas-praticas-ui.md` | Grid, tipografia, P&B, profundidade, mockups, dados na tela |
| `references/catalogo-ui.md` | Qual componente usar para cada tipo de frase, com dados exigidos |
| `references/marca-e-logo.md` | Como obter, recortar e validar o logo |
| `references/renderizacao-e-qa.md` | Relógio virtual, MP4, checklist de QA, problemas conhecidos |
| `scripts/runtime/` | CSS e JS embutidos no HTML (core, partículas, chrome, marca, receitas, tipos de motion, shell) |
| `scripts/components/` | Snippets HTML de cada componente de UI |
| `scripts/example/` | Projeto completo de referência (relatório CEOs no LinkedIn, 30 s) |
| `scripts/*.py` | build, deps, logo, sessão do navegador, render, preview, contact sheet (classes, uma responsabilidade por arquivo) |
