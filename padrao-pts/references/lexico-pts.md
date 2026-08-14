# Léxico do PZCT-PTS100

Este arquivo dá apoio à regra PTS-6 (léxico comum e um termo por conceito). Ele reúne exemplos que ilustram um princípio — prefira sempre a palavra mais simples e mais comum disponível, sem perder precisão — em vez de listar as 875 palavras aprovadas do ASD-STE100 como um dicionário fechado. Quando a palavra certa não estiver aqui, aplique o mesmo raciocínio dos exemplos.

## Por que um núcleo de vocabulário básico funciona

O Guia Prático do Português Simplificado (Ibict/MCTI, 2023) pesquisou um corpus de 121 textos didáticos do governo brasileiro e concluiu que um núcleo de aproximadamente 2 a 3 mil palavras já cobre a maior parte da comunicação cotidiana — o mesmo vocabulário que uma pessoa aprende até o fim do ensino fundamental. O português não tem uma lista fechada e oficial como o dicionário do ASD-STE100. Aplique sempre o princípio: se existe uma palavra mais simples e igualmente precisa, use-a.

## Vocabulário rebuscado → vocabulário comum

Exemplos citados pelo próprio Guia Ibict como típicos de textos oficiais em português:

| Evite | Prefira |
|---|---|
| beneplácito | aprovação, consentimento |
| perscrutar | investigar, examinar com cuidado |
| ergástulo público | prisão, cadeia |
| destarte, outrossim | por isso, além disso |
| supracitado, retromencionado | citado antes, mencionado acima |
| a fim de que | para que |
| não obstante | mesmo assim, apesar disso |
| concernente a, atinente a | sobre, relacionado a |
| propugnar | defender |
| ínclito, hialino | (raramente necessário — reescreva a frase) |

## Verbo-suporte → verbo pleno (regra PTS-3)

O padrão "realizar/fazer/efetuar/proceder a + substantivo" quase sempre pode virar um único verbo mais direto:

| Evite | Prefira |
|---|---|
| realizar a validação de | validar |
| efetuar o pagamento de | pagar |
| proceder à análise de | analisar |
| fazer a instalação de | instalar |
| dar início a | iniciar, começar |
| promover a atualização de | atualizar |
| levar a cabo | fazer, concluir |
| ter conhecimento de | saber, conhecer |

Atenção: nominalização costuma ser aceitável quando o substantivo nomeia o próprio processo do domínio. "A validação de entrada rejeita CPFs inválidos" está correto — ali, "validação" é o nome do processo. O problema aparece só quando o substantivo substitui um verbo que já existe e diria a mesma coisa mais direto.

## Jargão técnico e jurídico comum, com explicação

Quando o termo técnico for necessário (porque não existe substituto simples, como aconteceu com "coronavírus" e "COVID-19" durante a pandemia, exemplo citado pelo Guia Ibict), explique-o na primeira ocorrência em vez de assumir que o leitor já conhece:

| Termo técnico | Como introduzir na primeira ocorrência |
|---|---|
| onboarding | onboarding (o processo de receber e orientar alguém novo) |
| deploy | deploy (a publicação de uma nova versão do sistema) |
| rollback | rollback (voltar para a versão anterior) |
| SLA | Acordo de Nível de Serviço (SLA) |
| endpoint | endpoint (o endereço que recebe a chamada da API) |

## Palavras-hedge a evitar (regra PTS-5)

"Deveria", "poderia", "pode ser que", "eventualmente" (no sentido de "talvez", um decalque do inglês "eventually") escondem uma incerteza que o texto deveria resolver com um número, um prazo ou uma condição explícita. Ver PTS-5 em `SKILL.md` para o detalhe.

## Como usar este arquivo

1. Ao aplicar PTS-6, procure primeiro aqui um padrão parecido com o trecho que está reescrevendo.
2. Se não encontrar, aplique o princípio: existe uma palavra mais curta, mais comum e igualmente precisa? Se sim, use-a.
3. Nunca troque uma palavra técnica de domínio (o nome real de uma peça, de um conceito jurídico específico, de uma função de sistema) por um sinônimo impreciso só para simplificar — isso muda o sentido, o que a regra PTS-6 não permite.
