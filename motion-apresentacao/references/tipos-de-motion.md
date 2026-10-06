# Tipos de motion

Quinze formas de movimento que a skill executa. Sete já existem no core (`M.*`) e oito estão em
`scripts/runtime/motion-types.js` (`M.types.*`). Toda função segue a mesma assinatura das receitas:
`(seletor, t, opções)` e devolve o instante em que o movimento principal termina.

Use este arquivo na Etapa 4 (storyboard): para cada cena, escolha **um tipo herói** (o movimento que carrega
a mensagem) e no máximo dois tipos de apoio. Os tempos gerais (leitura, sobreposição de cenas, ritmo) estão
em `boas-praticas-motion.md`; aqui ficam só os parâmetros de cada tipo.

## Sumário
1. Escolha rápida
2. Das categorias de animação web para o vídeo
3. Fichas dos 15 tipos
4. Princípios de animação por trás dos tipos
5. Conflitos entre tipos

## 1. Escolha rápida

| A cena quer comunicar... | Tipo herói | Apoio que combina |
|---|---|---|
| Uma afirmação forte, a tese do filme | Tipografia cinética | Marcador de destaque |
| Um número que impressiona | Contador numérico | Push de câmera |
| Uma revelação, um "por trás de" | Revelação por máscara | Íris |
| Um comando, fórmula ou regra | Digitação | Marcador de destaque (sublinhado) |
| Uma ligação, um caminho, uma anotação | Desenho de traço | Micro-interação de cursor |
| A palavra que importa dentro da frase | Marcador de destaque | Tipografia cinética |
| Um produto ou app como protagonista | Flutuação 3D | Parallax em camadas |
| Algo que se transforma (ideia em produto) | Morphing de forma | Push de câmera |
| Profundidade, ambiente, contexto | Parallax em camadas | Flutuação 3D |
| Foco, close num detalhe | Push de câmera | Contador numérico |
| Troca de assunto | Transição com varredura | Echo trail |
| Mudança de capítulo, foco numa pessoa ou foto | Íris | Revelação por máscara |
| Velocidade, energia na saída | Echo trail | Transição com varredura |
| "O produto em uso", interação | Micro-interação de cursor | Marcador de destaque |
| Fechamento de marca | Partículas que formam o logo | (encerra o filme) |

## 2. Das categorias de animação web para o vídeo

A classificação de animação de interface do Tubik Studio (blog "web animation") separa seis papéis. No vídeo
não existe hover nem carregamento real, mas cada papel tem um equivalente:

| Categoria web | Papel | Equivalente no motion | Tipos |
|---|---|---|---|
| Hero animation | Primeira impressão, tom da marca | Abertura e primeira cena | Flutuação 3D, push de câmera, tipografia cinética |
| Loading animation | Mostrar progresso | Barra do chrome e contadores | Contador numérico, desenho de traço |
| Accent animation | Destacar o que importa, com contenção | Destaque de palavra ou dado | Marcador de destaque |
| Interactive animation | Diálogo com a interface | Simulação de uso do app | Micro-interação de cursor, digitação |
| Hover animation | Confirmar que algo é interativo | Clique visível do cursor | Micro-interação de cursor |
| Special motion effects | Memorabilidade e emoção | Momentos de assinatura | Morphing, parallax, partículas, íris |

Regra herdada do artigo: se o movimento não melhora a compreensão, ele não entra.

## 3. Fichas dos 15 tipos

### Tipografia cinética palavra por palavra

- **O que é:** cada palavra sobe de dentro de uma máscara, em cascata, com leve rotação.
- **Quando usar:** em toda headline. É o movimento-base da skill.
- **Evite:** em textos de mais de 4 palavras por linha, porque a cascata fica lenta.
- **Tempo:** 0,85 s por palavra, `expo.out`, stagger de 0,07 s.
- **Marcação:** `<h1 class="h" data-split>Primeira|segunda linha</h1>` ("|" quebra a linha).
- **Chamada:** `M.headIn('#cena', t)` (eyebrow + headline + subtítulo) ou `M.words('#cena .h', t, 0.07)`.
- **Variação dos prints de referência:** "palavras animadas pelo próprio significado". Quando a palavra pede,
  dê um movimento próprio a ela depois da cascata (ex.: "cresce" com `scale`, "cai" com `y`), via `M.T.fromTo`.

### Revelação por máscara

- **O que é:** o conteúdo é descoberto por uma janela que abre (wipe), sem mudar de lugar.
- **Quando usar:** revelar um bloco de título, uma imagem, um painel; "o que estava escondido".
- **Evite:** no mesmo elemento que já usa morphing ou íris (as três usam `clip-path`).
- **Tempo:** 0,9 s, `expo.inOut`. Com `settle: true`, o conteúdo assenta de 1,06 para 1.
- **Marcação:** qualquer bloco; envolva o título num `div` próprio se ele também tiver `data-split`.
- **Chamada:** `M.types.maskReveal('#cena .bloco', t, { dir: 'left' | 'right' | 'up' | 'down', settle: true })`.

### Contador numérico

- **O que é:** o número corre de zero até o valor exato da fonte, formatado no idioma.
- **Quando usar:** sempre que um número for o dado principal da cena.
- **Evite:** contar números pequenos (até 10), porque a contagem fica sem graça. Mostre-os prontos.
- **Tempo:** 1,2 a 1,6 s, `power3.out`. O número fica parado e legível por pelo menos 1,5 s depois.
- **Marcação:** `<div data-n="8116">0</div>`; casas decimais em `data-dec="2"`.
- **Chamada:** `M.countAll('#cena', t, 1.4, 0.1)` ou `M.count(el, 8116, t, 1.4)`.

### Digitação

- **O que é:** o texto aparece caractere a caractere, como num terminal ou campo de busca.
- **Quando usar:** fórmulas, comandos, termos buscados, prompts.
- **Evite:** em frases longas (mais de ~70 caracteres) ou em headlines.
- **Tempo:** 0,5 a 1,3 s, linear (representa tempo passando).
- **Marcação:** `<span data-type="texto final"></span>` dentro de `terminal.html` ou `search-list.html`.
- **Chamada:** `M.type(el, 'texto', t, 1.0)` (as receitas `terminal` e `searchList` já chamam).

### Íris

- **O que é:** a cena (ou uma foto) se abre num círculo que cresce a partir de um ponto, ou se fecha nele.
- **Quando usar:** mudança de capítulo, entrada de uma pessoa ou de um retrato, foco num ponto do quadro.
- **Evite:** em cenas com pouco conteúdo no centro, porque o círculo só é percebido onde há algo para recortar.
  Funciona melhor com foto, card grande ou fundo próprio da cena.
- **Tempo:** 0,8 s, `power3.inOut`.
- **Marcação:** a própria `.scene` ou uma imagem.
- **Chamada:** `M.types.iris('#cena', t, { at: '30% 50%', mode: 'open' | 'close' })`. Como entrada de cena,
  use no lugar de `M.sceneIn` (nunca os dois na mesma cena).

### Desenho de traço

- **O que é:** linhas e contornos SVG são desenhados do início ao fim.
- **Quando usar:** setas e anotações "à mão", conexões entre etapas, gráficos de linha, molduras.
- **Evite:** em traços muito curtos (menos de 80 px), porque o desenho passa despercebido.
- **Tempo:** 1,2 s por traço, `power2.inOut`, stagger de 0,12 s entre traços.
- **Marcação:** `<svg class="draw" ...><path d="..."/></svg>`; a classe `.draw` tira o preenchimento e arredonda as pontas.
- **Chamada:** `M.types.drawLine('#cena .seta', t, { duration: 1.2, stagger: 0.12 })`.

### Marcador de destaque

- **O que é:** uma barra passa por trás de um trecho e o inverte, ou o sublinha, ou o pinta de cor.
- **Quando usar:** destacar a palavra-chave de uma frase ou um dado dentro de um subtítulo.
- **Evite:** mais de dois destaques por cena. Se tudo se destaca, nada se destaca.
- **Tempo:** 0,6 s, `expo.inOut`; entra depois que o texto já está legível.
- **Marcação:** `<mark class="mk">trecho</mark>`, **fora** de elementos com `data-split` (o split reescreve o HTML
  e apaga a marcação). Para itálico serifado, acrescente `mk-serif`.
- **Chamada:** `M.types.highlight('#cena .sub', t, { style: 'fill' | 'under' | 'ink', color: '#4f7cff' })`.
  O estilo `ink` com `mk-serif` reproduz a "palavra em itálico serifado colorido" dos prints de referência.

### Flutuação 3D

- **O que é:** o objeto paira e gira devagar no espaço, com perspectiva.
- **Quando usar:** celular, card ou produto como protagonista da cena ("iPhone 3D flutuando", "produto girando").
- **Evite:** em elementos que outra receita já anima em `y` ou `rotation` (ex.: `.phone` com `R.phone`).
  Nesse caso, envolva o elemento num `div` e anime o `div`.
- **Tempo:** a duração da cena (4 s), `sine.inOut`; giro de 10 graus e subida de 14 px.
- **Chamada:** `M.types.float3d('#cena .envolve-celular', t, { duration: 4, tilt: 10, lift: 14 })`.

### Morphing de forma

- **O que é:** um elemento muda de forma: um ponto vira card, uma linha vira painel, uma pílula vira janela.
- **Quando usar:** transformação (ideia vira produto), nascimento de um card, a "linha que vira pílula" dos prints.
- **Evite:** no mesmo elemento que usa máscara ou íris.
- **Tempo:** 0,9 s, `expo.inOut`.
- **Formas prontas:** `dot`, `line`, `column`, `pill`, `card`, ou qualquer string `inset(a% b% c% d% round Npx)`.
- **Chamada:** `M.types.morph('#cena .card', t, { from: 'line', to: 'card', radius: 28 })`.

### Parallax em camadas

- **O que é:** camadas andam em velocidades diferentes conforme a profundidade, criando sensação de espaço.
- **Quando usar:** cenas de ambiente, fundo com formas, produto com elementos ao redor.
- **Evite:** com texto nas camadas, porque texto em movimento contínuo é difícil de ler.
- **Tempo:** a duração da cena, linear (é movimento de câmera contínuo); 120 px de deslocamento na profundidade 1.
- **Marcação:** `data-depth="0.2"` (fundo) até `data-depth="1"` (frente).
- **Chamada:** `M.types.parallax('#cena', t, { duration: 4, distance: 120, axis: 'x' | 'y' })`.

### Push de câmera

- **O que é:** aproximação (ou afastamento) lenta de todo o conteúdo, como uma câmera andando.
- **Quando usar:** dar peso a um número, "close nos detalhes", "zoom na tela" do app.
- **Evite:** escala acima de 1,12, porque o conteúdo encosta nas bordas e a área segura se perde.
- **Tempo:** a duração da cena, `power1.inOut`.
- **Marcação:** envolva o conteúdo da cena em `<div class="cam">` (a `.scene` já é animada por entrada e saída).
- **Chamada:** `M.types.cameraPush('#cena .cam', t, { to: 1.08 })`; para afastar, `{ from: 1.1, to: 1 }`.

### Transição com varredura e desfoque

- **O que é:** a cena entra da direita com desfoque enquanto linhas verticais cruzam o quadro e escondem a emenda.
- **Quando usar:** em toda troca de cena (é o padrão da skill).
- **Evite:** cortes secos ou fades para preto no meio do filme.
- **Tempo:** 0,65 s de entrada, `expo.out`; a saída da cena anterior começa 0,2 s antes.
- **Chamada:** `M.sceneIn('#cena', t)` (já chama `M.sweep`); `M.sweep(t, -1)` inverte o sentido.

### Echo trail

- **O que é:** quatro cópias esmaecidas seguem o elemento com atraso, como um rastro de velocidade.
- **Quando usar:** saídas de cena, saída do logo na abertura, "transições rápidas com motion blur e echo trail".
- **Evite:** em entradas e movimentos lentos (vira borrão). **Nunca como última ação do filme:** as cópias são
  tweens fora da linha do tempo e atravessam o fim do loop, aparecendo por cima do primeiro quadro.
- **Tempo:** cópias com 0,05 s de atraso e opacidade 55%, 34%, 20% e 10%.
- **Chamada:** `M.sceneOut('#cena', t)` ou `M.echoTo(el, M.outVars(), t)` para qualquer elemento.

### Micro-interação de cursor

- **O que é:** o cursor vai até um elemento, clica com uma onda e sai do quadro.
- **Quando usar:** simular o app em uso: trocar aba, clicar em "Seguir", abrir um card.
- **Evite:** deixar o cursor parado em cima de um dado ou usar mais de um clique por cena.
- **Tempo:** 0,55 s por trecho, `power3.inOut`; clique com escala 0,82.
- **Chamada:** `var tc = M.clickOn('#cena .botao', t)` (devolve o instante do clique) e depois `M.cursorOut(tc + 0.4)`.

### Partículas que formam o logo

- **O que é:** elementos da última cena viram partículas que convergem em curva e formam o símbolo da marca.
- **Quando usar:** no encerramento, sempre a partir de algo que já estava na tela (barras, pontos, linhas).
  É o equivalente do "pontinho que explode na tela" dos prints, no sentido inverso.
- **Evite:** partículas fora do encerramento.
- **Tempo:** 5,6 s no total (+ `hold`).
- **Chamada:** `M.brand.outro(t, { sources: function () { return M.$$('#ultima .fill'); }, hide: '#ultima' })`.

## 4. Princípios de animação por trás dos tipos

Os 12 princípios clássicos da animação já estão embutidos nos tipos. Saber onde cada um aparece ajuda a
ajustar um movimento que "não convence".

| Princípio | O que significa | Onde aparece na skill |
|---|---|---|
| Comprimir e esticar (squash & stretch) | o objeto se deforma ao acelerar e ao bater | pops com `back.out(2)`; para uma bolinha quicando, combine `scaleY` 0,8 no impacto com `scaleX` 1,2 |
| Antecipação (anticipation) | pequeno movimento contrário antes da ação | saídas com `power3.in` (acumulam antes de sair); recuo de 6 a 10 px antes de um salto |
| Encenação (staging) | um foco por vez | um tipo herói por cena; no máximo 3 focos simultâneos |
| Continuidade e sobreposição (follow-through) | partes chegam em tempos diferentes | stagger das palavras e listas; echo trail |
| Aceleração e desaceleração (slow in, slow out) | nada começa nem para de repente | tabela de easing em `boas-praticas-motion.md` |
| Arcos (arcs) | trajetórias curvas parecem naturais | partículas em curva; desenho de traço em `C` (curva de Bézier) |
| Ação secundária | detalhe que reforça a principal | card flutuante, marcador de destaque, cursor |
| Tempo (timing) | duração define peso e humor | variação de ritmo entre cenas; nada com a mesma duração |
| Exagero | amplificar para ser lido | moderado: rotações e bounces só nos pops pequenos |
| Desenho sólido | volume e perspectiva | flutuação 3D, sombras do kit de UI |
| Apelo | carisma do conjunto | consistência de paleta, tipografia e ritmo |

## 5. Conflitos entre tipos

| Não combine no mesmo elemento | Por quê | Saída |
|---|---|---|
| Máscara, íris e morphing | os três controlam `clip-path` | aplique cada um num elemento diferente |
| Flutuação 3D e receitas com `rise` | os dois animam `y` | envolva o elemento num `div` e anime o `div` |
| Push de câmera e `sceneIn`/`sceneOut` | os dois animam a `.scene` | use o invólucro `.cam` |
| Íris e `sceneIn` | duas entradas para a mesma cena | escolha uma |
| Marcador de destaque e `data-split` | o split reescreve o HTML | destaque no subtítulo, ou headline sem split |
