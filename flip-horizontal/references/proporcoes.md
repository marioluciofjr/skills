# Proporções e composição

## As cinco proporções de destino

| Proporção | Orientação | Valor R (largura ÷ altura) | Canvas do asset | Uso comum |
|---|---|---|---|---|
| 1:1 | Quadrada | 1,00 | canvas-1x1.png (1080 x 1080) | Feed |
| 9:16 | Vertical | 0,5625 | canvas-9x16.png (1080 x 1920) | Stories, Reels, Shorts |
| 3:4 | Vertical | 0,75 | canvas-3x4.png (1080 x 1440) | Feed vertical |
| 4:3 | Horizontal | 1,333 | canvas-4x3.png (1440 x 1080) | Slides antigos, blog |
| 16:9 | Horizontal | 1,778 | canvas-16x9.png (1920 x 1080) | YouTube, slides, banner |

**Origem fora da lista** (ex.: 3:2 = 1,5 ou 2:3 = 0,667): use a proporção real da origem nos cálculos. Se a pessoa usuária pedir "a mesma proporção", use a proporção da lista com o valor R mais próximo (3:2 → 4:3; 2:3 → 3:4).

## Comportamento das ferramentas

- **Gemini (Nano Banana):** gera as cinco proporções. Quando há uma imagem anexada, a saída costuma seguir a proporção da imagem anexada. Por isso, quando a proporção muda, anexe o canvas como segunda imagem (a última). A frase do canvas no prompt diz ao modelo para usar a proporção dele.
- **ChatGPT:** gera 1:1, horizontal 3:2 e vertical 2:3. Para 16:9 ou 4:3, o resultado sai em 3:2; para 9:16 ou 3:4, sai em 2:3. Nesses casos, recorte no Canva para a proporção final. O fundo liso deixa o recorte simples.
- **Canva, Google Flow, Lovart e similares:** escolha a proporção no seletor da ferramenta, quando existir, e mantenha a proporção escrita no prompt.

## Fórmula de composição

Use estes valores da ficha de pose:

- `s` = largura do personagem ÷ altura do personagem, medidas da foto de origem (do topo da cabeça até a borda inferior, incluindo a mão do gesto).
- `R` = valor da proporção de destino (tabela acima).

Cálculo:

1. Comece com o personagem ocupando `h = 0,92` da altura (8% de espaço acima da cabeça).
2. Calcule a fração da largura: `w = s × h ÷ R`.
3. Se `w` for maior que 0,75, fixe `w = 0,75` e recalcule `h = w × R ÷ s`. O espaço acima da cabeça passa a ser `1 − h`.
4. O personagem fica encostado no lado do quadro oposto ao gesto, com cerca de 4% de margem. O espaço verde vazio fica do lado para onde ele aponta.
5. A borda inferior sempre corta o corpo no mesmo ponto da foto de origem.

Arredonde para valores simples no prompt ("about the right 35% of the frame", "the upper third is empty green space").

### Exemplo de cálculo (s = 0,66, personagem da cintura para cima)

| Destino | w (largura ocupada) | Espaço acima da cabeça | Espaço vazio do lado do gesto |
|---|---|---|---|
| 1:1 | cerca de 60% | cerca de 8% | cerca de 35% |
| 9:16 | 75% (limite) | cerca de 36% | cerca de 21% |
| 3:4 | 75% (limite) | cerca de 15% | cerca de 21% |
| 4:3 | cerca de 45% | cerca de 8% | cerca de 51% |
| 16:9 | cerca de 35% | cerca de 8% | cerca de 61% |

## Regras dos pares de conversão

Há dois casos:

- **O quadro fica mais largo** (R de destino maior que R de origem): a largura extra vira espaço verde do lado do gesto. O personagem mantém a altura relativa. Este é o melhor caso para copy space.
- **O quadro fica mais alto** (R de destino menor que R de origem): a altura extra vira espaço verde acima da cabeça. Se o personagem ficar largo demais (`w` acima de 0,75), reduza a escala. Nunca preencha a altura extra com pernas ou partes do corpo que não aparecem na foto. Em formatos verticais, descreva o espaço vazio como "the upper area and the strip on the [lado] of the frame", e o gesto aponta para esse canto superior.

| Par | Ida | Volta |
|---|---|---|
| 1:1 e 9:16 | 1:1 → 9:16: mais alto; reduza a escala, muito espaço acima da cabeça | 9:16 → 1:1: mais largo; o espaço acima da cabeça diminui e sobra largura do lado do gesto |
| 1:1 e 3:4 | 1:1 → 3:4: um pouco mais alto; espaço extra acima da cabeça | 3:4 → 1:1: um pouco mais largo; espaço extra do lado do gesto |
| 1:1 e 4:3 | 1:1 → 4:3: mais largo; espaço extra do lado do gesto | 4:3 → 1:1: mais alto; o espaço do lado do gesto diminui |
| 1:1 e 16:9 | 1:1 → 16:9: bem mais largo; copy space grande do lado do gesto | 16:9 → 1:1: mais alto; o copy space diminui bastante |
| 9:16 e 3:4 | 9:16 → 3:4: mais largo; menos espaço acima da cabeça | 3:4 → 9:16: mais alto; reduza a escala |
| 9:16 e 4:3 | 9:16 → 4:3: muda de vertical para horizontal; personagem cresce e o espaço vai para o lado do gesto | 4:3 → 9:16: muda de horizontal para vertical; reduza a escala e use o espaço acima da cabeça |
| 9:16 e 16:9 | 9:16 → 16:9: muda de vertical para horizontal; copy space grande do lado do gesto | 16:9 → 9:16: muda de horizontal para vertical; personagem ocupa 75% da largura e o terço de cima fica vazio |
| 3:4 e 4:3 | 3:4 → 4:3: mais largo; espaço do lado do gesto | 4:3 → 3:4: mais alto; espaço acima da cabeça |
| 3:4 e 16:9 | 3:4 → 16:9: bem mais largo; copy space grande do lado do gesto | 16:9 → 3:4: mais alto; reduza a escala |
| 4:3 e 16:9 | 4:3 → 16:9: mais largo; mais copy space do lado do gesto | 16:9 → 4:3: um pouco mais alto; menos copy space |

**Mesma proporção na origem e no destino:** o personagem só muda de lado. A composição fica igual à de origem, refletida.

## Frases prontas para a seção How (em inglês)

- Horizontal: "16:9 landscape image. He occupies about the right 35% of the frame, close to the right edge; his head sits near the top with modest headroom; the left 60% of the frame is empty green space."
- Vertical: "9:16 portrait image. He occupies about the right 75% of the frame width and the lower two thirds of its height, with his waist at the bottom edge; the upper third and the narrow strip on the left of the frame are empty green space."
- Canvas: "If a second plain green image is attached, use its exact aspect ratio as the canvas."
