# Boas práticas de UI para os mockups

## Sumário
1. Princípios
2. Grid e área segura
3. Tipografia
4. Cor e contraste (P&B)
5. Profundidade e camadas
6. Mockups: janela, celular, cards
7. Dados na tela
8. Ícones
9. Adaptação para outros formatos

## 1. Princípios

- A UI demonstra a frase. Se a headline é “Sobre os líderes”, a tela mostra um ranking de pessoas, não um
  gráfico genérico. Pergunte: que app alguém abriria para responder a essa frase?
- UI plausível, não realista: parece um produto de verdade, mas sem marcas de terceiros, sem logos de
  sistemas operacionais e sem telas copiadas de apps existentes.
- Um componente principal por cena + no máximo um card flutuante.

## 2. Grid e área segura

Palco 1920x1080. Margens laterais de 140 px; área útil horizontal 140–1780. O chrome ocupa y 40–80 (topo)
e y 990–1040 (base); conteúdo entre y 130 e 960.

Layout padrão de cena: coluna de texto em x 140, largura 760, topo y 250; UI à direita a partir de x
900–1260, terminando em 1780. Variações que quebram a monotonia: cena de largura total (headline no topo,
UI em faixa embaixo, como o pipeline) e UI à esquerda com texto à direita.

Unidade de espaçamento: múltiplos de 4 px; respiros internos de 24–36 px nos painéis.

## 3. Tipografia

- Display (headline): sem serifa condensada e geométrica (padrão Inter Tight 700), 120 px, entrelinha
  0,98, espaçamento −0,05 em. Em 9:16 e 1:1, 96 px.
- Texto de apoio: mesma família, 30 px, cinza `g1`.
- Rótulos, números de tabela, URLs: mono (padrão JetBrains Mono) 13–20 px, caixa alta, espaçamento
  0,12–0,18 em.
- Números grandes em UI: display 700, 46–92 px, espaçamento negativo.
- No máximo duas famílias e quatro tamanhos por cena.

## 4. Cor e contraste (P&B)

- Fundo `#000`, superfícies `#0a0a0a`–`#141414`, bordas `#1f1f1f`–`#2e2e2e`, texto primário `#fff`,
  secundário `#9a9a9a`, terciário `#5c5c5c`.
- Para destacar, inverta: card branco com texto preto (notificação, recorde). É o único “acento”.
- Itens a sinalizar (problema, lacuna) usam borda tracejada, não cor.
- Com paleta de marca: troque `fg` ou use a cor só no elemento invertido; mantenha os cinzas.

## 5. Profundidade e camadas

Três camadas: grade sutil de fundo → painel principal (janela/celular) → card flutuante sobrepondo a
borda do painel. Sombras grandes e escuras (60–140 px de desfoque) e um filete luminoso de 1 px no topo
interno do painel. Nada de gradientes coloridos.

## 6. Mockups: janela, celular, cards

- Janela: barra de 56 px com três pontos cinza e um título mono centralizado (“contexto · fonte”).
- Celular: 410x820, cantos 64 px, ilha superior; cabeçalho com nome da tela e um indicador “ao vivo”.
- Cards: cantos 26 px, rótulo mono em cima, número grande, legenda curta embaixo.
- Controle segmentado: pílula branca deslizante; rótulos com `mix-blend-mode: difference` para inverter
  sobre a pílula.
- Cursor: seta branca com contorno preto e sombra; aparece só quando vai interagir.

## 7. Dados na tela

- Uma pergunta por gráfico. Barras horizontais para rankings; verticais para comparar poucos períodos
  com uma meta; números grandes para um único dado.
- Barras com proporção real (data-s = valor / maior valor). Nunca exagere diferenças.
- Rótulo à esquerda, valor à direita, alinhado em fonte mono para os dígitos não “dançarem”.
- Destaque o primeiro colocado (linha realçada, avatar invertido) e sinalize a exceção (tag, tracejado).
- Arredonde para o que se lê em 1 s (742,4k), mas preserve o valor exato quando ele for a notícia
  (183.809).

## 8. Ícones

Traço de 2 px, cantos arredondados, 44 px, sem preenchimento, desenhados como SVG simples no próprio
snippet. Um ícone por nó/etapa, sempre com o mesmo peso de traço.

## 9. Adaptação para outros formatos

- 1:1 (1080x1080): headline em cima (y 140), UI centralizada abaixo com largura máxima de 800 px; chrome
  só com a barra de progresso.
- 9:16 (1080x1920): headline em cima (y 220), UI ocupando y 700–1600, card flutuante sobre a borda
  inferior; margens de 80 px.
- Em qualquer formato, mantenha os mesmos tempos de leitura e a mesma ordem de entrada.
