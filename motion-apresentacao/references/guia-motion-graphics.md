# Guia de produção de motion graphics

Como um estúdio de motion leva uma peça do pedido ao arquivo final, e onde cada fase acontece nesta skill.
O SKILL.md diz **o que fazer** em cada etapa; este guia diz **como saber que a fase terminou** e quais erros
evitar antes de passar para a próxima. Tempos, easing e ritmo ficam em `boas-praticas-motion.md`; os
movimentos, em `tipos-de-motion.md`.

## Sumário
1. Visão geral do processo
2. As fases, uma a uma
3. Formatos de peça (roteiros-modelo)
4. Revisões: como receber e aplicar ajustes
5. Erros que custam retrabalho

## 1. Visão geral do processo

Cada fase fecha uma decisão. Mudar uma decisão já fechada custa mais quanto mais tarde acontece: trocar
uma frase no roteiro custa um minuto; trocar depois da animação pede refazer a coreografia da cena.

| Fase | Decisão que fecha | Etapa do SKILL.md | Ferramenta da skill |
|---|---|---|---|
| Briefing | para quem, para quê, o que não pode faltar | 1 | `perguntas-iniciais.md` |
| Roteiro | o que cada cena diz | 2 | leitura do material |
| Direção de arte | como o filme parece | 3 e 5 (`config.json`) | `marca-e-logo.md`, `boas-praticas-ui.md` |
| Storyboard | o que cada cena mostra e como se move | 4 | `catalogo-ui.md`, `tipos-de-motion.md` |
| Styleframe | um quadro final aprovado | 5 e 6 (primeira cena) | `build_motion.py`, `preview_frames.py` |
| Animatic | tempo de todas as cenas | 5 e 7 (bloqueio) | `preview_frames.py --every 1` |
| Animação | movimento final de cada cena | 5 e 7 (polimento) | `scenes.js`, `Motion.recipes`, `Motion.types` |
| Revisão | a peça passa no controle de qualidade | 7 | checklist de `renderizacao-e-qa.md` |
| Render e entrega | arquivos finais | 8 e 9 | `render_mp4.py`, `contact_sheet.py` |

## 2. As fases, uma a uma

### Briefing

- **Entregável:** as 5 respostas da Etapa 1 (público e ação, mensagens-chave, marca, estrutura, entrega).
- **Pronto quando:** dá para escrever numa linha "este filme faz [público] [ação]". Se não der, falta briefing.
- **Erro comum:** começar pelo visual ("quero algo tipo Apple") sem saber a ação esperada do público.

### Roteiro

- **Entregável:** uma tabela com, por cena, a headline (até 4 palavras), o subtítulo (até 16 palavras) e os
  dados exatos que aparecem na UI.
- **Pronto quando:** lido em voz alta, o roteiro conta a história sozinho, sem as imagens; cada cena tem uma
  ideia só; os números batem com a fonte.
- **Erro comum:** colocar todos os dados do material. O roteiro é corte: o que não cabe em headline,
  subtítulo e UI fica de fora.

### Direção de arte

- **Entregável:** `config.json` com tema, fontes e marca; `logo.png` + `logo.json`.
- **Pronto quando:** paleta e fontes estão fechadas e o logo passa na validação de `marca-e-logo.md`.
- **Erro comum:** usar a cor da marca em tudo. A cor entra num acento (destaque, `fg`), o resto fica neutro.

### Storyboard

- **Entregável:** o mapa de tempo da Etapa 4 com as colunas cena, tempo, UI, tipo de motion e dado principal.
- **Pronto quando:** cada cena tem um tipo herói, a UI demonstra a frase e a soma dos tempos fecha a duração.
- **Erro comum:** escolher o mesmo tipo herói para todas as cenas. Alterne para criar ritmo (ex.: contador,
  depois desenho de traço, depois flutuação 3D).

### Styleframe

O styleframe é um quadro parado, já com a cara final, que prova a direção antes de animar o resto.

- **Entregável:** a primeira cena montada no `scenes.html` e um quadro do meio dela capturado com
  `preview_frames.py --times <meio da cena>`.
- **Pronto quando:** hierarquia, grid, fontes e área segura estão corretos nesse quadro
  (`boas-praticas-ui.md`).
- **Erro comum:** animar as cinco cenas e só então descobrir que a fonte, a escala ou a paleta não funciona.

### Animatic

O animatic é o filme inteiro com movimento simples, só para validar o tempo.

- **Entregável:** todas as cenas com só `M.sceneIn`, `M.headIn` e `M.sceneOut` no `scenes.js`, e uma grade
  de `preview_frames.py --every 1`.
- **Pronto quando:** cada headline fica legível pelo tempo mínimo, a ordem das cenas conta a história e a
  duração total bate com o briefing.
- **Erro comum:** pular o animatic e ajustar o tempo depois de tudo animado, quando mover uma cena desloca
  todas as seguintes.

### Animação

- **Entregável:** `scenes.js` completo com receitas de componente, tipos de motion e encerramento de marca.
- **Pronto quando:** cada cena tem um momento de ação (clique, contador, traço, troca de aba), e a última
  cena entrega elementos para as partículas do logo.
- **Ordem de trabalho:** primeiro o tipo herói de cada cena, depois os apoios, por último os detalhes
  (pops, destaques). Revise a grade a cada cena terminada, não só no fim.
- **Erro comum:** empilhar efeitos. Antes de acrescentar um tipo, confira a tabela de conflitos em
  `tipos-de-motion.md`.

### Revisão

- **Entregável:** a grade de `preview_frames.py` com os instantes da lista de `renderizacao-e-qa.md` e todas
  as respostas "sim" no checklist.
- **Pronto quando:** o loop fecha (o quadro após o fim é igual ao início) e não há erros na página.
- **Erro comum:** revisar só o meio das cenas. Os defeitos aparecem nas transições e no encerramento.

### Render e entrega

- **Entregável:** HTML e MP4, conferido com `contact_sheet.py --video`.
- **Pronto quando:** a fonte display carregou (o render avisa se não), o tamanho do arquivo é razoável e a
  grade do vídeo bate com a grade de revisão.
- **Erro comum:** entregar o MP4 com fonte de fallback porque o aviso do render passou despercebido no log.

## 3. Formatos de peça (roteiros-modelo)

Quatro formatos comuns, com a sequência de cenas e os tipos de motion de cada uma. Use como ponto de
partida do storyboard e adapte ao material. Os colchetes indicam o que vem do briefing.

### Lançamento de app (30 s)

Fundo escuro com brilho suave, celular como protagonista, headline com palavra-chave em destaque.

| Cena | Conteúdo | Tipo herói | Apoio |
|---|---|---|---|
| Abertura | logo se forma | (abertura de marca) | echo trail na saída |
| 1 a 5 | [FRASE] + tela do app que demonstra a frase | flutuação 3D do celular | marcador de destaque (`ink`), push de câmera na tela |
| Destaque | cards saltando do celular | micro-interação de cursor | pops (`back.out`) |
| Ponte | celulares lado a lado, em leque | parallax em camadas | transição com varredura |
| Encerramento | logo + [TAGLINE] | partículas que formam o logo | (fim) |

### Produto em destaque (15 s)

Duas cores (acento + quase-preto), tipografia extra bold em caixa alta, transições rápidas.

| Cena | Conteúdo | Tipo herói | Apoio |
|---|---|---|---|
| 1 | um ponto aparece e se abre | morphing de forma (`dot` para `card`) | íris |
| 2 | [FRASE 1] + close no detalhe do produto | push de câmera | tipografia cinética |
| 3 | [FRASE 2] com o produto girando | flutuação 3D | echo trail na saída |
| 4 | [BENEFÍCIO 1] e [BENEFÍCIO 2] em cards ao redor | parallax em camadas | desenho de traço ligando cards ao produto |
| 5 | [PALAVRA 1] [PALAVRA 2] [PALAVRA 3] | tipografia cinética | transição com varredura |
| Encerramento | logo + [TAGLINE] | partículas que formam o logo | (fim) |

### Apresentação pessoal (15 s)

Fundo escuro alternando com uma cor, uma palavra por frase em itálico serifado colorido, números com contagem.

| Cena | Conteúdo | Tipo herói | Apoio |
|---|---|---|---|
| 1 | uma linha vira pílula e forma uma letra do [NOME] | morphing de forma (`line` para `pill`) | revelação por máscara do nome |
| 2 | foto em círculo + [FRASE DE IMPACTO] | íris na foto | marcador de destaque (`ink` + `mk-serif`) |
| 3 | [DESTAQUE 1], [DESTAQUE 2] e [DESTAQUE 3] com infográficos | contador numérico | desenho de traço |
| Encerramento | foto + [NOME] + botão "Seguir" sendo clicado | micro-interação de cursor | revelação por máscara |

### Showreel didático (15 s)

Peça que ensina princípios de animação. Fundo cinza-gelo alternando com grafite, anotações manuscritas.

| Cena | Conteúdo | Tipo herói | Apoio |
|---|---|---|---|
| 1 | bolinha quicando com rastro, que vira o ponto final da frase de abertura | echo trail + comprimir e esticar | morphing de forma |
| 2 | palavras animadas pelo próprio significado | tipografia cinética (variação semântica) | marcador de destaque |
| 3 | gráfico de easing (linear x ease-in-out) | desenho de traço | anotação com seta (desenho de traço) |
| 4 | cobrinha de pontos num grid (continuidade) | desenho de traço em `polyline` | stagger nos pontos |
| 5 | dial carregando até 100% (antecipação) | contador numérico | desenho de traço no arco do dial |
| Encerramento | [CARGO] / [NOME] + nota manuscrita [CTA] | revelação por máscara | desenho de traço |

Para tema de fundo luminoso, inverta o `theme` do `config.json` (`bg` em tom alto, `fg` escuro). Os componentes de UI foram
desenhados para fundo escuro, então revise contraste e sombras no styleframe.

## 4. Revisões: como receber e aplicar ajustes

- **Classifique o pedido pela fase que ele reabre.** "Troca essa frase" reabre o roteiro; "a cor está forte"
  reabre a direção de arte; "está rápido" reabre o animatic. Volte à fase, ajuste e refaça só as fases seguintes
  afetadas.
- **Ajuste de tempo:** mude os instantes no `scenes.js` a partir da cena alterada e confira as sobreposições
  de 0,2 s. Tudo o que vem depois anda junto.
- **Ajuste de texto:** confira se a headline continua em até duas linhas e se o tempo de leitura ainda cabe.
- **Uma rodada de cada vez:** junte os pedidos, aplique todos, gere a grade e só então renderize de novo
  (o render é a etapa mais cara).

## 5. Erros que custam retrabalho

| Erro | Fase que deveria ter evitado | Como evitar |
|---|---|---|
| Dado errado descoberto no vídeo final | roteiro | copiar números exatamente da fonte e conferir na tabela do roteiro |
| Filme bonito que não leva à ação | briefing | escrever a linha "este filme faz [público] [ação]" antes de tudo |
| Cenas com a mesma cara e o mesmo ritmo | storyboard | alternar tipos herói e UIs entre cenas |
| Fonte ou escala errada em todas as cenas | styleframe | aprovar um quadro antes de montar as outras cenas |
| Tempo apertado para ler | animatic | grade a cada 1 s antes de animar os detalhes |
| Efeitos brigando no mesmo elemento | animação | tabela de conflitos de `tipos-de-motion.md` |
| Resto de cena no primeiro quadro do loop | revisão | capturar o instante logo após o fim da volta |
