# O que é o ASD-STE100 (explicação para leigos)

## Quem mantém e desde quando

O ASD-STE100 (Simplified Technical English) é um padrão de escrita mantido pela ASD — a Aerospace, Security and Defence Industries Association of Europe, a associação europeia da indústria aeroespacial e de defesa. A primeira versão saiu em 1986, ainda sob o nome da antiga associação AECMA, o que faz do padrão um projeto de quase quarenta anos de manutenção contínua. A versão mais recente é a Issue 9, de janeiro de 2025. "STE" é uma marca registrada da União Europeia.

## Para que serve

O ASD-STE100 nasceu para escrever manuais técnicos de aviões, navios, veículos militares e equipamentos de defesa — documentos lidos por técnicos de manutenção, muitas vezes sem o inglês como língua materna, num contexto em que uma frase mal escrita pode causar um acidente. O padrão resolve uma pergunta prática: como garantir que duas pessoas diferentes leem exatamente a mesma instrução, sem precisar de uma segunda leitura para entender. Escrever bonito nunca foi o objetivo.

## Como o padrão é organizado

O documento oficial tem 434 páginas e se divide em duas partes:

- **Parte 1 — Regras de escrita**, com 9 seções: palavras, substantivos compostos, verbos, frases, escrita procedimental (instruções passo a passo), escrita descritiva (explicações), avisos de segurança, pontuação/contagem de palavras, e práticas gerais de escrita.
- **Parte 2 — Dicionário controlado**, com exatamente **875 palavras aprovadas** (o próprio documento declara esse número na introdução da Parte 2) — as palavras mais usadas em escrita técnica em inglês, cada uma com um único sentido e uma única classe gramatical aprovados.

Fora do dicionário, o padrão também define 22 categorias de "substantivo técnico" (nomes de peças, sistemas, ferramentas — como "engine" ou "propeller") e 4 categorias de "verbo técnico" (ações específicas de uma área, como "solder" ou "debug"), que podem ser usados mesmo não estando na lista das 875 palavras, porque são o vocabulário próprio do assunto tratado.

## A lógica central, em quatro ideias

1. **Uma palavra, um sentido, uma classe gramatical.** A palavra "close" só pode ser verbo (fechar); para o sentido de "perto", o padrão exige outra palavra ("near"). Isso elimina a ambiguidade de uma palavra servir para duas coisas diferentes.
2. **Frase curta e só uma ideia por vez.** No máximo 20 palavras por frase em texto de instrução (procedimental) e 25 em texto de explicação (descritivo) — limites literais das regras 5.1 e 6.3 do documento oficial.
3. **Voz ativa e formas verbais simples.** Só é permitido usar infinitivo, imperativo, presente simples, passado simples, futuro simples e particípio passado como adjetivo. Formas compostas como "has been tested" ou "is being checked" são proibidas — sempre em favor de "was tested" ou "the operator checks", mais diretas e sem ambiguidade de tempo.
4. **Um substantivo composto tem no máximo três palavras.** Uma sequência como "runway light connection resistance calibration" (5 palavras empilhadas) vira "calibration of the resistance of the runway light connection" — mais longo, mas sem a ambiguidade de não saber qual palavra modifica qual.

## Por que ele não pode ser simplesmente traduzido para o português

O ASD-STE100 resolve problemas específicos do inglês. Boa parte deles não existe em português: a regra de "uma classe gramatical por palavra" é praticamente automática na nossa língua, porque a morfologia portuguesa já separa "óleo" (substantivo) de "lubrificar" (verbo) — o inglês precisa da regra porque "oil" serve para as duas coisas sem mudar de forma. Ao mesmo tempo, o português tem problemas de ambiguidade que o inglês nunca teve motivo para cobrir: sujeito oculto (a terceira pessoa do singular serve para "ele", "ela", "você" e "o sistema" ao mesmo tempo), o "-se" apassivador, e a posição do adjetivo mudando o sentido da frase ("um simples teste" ≠ "um teste simples"). É por isso que o `padrao-pts` não traduz o ASD-STE100 — ele escreve regras próprias para o português, usando a mesma lógica de padrão (regras numeradas, limites objetivos, classificação de texto por tipo), documentadas em `references/conceito-pts.md` e no `SKILL.md` desta skill.

## O que esta skill não faz

Esta skill não reproduz o dicionário de 875 palavras da ASD, que é propriedade registrada da associação — o documento oficial e gratuito está em asd-ste100.org, para quem precisar de conformidade real com o padrão original (por exemplo, para documentação aeroespacial certificada). Esta skill também não afirma, em nenhum momento, ser uma tradução ou uma versão oficial do ASD-STE100 — ela usa a lógica do padrão como inspiração para um padrão próprio, o PZCT-PTS100, feito para o português.
