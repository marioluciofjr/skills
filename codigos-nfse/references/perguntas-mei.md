# Roteiro de perguntas ao MEI

Este arquivo tem dois tipos de conteúdo:

- **Texto para o MEI:** copie esse texto na conversa. Não troque o texto por termos técnicos.
- **Uso interno:** orienta a decisão dos códigos. Não mostre esse conteúdo ao MEI.

## Como fazer as perguntas

- Faça no máximo 4 perguntas, todas em uma única mensagem.
- Pergunte somente o que a descrição do serviço ainda não responde.
- A Pergunta 4 é obrigatória. Pule só se o MEI disser, com todas as letras, quem usou o serviço e onde essa pessoa está.
- Na Pergunta 3, a moeda é obrigatória quando quem pagou está fora do Brasil. Se o MEI responder sem a moeda, pergunte de novo. Nunca presuma a moeda.
- Numere as perguntas da mensagem a partir de 1, na ordem em que aparecem. Os números deste roteiro são só para uso interno. Exemplo: se faltam as perguntas 3 e 4 do roteiro, mostre como 1 e 2.
- Mostre as opções com letras (a, b, c).
- Diga ao MEI que ele pode responder só com os números e as letras. Exemplo: "1b euro, 2c".
- Se a resposta ficar confusa, reformule com um exemplo. Nunca adivinhe a resposta.
- Use a data de hoje, obtida no Passo 0, como data do serviço. Não pergunte a data.
- Não pergunte se o serviço foi cobrado. Presuma cobrança (operação onerosa) e use o alerta de cobrança de `assets/formato-saida.md`.
- Não pergunte a ocupação do MEI. Use o alerta de ocupação de `assets/formato-saida.md`.

## Mensagem de abertura

Comece sempre com esta frase. Ela obriga a separar o que o MEI já informou do que falta.

> Para indicar os códigos certos, preciso entender melhor o seu serviço. Você já informou: [fatos que a descrição já responde, em linguagem simples]. Faltam [número] respostas. Você pode responder só com os números e as letras, por exemplo: [exemplo com a numeração desta mensagem].

Se a descrição não responder nada, escreva "Você ainda não informou como, onde e para quem fez o serviço." no lugar da lista de fatos.

### Exemplo de mensagem quando faltam só as perguntas 3 e 4 do roteiro

Este exemplo é fictício. Ele mostra só o formato da mensagem.

Descrição do MEI: "Traduzi o site de uma empresa do Chile. Fiz tudo pela internet."

> Para indicar os códigos certos, preciso entender melhor o seu serviço. Você já informou: o serviço foi à distância, foi uma tradução e quem pagou está no Chile. Faltam 2 respostas. Você pode responder só com os números e as letras, por exemplo: 1 dólar, 2a.
>
> **1. Em qual moeda a empresa do Chile pagou?** Exemplos: peso chileno, dólar, real.
>
> **2. Quem usou ou recebeu o serviço foi a mesma pessoa ou empresa que pagou?**
> a) Sim, foi a mesma pessoa ou empresa.
> b) Não. Quem usou o serviço mora ou trabalha no Brasil.
> c) Não. Quem usou o serviço mora ou trabalha em outro país.

Repare: as perguntas aparecem como 1 e 2, e não como 3 e 4.

---

## As 4 perguntas

### Pergunta 1. Como e onde você fez o serviço?

**Texto para o MEI:**

> **1. Como e onde você fez o serviço?**
> a) À distância: pela internet, por videochamada, por telefone ou por e-mail.
> b) Pessoalmente, no meu local de trabalho.
> c) Pessoalmente, na casa ou na empresa do cliente.
> d) Pessoalmente, em outro lugar no Brasil. Exemplos: auditório, hotel, local de evento.
> e) Pessoalmente, fora do Brasil.
> f) Uma parte pessoalmente e outra parte à distância.

**Por que perguntamos (mostre ao MEI se ele pedir):** a forma e o lugar do serviço mudam o lugar onde a lei considera que o serviço aconteceu.

**Uso interno:**
- a) Serviço à distância. Regra do art. 11, X, da LC 214/2025 (lugar de quem pagou). Use as linhas do grupo 10 da seção 5.2 da base. Pelo art. 11, § 5º, serviço sobre a pessoa feito à distância também segue o inciso X.
- b) Serviço no estabelecimento do MEI. Linhas 030101 ou 050101 da seção 5.2, conforme a Pergunta 2.
- c) ou d) Serviço fora do estabelecimento do MEI, no Brasil. Linhas 030102 ou 050102 da seção 5.2, conforme a Pergunta 2.
- e) Local da operação fora do Brasil. Avalie exportação pelo art. 80, § 1º-A, I. Em comércio exterior, `mdPrestacao` = 3.
- f) Serviço misto. O art. 11, § 5º manda usar o inciso X. Em exportação, só a parte consumida no exterior é exportação (art. 80, § 5º). Recomende contador.

### Pergunta 2. Sobre o que foi o serviço?

**Texto para o MEI:**

> **2. O serviço foi feito sobre alguma destas coisas?**
> a) Um imóvel. Exemplos: casa, apartamento, terreno, sala comercial.
> b) Um objeto. Exemplos: carro, celular, roupa, máquina.
> c) A organização de um evento. Exemplos: feira, congresso, show.
> d) Transporte de pessoas ou de cargas.
> e) Nenhuma dessas. O serviço foi para pessoas. Exemplos: aula, consultoria, corte de cabelo, fotografia.

**Uso interno:** use somente as linhas da seção 5.2 da base.
- a) Art. 11, II. Linha 020201 (serviço sobre imóvel) ou 020301 (administração e intermediação de imóvel).
- b) Art. 11, V. Com Pergunta 1 = b: 050101. Com Pergunta 1 = c ou d: 050102. Serviço à distância sobre objeto não é "prestado fisicamente": use o grupo 10.
- c) Art. 11, IV. Linha 040101.
- d) Art. 11, VI ou VII. Passageiros: 060101. Carga: 070101 ou 070102, escolha em [LACUNA]. Recomende contador.
- e) Art. 11, III, somente se o serviço for exclusivamente sobre a pessoa ou usado integralmente de forma presencial por pessoa física. Com Pergunta 1 = b: 030101. Com Pergunta 1 = c ou d: 030102. Nos demais casos, use o grupo 10.
- Caso sem linha na seção 5.2: escreva "Não indicado" e oriente conferir no Emissor Nacional.

### Pergunta 3. Onde está quem pagou?

**Texto para o MEI:**

> **3. Quem pagou pelo serviço mora ou tem empresa em qual país?**
> a) No Brasil.
> b) Em outro país. Diga qual país e em qual moeda o cliente pagou.

**Por que perguntamos:** quando quem pagou está em outro país, o serviço pode ser uma exportação. Exportação é a venda de um serviço para alguém de fora do Brasil. Exportação de serviço não paga alguns impostos.

**Uso interno:** quem pagou = adquirente e tomador (LC 214/2025, art. 3º, IV).
- a) Afasta a exportação. No grupo 10, com serviço cobrado: 100301.
- b) Pode ser exportação. Avalie com a Pergunta 4. A moeda vai no campo `tpMoeda`, com o código da tabela de moedas do Banco Central. O valor da nota vai em reais. A conversão para IBS/CBS usa a taxa do Banco Central (LC 214/2025, art. 12, § 5º).

### Pergunta 4. Quem usou o serviço?

**Texto para o MEI:**

> **4. Quem usou ou recebeu o serviço foi a mesma pessoa ou empresa que pagou?**
> a) Sim, foi a mesma pessoa ou empresa.
> b) Não. Quem usou o serviço mora ou trabalha no Brasil.
> c) Não. Quem usou o serviço mora ou trabalha em outro país.
>
> Exemplo da letra b: uma empresa da Argentina pagou um treinamento para funcionários que moram no Brasil.
> Se você foi contratado por quem organizou um curso ou evento, quem recebeu o seu serviço foi quem contratou você.
> Se as pessoas que usaram o serviço estavam em países diferentes, diga quantas estavam no Brasil e quantas fora.

**Por que perguntamos:** para ser exportação, quem pagou e quem usou o serviço precisam estar fora do Brasil.

**Uso interno:** quem usou = destinatário (LC 214/2025, art. 3º, V). Esta pergunta decide a exportação para IBS/CBS (art. 80, § 1º-A, II). Nunca presuma a resposta.
- a) `indDest` = 0.
- b) `indDest` = 1. Se quem pagou está fora do Brasil: não é exportação para IBS/CBS (art. 80, § 1º-A, II). No grupo 10: 100302.
- c) `indDest` = 1. Se quem pagou também está fora do Brasil: pode ser exportação (art. 80, § 1º-A, II).
- Pessoas no Brasil e fora: só a parte consumida no exterior é exportação (art. 80, § 5º). Recomende contador.

## Cobrança presumida

A skill presume que o serviço foi cobrado (operação onerosa). Se o MEI disser que não cobrou, use 100401 no grupo 10. Operação não onerosa tem regras próprias de IBS/CBS (LC 214/2025, art. 4º, § 1º). Recomende contador.

---

## Campos de exportação sem pergunta

Na exportação, a skill não pergunta sobre vínculo com o cliente nem sobre apoio do governo. Use estes valores com a certeza "Sugerido":

- `vincPrest` = 0 (sem vínculo).
- `mecAFComexP` e `mecAFComexT` = 01 (nenhum).
- `movTempBens` = 1 (não), quando o serviço não envolve bens.

Inclua sempre este alerta no bloco "Atenção": "Se você e o cliente fazem parte do mesmo grupo de empresas, ou se você usou programa do governo de apoio à exportação, consulte um contador."

## Mapa das respostas para a seção 5.1 da base (exportação)

| Pergunta 1 | Pergunta 3 | Pergunta 4 | Resultado |
|---|---|---|---|
| a | b | a ou c | Exportação para IBS/CBS. Avalie o ISS pelo resultado no exterior. cIndOp: nota sobre exportação da seção 5.2 |
| a | b | b | Não é exportação. cIndOp 100302 |
| a | a | qualquer | Não é exportação. cIndOp 100301 |
| b, c ou d | b | qualquer | Não é exportação. Serviço feito pessoalmente no Brasil (art. 11, III). Exceção: serviço presencial que não é sobre a pessoa segue a linha da letra a |
| e | b | a ou c | Exportação (art. 80, § 1º-A, I) |
| e | b | b | Não é exportação para IBS/CBS. Quem usou o serviço está no Brasil. Recomende contador |
| e | a | qualquer | Não é exportação. Quem pagou está no Brasil |
| f | b | a ou c | Exportação só da parte consumida no exterior. Recomende contador |
