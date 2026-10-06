# Arquitetura e API do runtime

## Sumário
1. Visão geral do pipeline
2. Módulos e responsabilidades
3. Contrato do projeto
4. Esquema do config.json
5. API do Motion (core)
6. Chrome, marca, receitas e tipos de motion
7. Regras de construção da linha do tempo
8. Armadilhas conhecidas (e por que existem)

## 1. Visão geral do pipeline

Projeto (config + cenas + coreografia + logo) → `build_motion.py` → HTML autocontido →
`preview_frames.py` (revisão) → `render_mp4.py` (vídeo).

O HTML final tem um único palco (`#stage`) de tamanho fixo (padrão 1920x1080) escalado para caber em
qualquer janela, e uma única linha do tempo mestre do GSAP (`window.__tl`). Tudo o que acontece no filme
está nessa linha do tempo, o que permite loop perfeito, pausa (barra de espaço) e renderização
determinística.

## 2. Módulos e responsabilidades

Cada arquivo tem uma única responsabilidade e conversa com os outros só por interfaces pequenas.

| Arquivo | Responsabilidade | Depende de | Expõe |
|---|---|---|---|
| `runtime/motion-base.css` | Palco, tipografia das cenas, sobreposições globais e ordem de empilhamento | tokens do tema | classes |
| `runtime/components.css` | Kit de UI (janela, celular, cards, listas, gráficos, pipeline, terminal) | tokens do tema | classes |
| `runtime/motion-core.js` | Palco, linha do tempo, primitivas (texto, contadores, cursor, transições, echo) | gsap | `window.Motion`, `window.__tl` |
| `runtime/motion-particles.js` | Partículas em canvas que convergem para a forma de uma imagem | nada | `window.MotionParticles` |
| `runtime/motion-chrome.js` | Cabeçalho e barra de progresso por seção | Motion | `Motion.chrome` |
| `runtime/motion-brand.js` | Abertura com logo e encerramento com partículas + tagline | Motion, MotionParticles | `Motion.brand` |
| `runtime/motion-recipes.js` | Coreografias prontas de cada componente | Motion | `Motion.recipes` |
| `runtime/motion-types.js` + `motion-types.css` | Tipos de motion reutilizáveis em qualquer elemento (máscara, íris, traço, destaque, 3D, morph, parallax, câmera) | Motion | `Motion.types` |
| `runtime/shell.html` | Esqueleto HTML com marcadores de substituição | nada | modelo |
| `motion_config.py` | Esquema, padrões e validação do config | nada | `MotionConfig.load`, `MotionConfig.font_families`, `ConfigError` |
| `build_motion.py` | Montar o HTML a partir do projeto | motion_config, runtime | `HtmlBuilder`, CLI |
| `prepare_deps.py` | Baixar GSAP e fontes via npm, gerar fonts.css | motion_config | `NpmFetcher`, `FontPackager`, `DepsPreparer`, CLI |
| `extract_logo.py` | Gerar silhueta do logo e metadados | Pillow, NumPy, poppler | `LogoSilhouette`, `PdfRasterizer`, `PlaceholderLogo`, CLI |
| `browser_session.py` | Abrir o HTML com relógio virtual e deps locais | Playwright | `MotionBrowser` (`async with`), `MotionPage` |
| `render_mp4.py` | Capturar quadros e codificar MP4 | browser_session, ffmpeg | `Mp4Renderer`, `RenderSettings`, `FfmpegWriter`, CLI |
| `preview_frames.py` | Capturar quadros pontuais e montar a grade | browser_session, contact_sheet | `FramePreviewer`, CLI |
| `contact_sheet.py` | Montar grade de miniaturas (de imagens ou de vídeo) | Pillow, ffmpeg | `ContactSheet`, `VideoFrameExtractor`, CLI |

Para estender: um componente novo = snippet em `components/` + bloco em `components.css` + receita em
`motion-recipes.js`. Um tipo de motion novo = função em `motion-types.js` (+ estilo em `motion-types.css`,
se precisar) e ficha em `references/tipos-de-motion.md`. Um efeito global novo = módulo novo em `runtime/` acrescentado à lista `JS_FILES` do
`build_motion.py`, plugado em `Motion` sem alterar o core.

## 3. Contrato do projeto

Uma pasta com:

- `config.json` — obrigatório
- `scenes.html` — obrigatório; só as `<section class="scene">` das cenas. Pode usar o marcador `{{LOGO}}`
  em `src` de imagens para reaproveitar o logo, e `src` relativos a arquivos do projeto (viram data URI)
- `scenes.js` — obrigatório; precisa chamar `Motion.compose(function (M) { ... })`
- `logo.png` + `logo.json` — recomendados (sem logo, a abertura e o encerramento de marca são omitidos)

A abertura, o encerramento, o chrome, o cursor e as linhas de varredura são criados pelos módulos; não
os escreva no `scenes.html`.

## 4. Esquema do config.json

| Campo | Tipo | Padrão | Uso |
|---|---|---|---|
| `title` | texto | "Apresentação em motion" | título da página e nome do arquivo de saída |
| `lang`, `locale` | texto | "pt-BR" | idioma do HTML e formatação dos contadores |
| `width`, `height` | número | 1920, 1080 | tamanho do palco (use 1080x1080 ou 1080x1920 para quadrado/vertical) |
| `loop` | booleano | true | repetir a linha do tempo |
| `gsap_version` | texto | "3.12.5" | versão do GSAP (CDN e npm) |
| `theme` | objeto | P&B | `bg`, `fg` e cinzas `g1` (texto secundário) a `g5` (superfície mais escura) |
| `fonts.display`, `fonts.mono` | objeto | Inter Tight / JetBrains Mono | `family` (nome no Google Fonts) e `weights` |
| `brand.name` | texto | — | texto alternativo do logo e do chrome |
| `brand.logo` | caminho | — | PNG da silhueta, relativo ao projeto |
| `brand.aspect`, `brand.mark_end`, `brand.word_start` | número | do logo.json | proporção e frações onde termina o símbolo e começa o nome |
| `brand.tagline` | texto | — | frase final; "|" quebra linha |
| `brand.tagline_dim` | número | 0 | quantas palavras iniciais da tagline ficam em cinza |
| `brand.url` | texto | — | linha final em fonte mono |
| `brand.intro` | objeto | — | legenda da abertura: `kicker`, `title`, `meta` |
| `brand.lockup_width` | número | 52% da largura | largura do logo completo no palco |
| `brand.particle_step` | número | 6 | densidade das partículas (menor = mais partículas) |
| `chrome` | objeto ou null | null | `left`, `right`, `sections` (rótulos da barra de progresso) |

O `scripts/example/config.json` é o modelo completo.

## 5. API do Motion (core)

Todas as funções de agendamento recebem o instante `t` em segundos na linha do tempo mestre e, quando
faz sentido, devolvem o instante em que terminam.

| Função | O que faz |
|---|---|
| `M.T` | a linha do tempo mestre (GSAP); use para tweens próprios com `M.T.fromTo(...)` |
| `M.sceneIn(sel, t)` | entrada de cena: desliza da direita, desfoca → nítido, com varredura de linhas |
| `M.sceneOut(sel, t)` | saída de cena com echo trail para a esquerda |
| `M.headIn(scope, t)` | eyebrow + headline palavra por palavra + subtítulo |
| `M.words(sel, t, stagger)` | revela palavras de qualquer elemento com `data-split` |
| `M.count(el, valor, t, dur, casas)` | contador numérico formatado no locale |
| `M.countAll(scope, t, dur, stagger)` | conta todos os `[data-n]` do escopo (`data-dec` = casas) |
| `M.type(el, texto, t, dur)` | digitação caractere a caractere |
| `M.clickOn(el, t, origem)` | leva o cursor até o centro do elemento e clica; devolve o instante do clique |
| `M.cursorPath(pontos, t)`, `M.click(x, y, t)`, `M.cursorOut(t)` | controle fino do cursor |
| `M.echoTo(alvo, vars, t)` | qualquer movimento com echo trail (cópias atrasadas e esmaecidas) |
| `M.sweep(t, dir)` | varredura de linhas verticais (cobre trocas de cena) |
| `M.outVars()` | variáveis padrão de saída (para `echoTo` em partes de uma cena) |
| `M.layoutPos(el)` | posição de layout no palco, sem transforms (para mirar o cursor) |
| `M.rectInStage(el)` | retângulo visual no palco, com transforms (para uso em tempo de execução) |
| `M.$`, `M.$$`, `M.fmt` | seletores e formatação numérica |

Marcação de texto: `data-split` no elemento ativa a revelação por palavra; "|" quebra a linha;
`data-dim-first="N"` deixa as N primeiras palavras em cinza.

## 6. Chrome, marca, receitas e tipos de motion

- `M.chrome.in(t)`, `M.chrome.out(t)`, `M.chrome.progress(i, início, fim)` — a barra da seção `i` enche
  linearmente entre os dois instantes e o rótulo acende.
- `M.brand.intro(t)` — linha que se recolhe, símbolo gira até o lugar, nome revelado por máscara,
  legenda; sai com echo. Devolve o instante de entrada da primeira cena (t + 2,95 s).
- `M.brand.outro(t, { sources, hide, hold, fade })` — partículas nascem dos elementos devolvidos por
  `sources()` (normalmente as barras da última cena), convergem para o símbolo, que encolhe até o logo
  completo; nome e tagline entram. Dura 5,6 s (+ `hold`). `fade: false` termina congelado no logo.
- `M.recipes` — uma receita por componente, todas com assinatura `(escopo, t, opções)`:
  `phone`, `floatCard`, `searchList`, `leaderboard`, `pipeline`, `terminal`, `segmentedBars`,
  `dissolveToBars`, além das genéricas `rise` e `bars`. Cada receita lê os dados do próprio HTML.
- `M.types` — tipos de motion que servem a qualquer elemento, com a mesma assinatura `(seletor, t, opções)`:
  `maskReveal`, `iris`, `drawLine`, `highlight`, `float3d`, `morph`, `parallax`, `cameraPush`. Opções,
  marcação exigida e conflitos em `references/tipos-de-motion.md`.

## 7. Regras de construção da linha do tempo

- Uma cena = `sceneIn` no início, `sceneOut` 0,2 s antes da próxima `sceneIn`. A sobreposição é o que
  elimina cortes secos.
- Use `fromTo` com estados explícitos. A linha do tempo repete: estados implícitos herdados da volta
  anterior quebram o loop.
- Efeitos que precisam medir a tela em tempo de execução (partículas) entram via `M.T.call`; efeitos que
  só precisam de posição de layout (cursor) usam `M.layoutPos` na hora de compor.
- A soma dos instantes define a duração: a última função (normalmente `M.brand.outro`) determina o fim
  da volta, e é essa duração que o render usa.

## 8. Armadilhas conhecidas (e por que existem)

- **Estilo por id quebra o echo.** As cópias do echo perdem os ids (para não duplicar). Se o elemento
  for posicionado por `#id` no CSS, as cópias aparecem fora do lugar e ficam presas na tela. Estilize por
  classe; ids só para seletores no `scenes.js`.
- **Objeto `vars` compartilhado.** O GSAP anexa estado interno ao objeto de variáveis de um tween de
  timeline. Por isso o `echo` copia só chaves conhecidas e `M.outVars()` devolve sempre um objeto novo.
- **Transform no CSS + yPercent no GSAP.** Um `transform` declarado no CSS é lido como deslocamento em
  px e somado ao `yPercent`. Deixe o estado inicial para o GSAP (`T.set`/`fromTo`), não para o CSS.
- **Nomes de classe genéricos.** Classes como `ghost` colidem com as do runtime; prefira nomes
  descritivos (`target`, `echo-ghost`).
- **Echo como última ação do filme.** As cópias do echo são tweens fora da linha do tempo; se a volta
  termina durante um echo, elas aparecem por cima do primeiro quadro do loop. Termine com `M.brand.outro`
  ou deixe pelo menos 0,3 s depois do último `sceneOut`.
- **Elementos escondidos por `gsap.set` dentro de callbacks** não são revertidos no loop; garanta que a
  cena seja reexibida pela própria `sceneIn` da volta seguinte.
