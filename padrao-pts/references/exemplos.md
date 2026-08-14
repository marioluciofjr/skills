# Exemplos completos do PZCT-PTS100

Seis exemplos de antes/depois: cinco cobrem um tipo de conteúdo citado como caso de uso da skill, e o sexto mostra a regra PTS-7 em ação. Cada um mostra o cabeçalho de diagnóstico, as regras aplicadas e o texto final — já em markdown estruturado, nunca em bloco de texto corrido, seguindo `assets/formato-saida.md`.

Os blocos "Antes" têm defeito de propósito — são o material de trabalho para demonstrar cada regra, incluindo o "não é sobre... é sobre" do exemplo 2, citado ali como o erro a corrigir. Trate esses trechos como exemplo do problema, sempre, nunca como orientação de estilo a seguir.

## 1. Trecho de guia

- **Destinatário:** humano
- **Critério lusófono:** português - Brasil (padrão)

Antes:
> Quando da ocorrência de uma falha no sistema, é necessário que seja realizada a verificação dos logs, os quais devem ser analisados minuciosamente, a fim de que se possa identificar a causa raiz do problema que ocasionou a falha.

| Regra | Original | Reescrito |
|---|---|---|
| PTS-1 | "é necessário que seja realizada a verificação" (sujeito oculto) | "verifique os logs" |
| PTS-3 | "seja realizada a verificação" (verbo-suporte) | "verifique" |
| PTS-2 | frase de 40+ palavras, três ideias | três frases curtas |

**Texto final:**

1. Verifique os logs assim que o sistema falhar.
2. Analise os logs com cuidado.
3. Identifique a causa raiz da falha.

## 2. Parágrafo de e-book

- **Destinatário:** humano
- **Critério lusófono:** português - Brasil (padrão)

Antes:
> A produtividade não é sobre fazer mais coisas. É sobre fazer as coisas certas. E isso muda tudo. Ferramentas de IA generativa podem, eventualmente, ajudar nesse processo, embora seus resultados devam sempre ser revisados com cautela.

Depois (o "não é X, é Y" do original cai aqui como efeito colateral de PTS-9, ao lado dos outros dois problemas da frase):

| Regra | Original | Reescrito |
|---|---|---|
| PTS-9 | "não é sobre... é sobre... e isso muda tudo" (paralelismo negativo + clapping) | reescrito direto, sem antítese retórica |
| PTS-5 | "podem, eventualmente, ajudar" (hedge) | "ajudam" + condição explícita |
| PTS-4 | passiva "devam ser revisados" | ativa, com sujeito |

**Texto final:**

Produtividade é fazer as coisas certas, não fazer mais coisas. Ferramentas de IA generativa ajudam nesse processo. Revise sempre o resultado antes de usar.

*(este texto final fica em parágrafo, sem lista, porque o original também era um parágrafo reflexivo — a regra é formatar o texto final conforme a estrutura do conteúdo, não forçar lista onde o conteúdo não é uma sequência de itens)*

## 3. Post tutorial

- **Destinatário:** humano
- **Critério lusófono:** português - Brasil (padrão)

Antes:
> Para você conseguir configurar a API (Application Programming Interface) de forma correta, o token de acesso deve ser gerado, e ele deverá ser copiado e colado no arquivo de configuração, processo que pode levar de 5 a 10 minutos dependendo da familiaridade do usuário com o painel.

| Regra | Original | Reescrito |
|---|---|---|
| PTS-8 | "API (Application Programming Interface)" (sigla depois do nome, ordem invertida) | "Interface de Programação de Aplicações (API)" |
| PTS-4 | "deve ser gerado... deverá ser copiado" (passiva encadeada) | imperativo: "gere... copie... cole" |
| PTS-8 | "de 5 a 10 minutos" (faixa que sinaliza estimativa não medida) | número único ou condição explícita |

**Texto final:**

1. Gere o token de acesso na Interface de Programação de Aplicações (API).
2. Copie o token.
3. Cole o token no arquivo de configuração.

O processo leva cerca de 5 minutos.

## 4. Passo de manual de instrução

- **Destinatário:** humano
- **Critério lusófono:** português - Brasil (padrão)

Antes:
> Antes de prosseguir com a manutenção, o operador deverá certificar-se de que o equipamento se encontra desligado, sendo que, caso contrário, poderá haver risco de choque elétrico, o que deve ser evitado a todo custo.

| Regra | Original | Reescrito |
|---|---|---|
| PTS-5 | "deverá certificar-se" (hedge em instrução) | "verifique" (imperativo direto) |
| PTS-9 | aviso de risco depois da condição, condição no meio da frase | aviso de segurança primeiro, no formato AVISO |
| PTS-2 | uma frase, três ideias encadeadas por vírgula | frases separadas |

**Texto final:**

**AVISO:** não faça a manutenção com o equipamento ligado. O equipamento ligado pode causar choque elétrico.

Verifique se o equipamento está desligado antes de continuar.

## 5. Instrução para sistema agêntico (modo agente)

- **Destinatário:** IA generativa
- **Critério lusófono:** português - Brasil (padrão)

Antes (trecho de um `SKILL.md` mal escrito):
> Essa skill é utilizada para realizar o processamento de arquivos. Após o processamento, o mesmo é validado e, caso aprovado, será enviado para o destino configurado. Arquivo processado.

| Regra | Original | Reescrito |
|---|---|---|
| PTS-3 | "realizar o processamento de" (verbo-suporte) | "processa" |
| PTS-1 (modo agente) | "o mesmo é validado" (referência cruzando frase) | repete "o arquivo" |
| PTS-1 (modo agente) | "Arquivo processado." (particípio isolado — evento ou estado?) | sujeito + verbo finito |

**Texto final:**

Esta skill processa arquivos.

1. O agente valida o arquivo processado.
2. Se o arquivo for aprovado, o agente envia o arquivo para o destino configurado.
3. O agente enviou o arquivo. *(evento — se for status, use "O arquivo está no estado ENVIADO.")*

## 6. Mesma frase, dois públicos lusófonos (regra PTS-7)

**Pedido A — sem declaração de público:** aplique o padrão, português do Brasil.

- **Destinatário:** humano
- **Critério lusófono:** português - Brasil (padrão)

**Texto final:** O usuário deve conectar o celular ao computador antes de abrir o aplicativo.

**Pedido B — a pessoa usuária escreveu "preciso desse texto para Portugal":** troque a variante conforme `references/variantes-lusofonas.md`.

- **Destinatário:** humano
- **Critério lusófono:** português - Portugal

**Texto final:** O utilizador deve ligar o telemóvel ao computador antes de abrir a aplicação.

| Regra | Termo em português - Brasil | Termo em português - Portugal |
|---|---|---|
| PTS-7 | usuário | utilizador |
| PTS-7 | celular | telemóvel |
| PTS-7 | conectar | ligar |
| PTS-7 | aplicativo | aplicação |

Nenhuma das duas frases está errada. A troca aconteceu só porque o Pedido B declarou o público; sem essa declaração, a resposta A é sempre o padrão.
