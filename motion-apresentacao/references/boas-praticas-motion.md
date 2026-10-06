# Boas práticas de motion design

## Sumário
1. Das respostas às decisões
2. Estrutura e mapa de tempo
3. Tempo de leitura
4. Easing e duração
5. Stagger e coreografia dentro da cena
6. Transições sem cortes secos
7. Echo trail
8. Abertura e encerramento de marca
9. Números, cursor e microinterações
10. O que evitar

## 1. Das respostas às decisões

| Resposta | Decisão |
|---|---|
| Público executivo, investidores | Menos cenas (4), mais tempo por dado, UI sóbria (janelas, rankings) |
| Público de produto, marketing, redes | Mais cenas (5–6), ritmo mais rápido, celular e notificações |
| Objetivo "baixar o relatório", "agendar conversa" | Tagline e URL como última imagem; use `hold` de 1–2 s no `outro` |
| Muitos números no material | Uma ideia por cena; o resto vira subtítulo ou fica de fora |
| Sem logo disponível | `extract_logo.py placeholder` e avise a pessoa |
| Paleta da marca | Mantenha fundo escuro e use a cor só em `fg` ou num acento; nunca em todos os elementos |
| 9:16 vertical | Palco 1080x1920; texto em cima, UI embaixo; headline 96px |
| 1:1 quadrado | Palco 1080x1080; headline 96px; UI menor e centralizada |
| Peça única (não loop) | `loop: false` e `fade: false` no `outro` para terminar no logo |
| 15 s | Abertura curta (2 s), 2–3 cenas, encerramento 5 s |
| 60 s | 8–10 cenas ou cenas mais longas (6 s) com dois momentos de UI cada |

## 2. Estrutura e mapa de tempo

Padrão para 30 s (o exemplo segue exatamente isto):

| Bloco | Início | Duração | Conteúdo |
|---|---|---|---|
| Abertura | 0 | 2,95 s | logo se forma, legenda do tema |
| Cena 1–5 | 2,95 | ~4,2 s cada | headline + UI que demonstra a frase |
| Ponte | ~23,75 | 0,65 s | texto sai, janela se dissolve, sobram as barras |
| Encerramento | 24,4 | 5,6 s | partículas → símbolo → logo + tagline → fade |

Fórmula para outra duração: tempo das cenas = duração − 2,95 − 5,6; divida pelo número de cenas.
Cena abaixo de 3,5 s não dá tempo de ler; acima de 6 s pede um segundo momento de UI (troca de aba,
segundo card, destaque).

## 3. Tempo de leitura

- Headline: até 4 palavras, no máximo duas linhas. O olho lê 3–4 palavras por segundo em movimento.
- Subtítulo: até 16 palavras, entra 0,7 s depois da headline.
- Cada número precisa ficar parado e legível por pelo menos 1,5 s depois que o contador termina.
- Não mais que 3 focos de atenção simultâneos por cena (headline, UI, card flutuante).

## 4. Easing e duração

| Movimento | Ease | Duração |
|---|---|---|
| Entrada de cena e de janelas | `expo.out` | 0,65–0,9 s |
| Palavras da headline | `expo.out` | 0,85 s, stagger 0,07 s |
| Saída de cena | `power3.in` | 0,45 s |
| Troca de estado (aba, barras para outra série) | `expo.inOut` | 0,55–0,9 s |
| Contadores | `power3.out` | 1,2–1,6 s |
| Pequenos “pops” (avatar, ícone, tag) | `back.out(2)` | 0,5 s |
| Progresso e trilhos contínuos | `none` | igual ao intervalo |

Regra geral: entradas desaceleram (out), saídas aceleram (in), trocas fazem os dois (inOut). Nada linear,
exceto o que representa tempo passando.

## 5. Stagger e coreografia dentro da cena

Ordem de leitura = ordem de entrada: eyebrow → headline → UI → dados → destaque → subtítulo.
Itens de lista em cascata de 0,07–0,09 s; cards de 0,1–0,14 s. Cada cena deve ter um momento de
“ação” (cursor clica, aba troca, contador dispara, pulso percorre o trilho) para parecer um app em uso,
não um slide.

## 6. Transições sem cortes secos

- A saída da cena atual começa 0,2 s antes da entrada da próxima; as duas convivem nesse intervalo.
- A entrada vem da direita com desfoque e a saída vai para a esquerda com desfoque: o movimento contínuo
  faz parecer uma câmera andando.
- A varredura de linhas cruza o quadro na troca e esconde a emenda.
- Nunca troque de cena com corte direto nem com fade para preto no meio do filme.

## 7. Echo trail

Quatro cópias do elemento seguem o movimento com atraso de 0,05 s cada e opacidade 55%, 34%, 20% e 10%.
Use em: saídas de cena, saída do logo na abertura e no movimento do símbolo grande para o logo final.
Não use em entradas (o elemento ainda está vazio) nem em movimentos lentos (vira borrão).

## 8. Abertura e encerramento de marca

- Abertura: a linha horizontal se recolhe no ponto onde o símbolo nasce; o símbolo gira e foca; o nome é
  revelado por máscara da esquerda para a direita; a legenda dá o tema.
- Encerramento “elementos formam o logo”: as partículas devem nascer de algo que estava na tela
  (barras, pontos, linhas) para haver continuidade. Elas convergem em curva, deixam rastro e assentam no
  símbolo, que então ganha forma sólida, encolhe para o logo completo e a tagline entra palavra por
  palavra.

## 9. Números, cursor e microinterações

- Contadores sempre terminam no valor exato da fonte, com a formatação do idioma.
- O cursor percorre em 0,55 s com `power3.inOut`, clica com escala 0,82 e uma onda; depois sai pela
  borda. Nunca deixe o cursor parado em cima de um dado.
- Destaques (linha realçada, tag “sub-representada”, card de recorde) entram depois que o dado está
  legível, nunca junto.

## 10. O que evitar

- Texto corrido na tela; tudo o que não cabe em headline + subtítulo + UI fica de fora.
- Mais de uma animação “herói” ao mesmo tempo.
- Rotações e bounces exagerados (fora dos pops pequenos).
- Partículas, brilho ou sombras coloridas fora do encerramento.
- Durações iguais para tudo: variação de ritmo é o que dá vida.
