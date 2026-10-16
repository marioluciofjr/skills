# Exemplo completo

Foto de origem: homem de barba em estúdio com fundo laranja, 800 x 534 pixels (proporção 3:2). Pedido: o personagem deve apontar para o outro lado, em 16:9.

## Ficha de pose (análise interna)

- **Atributos:** cabelo castanho-avermelhado bagunçado, barba cheia castanho-avermelhada com bigode, sorriso de canto com a boca fechada, sobrancelha levemente erguida, camisa social azul-clara de manga comprida com botões brancos pequenos e punhos longos.
- **Braço do gesto:** braço direito. A manga desce do ombro direito (lado esquerdo da imagem) até o cotovelo, embaixo, do lado direito do corpo. O antebraço sobe na diagonal pela frente do peito, e a mão direita termina no centro do peito.
- **Gesto:** indicador estendido, demais dedos dobrados, apontando para o espaço vazio no lado direito do quadro, cerca de 30 graus acima da horizontal.
- **Outro braço:** antebraço esquerdo dobrado na horizontal sobre a cintura; a mão esquerda fica embaixo do cotovelo direito, segurando-o.
- **Cabeça e olhar:** cabeça levemente girada para o lado direito do quadro; olhos de canto para o mesmo lado.
- **Enquadramento:** da cintura para cima; a borda inferior corta na cintura; pouco espaço acima da cabeça.
- **Posição:** personagem na parte esquerda do quadro; espaço vazio na parte direita.
- **s:** cerca de 0,66.

## Pose final (depois da tabela de troca)

- Braço do gesto: braço **esquerdo**, cotovelo embaixo do lado esquerdo do corpo, antebraço subindo pela frente do peito, mão esquerda no centro do peito.
- Gesto: aponta para o espaço vazio na parte **esquerda** do quadro, cerca de 30 graus acima da horizontal.
- Outro braço: antebraço **direito** na cintura, mão direita embaixo do cotovelo esquerdo.
- Cabeça e olhar: para a parte **esquerda** do quadro.
- Posição: personagem na parte **direita** do quadro.

## Composição em 16:9

`w = 0,66 × 0,92 ÷ 1,778 ≈ 0,34`. O personagem ocupa cerca de 35% da largura, encostado na direita. O espaço vazio ocupa cerca de 60% da largura, à esquerda.

## Saída da skill

Reforço opcional: anexe também assets/canvas-16x9.png como segunda imagem (a última anexada).

```text
Who: Use the attached image as the reference photo for this person; it is the first attached image, and a second plain green image may follow. The person is the exact same bearded man from the reference photo, not a lookalike: light skin, an oval face, thick eyebrows, a straight nose, tousled reddish-brown hair, a full reddish-brown beard and mustache, a sly closed-mouth smirk with one eyebrow slightly raised, and a light blue long-sleeved button-up shirt with small white buttons and long buttoned cuffs. Keep his face, identity, hair, beard, expression, skin tone, shirt color, fabric, and body proportions exactly as in the reference photo; only the pose and the backdrop are new.

What: A new studio photo of this man standing in the right part of the frame, posed as follows. His left forearm rises diagonally from his left elbow, which rests low at his left side, up across his chest, so his left hand ends near the center of his chest. His left index finger is extended and the other fingers are curled, pointing up into the empty green space that fills the left part of the frame, about 30 degrees above horizontal. His right forearm lies folded horizontally across his waist, with his right hand tucked under his left elbow to support it. His head turns slightly toward the left part of the frame and his eyes glance sideways into the same empty green space his finger points to. Exactly two arms and two hands, five fingers on each hand, each arm continuous from shoulder to elbow to wrist, sleeves and cuffs matching the reference shirt. No extra or missing limbs or fingers, no fused fingers, no disconnected wrists, no second person.

Where: A flat, seamless chroma key green (#00B140) backdrop filling the entire frame behind him, evenly lit, with no gradient, no shadow, no texture, no floor line, no props, and no text. The large empty green area fills the left part of the frame. No green reflections or spill on his skin, hair, beard, or shirt; clean, crisp edges around his hair and beard for easy keying.

How: Photorealistic studio portrait, frontal eye-level camera, waist-up framing with the bottom edge cutting at his waist as in the reference photo, soft diffused frontal lighting, natural warm skin tones, the same light blue shirt color. 16:9 landscape image. He occupies about the right 35% of the frame, close to the right edge; his head sits near the top with modest headroom; the left 60% of the frame is empty green space. If a second plain green image is attached, use its exact aspect ratio as the canvas. Sharp focus, no watermark, no text.
```

## Variação: mesma foto em 9:16

Só a seção `How` muda. Cálculo: `w = 0,66 × 0,92 ÷ 0,5625 ≈ 1,08`, acima do limite. Então `w = 0,75` e `h = 0,75 × 0,5625 ÷ 0,66 ≈ 0,64`.

```text
How: Photorealistic studio portrait, frontal eye-level camera, waist-up framing with the bottom edge cutting at his waist as in the reference photo, soft diffused frontal lighting, natural warm skin tones, the same light blue shirt color. 9:16 portrait image. He occupies about the right 75% of the frame width and the lower two thirds of its height, with his waist at the bottom edge; the upper third and the narrow strip on the left of the frame are empty green space, and his finger points up toward that empty upper-left area. If a second plain green image is attached, use its exact aspect ratio as the canvas. Sharp focus, no watermark, no text.
```

## Por que este prompt funciona

- Nenhuma palavra pede inversão, e a pose de origem não aparece no texto.
- A direção está travada de três formas: o personagem fica na parte direita do quadro, o dedo aponta para o espaço verde da esquerda e a mão anatômica é a esquerda. O olhar confirma.
- O fundo verde obriga a IA a gerar a imagem inteira de novo, então ela não devolve a foto de entrada.
- A borda inferior fica na cintura, então a IA não inventa pernas para preencher o quadro.
