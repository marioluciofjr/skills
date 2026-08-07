# Exemplos de saída — skill aos-fatos

## Exemplo 1 — resposta completa (12 notícias encontradas)

A resposta é **uma única lista numerada contínua, de 1 a 12** — nunca use `---` entre os itens (isso quebra a lista em blocos separados no Markdown). O comentário e o link ficam indentados (4 espaços) dentro do próprio item numerado, para o Markdown manter tudo vinculado ao número correto:

```
1. **[Título exato da checagem, como publicado no Aos Fatos]**

    Comentário: [até 100 palavras, contextualizando por que esse tema é relevante agora, citando o veredito de forma breve]

    Leia mais no portal Aos Fatos: [https://www.aosfatos.org/noticias/caminho-real-da-materia-1/]

2. **[Título exato da próxima checagem]**

    Comentário: [...]

    Leia mais no portal Aos Fatos: [https://www.aosfatos.org/noticias/caminho-real-da-materia-2/]
```

Continue assim até o item 12. Depois do último item, encerra a resposta com o disclaimer obrigatório (ver seção "Disclaimer" abaixo) — uma única vez, não repetido por item.

### Exemplo real de dois itens preenchidos (note a numeração contínua)

```
1. **É falso que vacina X causa Y, mostra checagem do Aos Fatos**

    Comentário: Esse boato voltou a circular em grupos de WhatsApp durante a campanha de vacinação deste mês, reacendendo um medo antigo sobre efeitos adversos que já foi desmentido por diversas agências de saúde. O Aos Fatos consultou especialistas e dados oficiais do Ministério da Saúde e concluiu que a alegação é falsa — não há qualquer estudo científico que sustente essa relação de causa e efeito.

    Leia mais no portal Aos Fatos: [https://www.aosfatos.org/noticias/e-falso-que-vacina-x-causa-y/]

2. **TSE não anunciou novas urnas eletrônicas para as eleições deste ano**

    Comentário: A desinformação sobre urnas eletrônicas volta a crescer em período eleitoral, alimentando desconfiança no processo de votação mesmo sem qualquer mudança oficial anunciada pelo órgão responsável. O Aos Fatos verificou junto ao TSE e confirmou que não houve anúncio de novo modelo de urna — a informação é falsa.

    Leia mais no portal Aos Fatos: [https://www.aosfatos.org/noticias/tse-novas-urnas-eletronicas-eleicoes/]
```

## Exemplo 2 — menos de 12 resultados encontrados

Quando o filtro escolhido (ex: um canal pouco frequente, ou um ano muito recente) não tiver 12 checagens na página 1, a skill informa isso com transparência antes de listar o que encontrou, mantendo a mesma lista numerada contínua (sem `---`):

```
Encontrei 7 checagens para esse filtro (não há 12 disponíveis nesse recorte). Segue o que foi localizado:

1. **[Título]**

    Comentário: [...]

    Leia mais no portal Aos Fatos: [URL]

...

7. **[Título]**

    Comentário: [...]

    Leia mais no portal Aos Fatos: [URL]
```

Nunca inventar itens extras para "completar" os 12.

### Exemplo 2b — menos de 12 por limite da ferramenta de fetch (não do site)

Essa é uma causa diferente da do Exemplo 2 e a mensagem precisa deixar isso claro — o site tinha os 12, mas a ferramenta de navegação deste ambiente não conseguiu processar todos:

```
O filtro escolhido tem pelo menos 12 checagens disponíveis, mas processei 7 delas — o limite de interações da ferramenta de navegação deste ambiente impediu abrir as demais nesta execução. Segue o que consegui verificar:

1. **[Título]**

    Comentário: [...]

    Leia mais no portal Aos Fatos: [URL]

...

7. **[Título]**

    Comentário: [...]

    Leia mais no portal Aos Fatos: [URL]
```

## Exemplo 3 — busca por palavra-chave livre (Ramo D)

A pessoa descreve o que ouviu; internamente a skill testa até 10 palavras-chave candidatas via `?q=`, **sem desistir na primeira tentativa** — mesmo que as primeiras não retornem nada, continua até juntar 12 itens únicos ou esgotar as 10 tentativas. Isso é invisível para a pessoa usuária — ela só vê o resultado final consolidado.

### Exemplo: descrição sem checagem exata, mas com notícias relacionadas

Pergunta: *"É verdade que a vacina de sarampo tá proibida? /aos-fatos"*

Como veio com descrição já no gatilho, a skill pula direto para o Ramo D (sem mostrar o menu). Palavras-chave testadas em sequência: `vacina de sarampo`, `vacina sarampo proibida`, `sarampo proibido`, `vacina proibida`, `proibição vacina sarampo`, `vacina`, `sarampo`, `vacinas`, `proibição vacina`, `vacina sarampo` — até juntar 12 itens únicos.

```
Não encontrei uma checagem específica sobre "vacina de sarampo proibida", mas localizei 12 checagens relacionadas ao tema (vacinas e sarampo) que podem te interessar:

1. **[Título de uma checagem sobre vacina]**

    Comentário: [...]

    Leia mais no portal Aos Fatos: [URL]

...

12. **[Título de outra checagem relacionada]**

    Comentário: [...]

    Leia mais no portal Aos Fatos: [URL]
```

## Disclaimer obrigatório (incluir sempre, uma única vez, ao final da resposta)

> Esta skill foi criada em coautoria com o Claude Code, no ambiente do Antigravity IDE, com revisão do autor. É uma skill open-source, desenvolvida por iniciativa própria do autor, cuja inspiração surgiu a partir do curso "Jornalismo IA", do ITS Rio.
