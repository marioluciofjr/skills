# Princípios da Gestalt

Gestalt é a teoria de como percebemos elementos visuais como grupos. Esta tabela é a fonte dos limiares de G01 a G09.

| ID | Princípio | Lei equivalente | Regra de layout | Regra de motion | Verificação |
|----|-----------|-----------------|-----------------|-----------------|-------------|
| G01 | Proximidade | L01 | Espaço entre grupos de no mínimo 2 vezes o espaço interno do grupo; escala com base 4 ou 8 | Elementos de um grupo entram no mesmo intervalo de tempo | `scripts/escala.py` confirma razão de 2,0 ou mais |
| G02 | Semelhança | L02 | Elementos de mesma função compartilham cor, tamanho e peso; funções diferentes diferem em pelo menos 1 atributo perceptível | Elementos de mesma função usam a mesma animação | Inventário de estilos por função sem variação não documentada |
| G03 | Conectividade uniforme | L03 | Conectores com espessura e cor únicas por tipo de relação | Conectores desenham na direção do fluxo | No máximo 1 estilo de conector por tipo de relação |
| G04 | Região comum | L04 | Grupos delimitados por fundo ou borda; padding interno maior ou igual ao gap entre itens internos | O container anima antes do conteúdo ou junto com o conteúdo | Medição de padding e gap |
| G05 | Prägnanz | L05 | Formas simples; ícones em grade única; silhuetas reconhecíveis em 24 px | Transformações entre formas simples, sem distorção intermediária confusa | Ícones exportados em 24 px continuam identificáveis |
| G06 | Destino comum | L06 | Itens relacionados compartilham alinhamento e direção de leitura | Itens de um grupo usam o mesmo easing, a mesma direção e a mesma duração; defasagem de 20 a 80 ms dentro do grupo; intervalo maior entre grupos do que dentro dos grupos | Tabela de timing por grupo |
| G07 | Continuidade | L07 | No máximo 3 eixos de alinhamento por tela; leitura em Z ou F definida | Trajetórias em curva contínua; sem mudança brusca de direção sem motivo narrativo | Contagem de eixos; revisão da trajetória |
| G08 | Figura-fundo | Exclusivo da gestalt | Contraste figura-fundo de 4,5:1 para texto e 3:1 para elementos gráficos; sobreposição escura ou clara sobre fotos com texto | O fundo anima com menos intensidade que a figura | `scripts/contraste.py` |
| G09 | Fechamento | Exclusivo da gestalt | Use em logotipos e ícones; nunca dependa de fechamento para indicar elemento interativo | Revelações de logotipo podem usar fechamento progressivo | Elementos interativos têm contorno ou fundo completo |

## Termos

- **Padding:** espaço entre a borda de um grupo e o conteúdo do grupo.
- **Gap:** espaço entre os itens de um grupo.
- **Easing:** curva de aceleração de uma animação.
- **Defasagem:** pequeno atraso entre os elementos de um grupo.
- **Fechamento:** a tendência de completar mentalmente uma forma incompleta.
