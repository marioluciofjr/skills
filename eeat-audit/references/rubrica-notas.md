# Rubrica de Notas E-E-A-T (0 a 5)

Este documento define a escala de julgamento da skill. Leia-o antes de atribuir qualquer nota.

## Índice

1. Âncoras gerais da escala
2. Âncoras por pilar
3. Sete regras antiinflação
4. Cálculo da nota global ponderada
5. Trava YMYL
6. Leitura da nota global

---

## 1. Âncoras gerais da escala

A escala mede a força da evidência presente no texto ou na página. Ela não mede a intenção do autor nem o potencial do conteúdo.

| Nota | Nível | Critério de evidência |
|---|---|---|
| 0 | Ausente | Nenhuma evidência no texto. Ou evidência falsa, enganosa ou contraditória. |
| 1 | Crítico | Menção incidental, sem qualquer sustentação verificável. |
| 2 | Insuficiente | Evidência genérica, reproduzível por qualquer terceiro sem acesso ao objeto. |
| 3 | Mínimo aceitável | Evidência presente e verificável, porém rasa ou parcial. |
| 4 | Sólido | Evidência específica, verificável e coerente ao longo de todo o texto. |
| 5 | Referência | Evidência original e auditável na fonte primária, que terceiros não reproduzem. |

A fronteira entre 2 e 3 é a verificabilidade. A fronteira entre 4 e 5 é a originalidade.

---

## 2. Âncoras por pilar

Use estas âncoras para posicionar a nota. Elas descrevem os extremos operacionais de cada pilar.

### Experiência (peso 1)

| Nota | Descrição observável |
|---|---|
| 0 | O texto não indica qualquer contato do autor com o objeto tratado. |
| 1 | O texto usa a primeira pessoa sem descrever uso, teste ou vivência concreta. |
| 2 | O texto descreve o objeto a partir do manual, da página do fabricante ou de resumo de terceiros. |
| 3 | O texto relata uso real, sem método declarado e sem registro visual próprio. |
| 4 | O texto relata uso real com contexto específico: duração, condições e resultado observado. |
| 5 | O texto publica método de teste próprio, registro visual original e limitações encontradas. |

### Especialidade (peso 1)

| Nota | Descrição observável |
|---|---|
| 0 | O texto contém erro conceitual básico do domínio. |
| 1 | O texto usa jargão de forma imprecisa e não identifica o autor. |
| 2 | O texto usa a terminologia correta, sem autoria identificada e sem profundidade. |
| 3 | O texto identifica o autor e explica o tema com correção, sem credencial verificável. |
| 4 | O autor tem biografia com credencial verificável e o texto trata nuances do tema. |
| 5 | O autor tem credencial verificável no tópico específico e o texto declara revisão técnica nominal. |

### Autoridade (peso 2)

Este pilar tem o dobro do peso dos demais no cálculo da nota global. Aplique atenção proporcional na coleta de evidência.

| Nota | Descrição observável |
|---|---|
| 0 | O texto não cita nenhuma fonte externa. |
| 1 | O texto cita fonte externa sem link, sem autoria e sem data. |
| 2 | O texto cita blogs comerciais do próprio segmento ou agregadores de conteúdo. |
| 3 | O texto cita fonte externa qualificada com link ativo, sem dado próprio. |
| 4 | O texto cita fonte primária reconhecida no nicho e a publicação tem histórico no tema. |
| 5 | O texto cita fonte primária e apresenta dado proprietário produzido pela própria organização. |

### Confiabilidade (peso 1)

| Nota | Descrição observável |
|---|---|
| 0 | O texto contém afirmação factual incorreta, ou omite autoria e data por completo. |
| 1 | O texto tem autoria genérica, do tipo "equipe editorial", sem data e sem fonte. |
| 2 | O texto tem autoria e data de publicação, sem qualquer link de comprovação. |
| 3 | O texto tem autoria, data e alguns links de comprovação ativos, com cobertura parcial das afirmações. |
| 4 | Toda afirmação factual leva a uma fonte ativa. O texto declara a data da última revisão. |
| 5 | O item 4 mais transparência de conflito de interesse, política editorial e canal de correção. |

---

## 3. Sete regras antiinflação

Sem estas regras, a nota deriva para cima a cada execução.

1. **Pontue apenas evidência presente.** Não infira credencial, fonte ou intenção não declarada no texto ou na página.
2. **Na dúvida, atribua a menor.** Quando duas notas parecerem defensáveis, escolha a menor e explique por que a nota maior não se sustenta.
3. **Teto 3 sem elemento externo.** Limite qualquer pilar a 3 quando faltar elemento externo verificável: link ativo, dado, biografia de autor ou data de revisão.
4. **Nota 5 exige irreprodutibilidade.** Atribua 5 apenas quando o texto contiver elemento que terceiros não reproduzam sem acesso direto ao objeto: dado proprietário, imagem original, método próprio ou credencial nominal.
5. **Proibida a compensação entre pilares.** Uma Experiência forte não eleva a Confiabilidade. Avalie cada pilar de forma isolada.
6. **Apenas números inteiros.** Não use 3,5 nem intervalos. A nota global é o único valor decimal do diagnóstico.
7. **Tolerância zero em YMYL.** Em conteúdo YMYL, limite a Confiabilidade a 2 quando qualquer afirmação factual não tiver fonte primária.

---

## 4. Cálculo da nota global ponderada

```
Nota Global = (Experiência × 1 + Especialidade × 1 + Autoridade × 2 + Confiabilidade × 1) / 5
```

Pesos: Experiência 1, Especialidade 1, Autoridade 2, Confiabilidade 1. Soma dos pesos: 5.

Arredonde o resultado a uma casa decimal.

**Exemplo de cálculo**

Um artigo recebe Experiência 4, Especialidade 3, Autoridade 1 e Confiabilidade 3.

```
(4 × 1 + 3 × 1 + 1 × 2 + 3 × 1) / 5
= (4 + 3 + 2 + 3) / 5
= 12 / 5
= 2,4
```

**Consequência operacional do peso.** Um ponto ganho em Autoridade move a nota global 0,4. Um ponto ganho em qualquer outro pilar move 0,2. No exemplo acima, elevar a Autoridade de 1 para 3 leva a nota global a 3,2. Elevar a Especialidade de 3 para 5 leva a 2,8. Use esse cálculo para ordenar o plano de ação por impacto, e não apenas por gravidade.

---

## 5. Trava YMYL

Em conteúdo YMYL com Confiabilidade 0 ou 1, a nota global não passa de 2,0, qualquer que seja o resultado da média.

A trava existe porque o peso 1 da Confiabilidade não reflete o risco real desse tipo de conteúdo. Um artigo de saúde com autoridade alta e confiabilidade nula causa dano ao leitor. Declare a aplicação da trava no diagnóstico sempre que ela alterar o resultado.

---

## 6. Leitura da nota global

| Faixa | Veredito | Encaminhamento |
|---|---|---|
| 0,0 a 1,4 | Reprovado | Reescreva o conteúdo. A correção pontual não recupera o texto. |
| 1,5 a 2,4 | Insuficiente | Corrija os pilares críticos antes de manter a página publicada. |
| 2,5 a 3,4 | Aceitável com ressalvas | Publique com as correções do plano de ação aplicadas. |
| 3,5 a 4,4 | Sólido | Aplique os ajustes de refinamento. O conteúdo compete no nicho. |
| 4,5 a 5,0 | Referência | Mantenha o padrão. Use o conteúdo como modelo interno. |

Declare a faixa junto com o número. O número mede, a faixa comunica.
