# Marca e logo

O motion usa o logo como silhueta de uma cor (branca no padrão P&B) sobre transparente. Isso permite
recortar símbolo e nome com máscaras, girar o símbolo na abertura e amostrar a forma para as partículas.

## Onde buscar o logo (ordem de preferência)

1. **Arquivo enviado pela pessoa** (PNG, SVG, JPG) → `extract_logo.py image`.
2. **PDF do próprio material** (capa, contracapa, rodapé). Logos em PDF costumam ser vetoriais e saem
   perfeitos em 1200 dpi → `extract_logo.py page` para localizar e `extract_logo.py pdf` para recortar.
3. **Site da marca**: busque a URL do arquivo do logo (cabeçalho, og:image, favicon). Se o download for
   bloqueado pelo ambiente, peça o arquivo à pessoa ou volte para a opção 2.
4. **Sem logo**: `extract_logo.py placeholder --text "Nome"` e avise que é provisório.

## Como recortar de um PDF

1. Renderize a página em 72 dpi com o subcomando `page`; nessa resolução 1 px = 1 pt.
2. Abra a imagem, identifique o retângulo do logo e anote x, y, largura e altura em pt (origem no canto
   superior esquerdo). Deixe 2–4 pt de folga, sem encostar em outros elementos.
3. Rode o subcomando `pdf` com `--bbox x,y,largura,altura`.
4. Confira a saída sobre um fundo cinza: nada cortado, nada sobrando (ex.: pedaço de outro logo).

## O logo.json

- `aspect`: largura ÷ altura do PNG.
- `mark_end`: fração da largura onde termina o símbolo.
- `word_start`: fração onde começa o nome.

A detecção procura o maior vão vertical depois de um bloco que ocupe até 45% da largura. Confira:
símbolos com partes soltas (pontos, traços) podem enganar a detecção. Se precisar, corrija os valores
à mão no `logo.json` ou sobrescreva no `config.json` (`brand.mark_end`, `brand.word_start`).
Logo só com nome (sem símbolo): `mark_end = word_start = 1`; a abertura gira o logo inteiro e as
partículas formam o logo inteiro.

## Cuidados

- Use a silhueta na cor do texto do tema (`--color` do script). Logos multicoloridos perdem as cores de
  propósito; se a marca exigir as cores originais, avise que o encerramento por partículas fica
  monocromático.
- Não distorça, não aplique contorno, não troque a fonte do nome.
- Logo de terceiros (clientes, parceiros) não entra no motion sem pedido explícito.
