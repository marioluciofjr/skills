# Formato da resposta final

Use este modelo em toda resposta com códigos. Substitua o texto entre colchetes. Não mude a ordem dos blocos.

## Regras do modelo

- Mostre a linha "Verificação de atualização" sempre no topo.
- Na linha "Verificação de atualização", escreva somente o que você fez nesta conversa. Para cada fonte aberta, copie o marcador encontrado nela. Sem fonte aberta, escreva "Abri 0 de [total] fontes oficiais".
- Nunca copie a linha de verificação do exemplo preenchido.
- Se a base estiver vencida, coloque o aviso de base vencida logo abaixo dessa linha.
- Mostre cada um dos cinco códigos num título de nível 3 (###), com o código em negrito. O MEI precisa achar os códigos só de bater o olho.
- Escreva cada "Justificativa" com até 50 palavras, em linguagem simples.
- Escreva cada "O que é" com a explicação curta de `references/glossario.md`.
- Use somente estes valores em "Certeza": Confirmado, Sugerido, Consulte um contador, Confira no Emissor Nacional.
- Em "Fonte", cite o documento oficial com artigo, item ou versão.
- Mostre a NBS nos dois formatos: com pontos e como o Emissor Nacional pede, só com números.
- Quando o campo não deve ser preenchido, escreva "Não preencher" no lugar do código e explique o motivo.
- Quando não houver código seguro, escreva "Não indicado" e explique o motivo.
- Na linha "Preencher IBS/CBS", oriente sempre "Sim". A skill prepara o MEI para a obrigatoriedade de 2027.
- Mostre o bloco "Outros campos da emissão completa" somente com os campos que se aplicam ao caso.
- No bloco "O que entendi do seu serviço", copie as respostas do MEI. Não acrescente hipóteses, nem entre parênteses.
- Mostre sempre o bloco "Atenção" com os dois alertas fixos: cobrança e ocupação.
- Depois dos alertas fixos, mostre no máximo 3 alertas do caso, do maior risco para o menor. Se houver alerta de tabela não conferida, ele é o primeiro dos 3.
- Os demais alertas do caso vão numa única linha final: "Outras observações:", com itens curtos separados por ponto e vírgula.
- Quando um alerta vier de regra marcada na base como [CONFIRMAR NO ANEXO VI/VII], termine o alerta com "(confira no Emissor Nacional)".
- Se você não conferiu na fonte oficial os códigos tirados de `references/tabelas/`, inclua o alerta de tabela não conferida.
- Termine sempre com o aviso final.

## Alertas padronizados

- **Cobrança (fixo):** Considerei que você cobrou pelo serviço. Se você não cobrou, avise, porque o Indicador de Operação muda.
- **Ocupação (fixo):** Confira se este serviço corresponde a uma ocupação do seu CCMEI (Certificado da Condição de Microempreendedor Individual). Se não corresponder, consulte um contador.
- **Tabela não conferida:** O Código de Tributação Nacional e a NBS vieram de cópias das tabelas oficiais feitas em [data de `tabelas_incorporadas` no manifesto]. Não consegui conferir se esses códigos continuam iguais. Confira no Emissor Nacional antes de emitir a nota.

## Modelo

```markdown
**Verificação de atualização:** [Base atualizada | Mudança em fonte oficial | Não foi possível verificar] em [data de hoje por extenso]. Abri [n] de [total] fontes oficiais. [Para cada fonte aberta: nome curto da fonte: "marcador encontrado".] Base revisada em [data de `ultima_verificacao_em` por extenso].

**O que entendi do seu serviço**
- Serviço: [descrição curta]
- Como foi feito: [pessoalmente | à distância | parte pessoalmente e parte à distância]
- Quem pagou: [Brasil | país]
- Quem usou o serviço: [a mesma pessoa que pagou | outra pessoa no Brasil | outra pessoa em país]
- Exportação de serviço: [Sim | Não]. [uma frase com o motivo]

---

### Código de Tributação Nacional: **[código de 6 números | Não indicado]**
- Descrição: [descrição da tabela]
- O que é: [explicação curta do glossário]
- Justificativa: [até 50 palavras]
- Certeza: [valor]
- Fonte: [documento oficial]

### Código na NBS: **[código com pontos] ([código só com números]) | Não indicado**
- Descrição: [descrição da tabela]
- O que é: [explicação curta do glossário]
- Justificativa: [até 50 palavras, com as outras opções do mesmo subitem]
- Certeza: [valor]
- Fonte: [documento oficial]

### Indicador de Operação: **[código | Não preencher]**
- O que é: [explicação curta do glossário]
- Justificativa: [até 50 palavras]
- Certeza: [valor]
- Fonte: [documento oficial]

### CST (IBS/CBS): **[código]**
- Nome: [nome do CST]
- O que é: [explicação curta do glossário]
- Justificativa: [até 50 palavras]
- Certeza: [valor]
- Fonte: [documento oficial]

### cClassTrib (IBS/CBS): **[código]**
- Nome: [nome do cClassTrib]
- O que é: [explicação curta do glossário]
- Justificativa: [até 50 palavras]
- Certeza: [valor]
- Fonte: [documento oficial]

---

**Outros campos da emissão completa**
- Preencher IBS/CBS: Sim. Assim, você já fica pronto para 2027, quando o preenchimento passa a ser obrigatório.
- Tributação do ISSQN: [opção e motivo em uma frase]
- Comércio exterior: [campo: valor], um por linha

**Atenção**
- [alerta fixo de cobrança]
- [alerta fixo de ocupação]
- [até 3 alertas do caso, do maior risco para o menor; o alerta de tabela não conferida vem primeiro]
- Outras observações: [demais alertas, curtos, separados por ponto e vírgula | omita a linha se não houver]

> Esta orientação é informativa e não substitui uma pessoa contadora. Antes de emitir a nota, confirme os códigos com um profissional de contabilidade.
```

## Exemplo preenchido

Caso fictício: revisão de textos de um livro, feita pela internet, para uma editora no Brasil. O MEI respondeu que a editora usou o serviço. Neste exemplo, a IA estava sem acesso à web.

**O exemplo mostra só o formato.** Os códigos aparecem como marcadores entre colchetes. Nunca copie códigos de um exemplo. Os códigos vêm das tabelas da skill, com a conferência do Passo 4.

```markdown
**Verificação de atualização:** Não foi possível verificar em [data de hoje]. Abri 0 de 5 fontes oficiais. Base revisada em [data de `ultima_verificacao_em`].

**O que entendi do seu serviço**
- Serviço: revisão de textos de um livro
- Como foi feito: à distância
- Quem pagou: Brasil
- Quem usou o serviço: a mesma empresa que pagou
- Exportação de serviço: Não. Quem pagou está no Brasil.

---

### Código de Tributação Nacional: **[código de 6 números da tabela]**
- Descrição: [descrição copiada da tabela]
- O que é: o código que identifica o tipo de serviço na lista nacional.
- Justificativa: você revisou textos para uma editora. Este é o código da lista nacional que descreve esse serviço. [Se o subitem tiver mais de um código, diga por que escolheu este.]
- Certeza: Confira no Emissor Nacional
- Fonte: Portal da NFS-e, lista de Códigos de Tributação Nacional (cópia de [data da cópia])

### Código na NBS: **[NBS com pontos] ([NBS só com números])**
- Descrição: [descrição copiada da tabela]
- O que é: a Nomenclatura Brasileira de Serviços, uma lista oficial que classifica cada serviço.
- Justificativa: [por que esta descrição combina com o serviço]. As outras opções do mesmo subitem são [opções da tabela].
- Certeza: Confira no Emissor Nacional
- Fonte: Anexo VIII [versão], Portal da NFS-e (cópia de [data da cópia])

### Indicador de Operação: **[código da seção 5.2 da base]**
- O que é: o código que mostra onde a lei considera que o serviço aconteceu.
- Justificativa: o serviço foi feito à distância e cobrado de uma empresa no Brasil. Nesse caso, a lei considera o lugar de quem pagou.
- Certeza: Confirmado
- Fonte: Anexo VII [versão]; LC 214/2025, art. 11, X

### CST (IBS/CBS): **Não indicado**
- O que é: Código de Situação Tributária: mostra se o IBS e a CBS são cobrados normalmente ou não.
- Justificativa: nenhuma fonte oficial define o CST do MEI em serviço prestado no Brasil.
- Certeza: Consulte um contador
- Fonte: Res. CGSN 140/2018, art. 106, § 1º, V (o MEI não destaca IBS e CBS)

### cClassTrib (IBS/CBS): **Não indicado**
- O que é: Código de Classificação Tributária: detalha o motivo do CST.
- Justificativa: sem CST definido, não há cClassTrib seguro para indicar.
- Certeza: Consulte um contador
- Fonte: seção 5.3 da base

---

**Outros campos da emissão completa**
- Preencher IBS/CBS: Sim. Assim, você já fica pronto para 2027, quando o preenchimento passa a ser obrigatório.
- Tributação do ISSQN: 1, operação tributável. O ISS do MEI já está no valor fixo do DAS.

**Atenção**
- Considerei que você cobrou pelo serviço. Se você não cobrou, avise, porque o Indicador de Operação muda.
- Confira se este serviço corresponde a uma ocupação do seu CCMEI (Certificado da Condição de Microempreendedor Individual). Se não corresponder, consulte um contador.
- O Código de Tributação Nacional e a NBS vieram de cópias das tabelas oficiais feitas em [data da cópia]. Não consegui conferir se esses códigos continuam iguais. Confira no Emissor Nacional antes de emitir a nota.
- O CST e o cClassTrib do MEI em serviço no Brasil ainda não têm regra oficial. Peça a um contador os códigos antes de emitir a nota.
- Outras observações: se a editora quiser reter ISS, a lei não permite retenção de ISS de MEI (LC 123/2006, art. 21, § 4º, IV).

> Esta orientação é informativa e não substitui uma pessoa contadora. Antes de emitir a nota, confirme os códigos com um profissional de contabilidade.
```
