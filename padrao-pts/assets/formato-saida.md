# Formato de saída do padrao-pts

Este template vale para o modo padrão da skill (quando a pessoa usuária cola um texto de referência para reescrever). Os modos "regras" e "conceito" têm saída própria, descrita em `SKILL.md`.

Toda reescrita em PZCT-PTS100 segue esta estrutura. Se nenhuma regra for violada, pule direto para "Texto final" com uma frase curta dizendo que o texto já está conforme — não force um relatório de mudanças que não existem.

```markdown
- **Destinatário:** [humano | IA generativa]
- **Critério lusófono:** português - [Brasil, padrão | outro país, se a pessoa usuária declarou]

| Regra | Original | Reescrito |
|---|---|---|
| PTS-N (nome curto da regra) | "trecho original entre aspas" | "trecho reescrito" |
| ... | ... | ... |

## Texto final

[texto completo reescrito, formatado em markdown — títulos, listas ou tabelas quando o conteúdo pedir (regra PTS-9). Nunca amontoe o texto final num único parágrafo corrido: isso prejudica a leitura e vai contra o objetivo de acessibilidade da skill.]

**Variante lusófona aplicada:** [preencha só se a pessoa usuária pediu uma variante diferente do português do Brasil — qual país, quais termos trocados. Omita esta linha quando a saída for em português do Brasil, o padrão.]

**Mantido de propósito:** [o que não foi simplificado e por quê — ex.: uma condição de segurança que ficaria mais longa mas não pode ser cortada]

**Lembrete:** revise este texto antes de publicar — o PZCT-PTS100 organiza a escrita, mas não substitui a sua revisão final.
```

## Regras de preenchimento

- Cite sempre o trecho original entre aspas, na íntegra — nunca parafraseie a "coluna Original" da tabela.
- Uma linha da tabela por trecho reescrito, não por regra — se uma frase violar duas regras, use duas linhas ou combine-as de forma explícita na mesma linha.
- O "Texto final" segue a estrutura do conteúdo original: passos viram lista numerada, itens viram lista com marcadores, seções longas ganham subtítulo. Só fica em parágrafo corrido quando o próprio conteúdo é mesmo um parágrafo corrido no original.
- A linha "Mantido de propósito" é obrigatória sempre que uma frase ficar mais longa do que o limite da PTS-2 para preservar uma condição, exceção ou informação de segurança.
- O lembrete de revisão humana aparece sempre, mesmo em textos curtos.
