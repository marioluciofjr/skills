# Espelhamento anatômico

Este arquivo ensina a ler a pose da foto de origem e a calcular a pose final. A pose final é a imagem refletida: o personagem passa a ser visto como se estivesse diante de um espelho.

## Os dois sistemas de referência

| Sistema | Quem define | Exemplo | Uso no prompt |
|---|---|---|---|
| Lado anatômico | O próprio personagem | "his left hand" | Partes do corpo |
| Lado do quadro | Quem olha a imagem | "the left part of the frame" | Posições na imagem |

Os dois sistemas não coincidem quando o personagem está de frente para a câmera. Por isso o prompt nunca mistura os dois na mesma expressão.

## Como descobrir o lado anatômico

1. **Personagem de frente para a câmera:** o lado anatômico é o inverso do lado do quadro. A mão que aparece no lado direito da imagem é a mão esquerda do personagem.
2. **Personagem de costas:** o lado anatômico é igual ao lado do quadro.
3. **Personagem de perfil ou em três quartos:** descubra qual ombro está mais perto da câmera e aplique a regra 1 ou 2 a partir do tronco.

**Cuidado com braços que cruzam o corpo.** Não decida pela posição da mão. Siga a manga, do ombro até o cotovelo e do cotovelo até o punho. O braço pertence ao ombro de onde ele sai.

- Exemplo: a mão que aponta está no lado direito da imagem, mas a manga desce na diagonal até um cotovelo no lado esquerdo da imagem, embaixo do ombro do lado esquerdo da imagem. Com o personagem de frente, esse é o braço direito dele, que cruza o peito.

## Tabela de troca

Na pose final, cada item troca de lado. O que não está na tabela fica igual (expressão, roupa, cores, ângulo do gesto, inclinação para cima ou para baixo).

| Elemento | Foto de origem (exemplo) | Pose final |
|---|---|---|
| Mão que aponta | right hand | left hand |
| Cotovelo do braço que aponta | right elbow, low at his right side | left elbow, low at his left side |
| Antebraço que cruza o peito | rises across his chest toward his left | rises across his chest toward his right |
| Braço dobrado na cintura | left forearm across the waist | right forearm across the waist |
| Mão que segura o cotovelo | left hand tucked under the right elbow | right hand tucked under the left elbow |
| Braço por cima | right arm over the left forearm | left arm over the right forearm |
| Giro da cabeça | toward the right part of the frame | toward the left part of the frame |
| Olhar | toward the right part of the frame | toward the left part of the frame |
| Inclinação do tronco | leans toward the right part of the frame | leans toward the left part of the frame |
| Perna de apoio / passo | weight on the left leg, stepping toward the right part of the frame | weight on the right leg, stepping toward the left part of the frame |
| Objeto segurado | holds a mug in the right hand | holds the mug in the left hand |
| Posição no quadro | stands in the left part of the frame | stands in the right part of the frame |
| Espaço vazio (copy space) | right part of the frame | left part of the frame |

## Referência rápida de coerência

Para um personagem **de frente para a câmera**, com o braço que aponta **cruzando o peito**:

| Aponta para | Mão que aponta | Cotovelo dessa mão fica em | Personagem fica em |
|---|---|---|---|
| left part of the frame | left hand | right part of his body in the frame | right part of the frame |
| right part of the frame | right hand | left part of his body in the frame | left part of the frame |

Para um personagem **de frente para a câmera**, com o braço que aponta **aberto para o lado** (sem cruzar o peito):

| Aponta para | Mão que aponta |
|---|---|
| left part of the frame | right hand |
| right part of the frame | left hand |

Se a pose final calculada não bater com estas tabelas, refaça a ficha de pose seguindo a manga do ombro ao punho.

## Frases prontas (em inglês)

- Braço que cruza: "His left forearm rises diagonally from his left elbow, which rests low at his left side, up across his chest, so his left hand ends near the center of his chest."
- Gesto: "His index finger is extended and the other fingers are curled, pointing up into the empty green space that fills the left part of the frame, about 30 degrees above horizontal."
- Braço dobrado: "His right forearm lies folded horizontally across his waist, with his right hand tucked under his left elbow to support it."
- Olhar: "His head turns slightly toward the left part of the frame and his eyes glance sideways into the same empty green space his finger points to."
