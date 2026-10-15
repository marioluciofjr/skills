# Base de conhecimento: MEI e NFS-e Nacional (emissão completa)

Arquivo de referência da skill. Pesquisa realizada em 14/10/2026.

> **Aviso obrigatório em toda resposta da skill:** esta orientação é informativa e não substitui a análise de uma pessoa contadora. Na dúvida, consulte um profissional de contabilidade.

---

## 0. Como usar este arquivo

- Cada regra traz a **fonte** e o **grau de certeza**:
  - **[CONFIRMADO]**: está no texto de lei, resolução ou documentação técnica oficial.
  - **[INFERIDO]**: dedução lógica a partir de fontes oficiais, sem texto expresso.
  - **[LACUNA]**: as fontes não resolvem. A skill deve encaminhar ao contador.
  - **[SEM FONTE OFICIAL]**: encontrado só em fonte não oficial. Tratar como lacuna.
  - **[CONFIRMAR NO ANEXO VI/VII]**: regra técnica vista em transcrição não oficial; conferir no anexo oficial vigente antes de usar.
- Antes de responder, a skill deve executar a **checagem de atualização** (seção 1).
- Nenhum código pode ser sugerido se não constar nas tabelas oficiais vigentes.

### 0.1 Política de fontes (obrigatória)

1. **Sempre preferir fonte oficial**, nesta ordem:
   1. Lei (planalto.gov.br) e normas publicadas no Diário Oficial da União.
   2. Resoluções do CGSN e do CGNFS-e (normas.receita.fazenda.gov.br ou DOU).
   3. Documentação técnica do Portal Nacional da NFS-e (gov.br/nfse) e da calculadora oficial (consumo.tributos.gov.br).
   4. Páginas de órgãos públicos (Receita Federal, secretarias de fazenda).
2. Fontes não oficiais (blogs, fóruns, sites de ERP, escritórios) servem **apenas para localizar** a norma. Nunca são citadas como fundamento.
3. Quando uma regra só tiver sido encontrada em fonte não oficial, ela recebe a marca **[SEM FONTE OFICIAL]** e a skill deve tratá-la como lacuna.
4. Toda resposta deve citar a norma ou documento oficial com artigo, item ou versão.

---

## 1. Manifesto de versões e checagem de atualização

### 1.1 Versões vigentes encontradas em 14/10/2026

| Documento | Versão | Onde verificar |
|---|---|---|
| Nota Técnica SE/CGNFS-e nº 009 | v1.01 (o PDF é datado de 11/09/2026; a página lista 01/10/2026) | gov.br/nfse → Documentação técnica → RTC |
| Nota Técnica SE/CGNFS-e nº 010 | v1.00. Trata do leiaute da NFS-e Via e do evento de manifestação do adquirente (descrição da página RTC; nota não lida na íntegra) | mesma página |
| Anexo VI – Leiaute e regras de negócio | v1.04.01 (NT 009) | mesma página |
| Anexo VII – Indicador de operação (cIndOp) | v1.03.00 publicado; a NT 009 cita v1.02.01 | mesma página |
| Anexo VIII – Correlação Item × NBS × cClassTrib × cIndOp | v1.01.00 (não normativo, em desenvolvimento) | mesma página |
| Tabela CST e cClassTrib | Informe Técnico 2025.002 v1.60 (23/06/2026) | Portal da NF-e; calculadora consumo.tributos.gov.br |
| LC 214/2025 | Alterada pela LC 227/2026 (13/01/2026) e LC 235/2026 (27/08/2026) | planalto.gov.br |
| Resolução CGSN 140/2018 | Alterada pela Res. CGSN 190/2026 (efeitos em 01/01/2027) | normas.receita.fazenda.gov.br |
| Resolução CGSN 191/2026 | NFS-e nacional obrigatória para ME/EPP a partir de 01/11/2026 | idem |

### 1.2 Discrepâncias já detectadas

- A NT 009 v1.01 menciona o Anexo VII v1.02.01, mas a página oficial publica a v1.03.00. **Usar sempre a versão publicada na página.**
- A NT 009 informa que o cronograma de implantação será publicado no portal. Na página "Atualizações e Implantações" (atualizada em 11/08/2026), a produção de 10/08/2026 cita apenas a evolução da NT 004 no Emissor Nacional Web. **As regras da NT 009 podem ainda não estar em produção.**
- A NT 010 v1.00 trata da NFS-e Via, outro tipo de documento. Até leitura integral, ela não altera as regras desta base para o MEI.
- A tabela da seção 5.2 foi conferida no arquivo oficial do Anexo VII v1.03.00 em 14/10/2026. Os códigos 030103, 030104 e 050103, presentes em cópias não oficiais, não existem nessa versão.
- Fonte não oficial cita a versão 1.70 do Informe Técnico 2025.002. A versão não foi confirmada em página oficial. Os códigos 410004 e 410027 aparecem na tabela oficial do ambiente nacional (SVRS) em 14/10/2026.

### 1.3 Procedimento obrigatório antes de responder

Siga o Passo 0 do `SKILL.md`. O Passo 0 usa o arquivo `references/manifest.json`, que guarda as URLs, as versões registradas, os marcadores de versão e as datas-gatilho. Ao atualizar esta base, atualize também o manifesto.

### 1.4 Rotina de manutenção (para quem mantém a skill)

Faça esta rotina antes da data `revisar_ate` do manifesto.

1. Abra cada URL do manifesto, inclusive as de prioridade média.
2. Compare a versão publicada com o campo `registrado`.
3. Se houver versão nova, leia o documento e atualize as seções listadas em `secoes_afetadas`.
4. Atualize `registrado` e `marcadores_de_versao` no manifesto.
5. Mova `ultima_verificacao_em` para a data de hoje e `revisar_ate` para 30 dias depois.
6. Registre a alteração no campo `historico` do manifesto.
7. Se a lista de Códigos de Tributação Nacional ou o Anexo VIII mudarem, gere de novo os arquivos de `references/tabelas/` a partir da fonte oficial. Atualize `tabelas_incorporadas` no manifesto (data, versão e número de linhas).
8. Cruze todas as NBS de `anexo-viii-item-nbs.csv` com a tabela oficial NBS 2.0 do MDIC. Remova da cópia a NBS que não existir mais. Registre o resultado em `cruzamento_com_nbs_oficial`.

---

## 2. Linha do tempo relevante para o MEI

| Data | Evento | Fonte |
|---|---|---|
| 01/09/2023 | MEI obrigado a emitir NFS-e no padrão nacional | Res. CGSN 169/2022, alterada pela Res. CGSN 172/2023 (Portal NFS-e, "Legislação Aplicável ao MEI") |
| 05/01/2026 | Leiaute NT 004 (grupos IBS/CBS) em produção | Portal NFS-e, página RTC |
| 10/08/2026 | Emissor Nacional Web com destaque de IBS/CBS (NT 004) | Portal NFS-e, "Atualizações e Implantações" |
| 30/09/2026 | Fim do prazo de opção de ME/EPP pelo regime regular de IBS/CBS no 1º semestre de 2027 (não se aplica ao MEI) | Res. CGSN 140/2018, art. 40-D, I (redação da Res. CGSN 190/2026, DOU 10/08/2026) |
| 01/11/2026 | NFS-e nacional obrigatória para ME/EPP do Simples | Res. CGSN 191/2026 (DOU 10/08/2026) |
| 31/12/2026 | Último dia antes da obrigatoriedade dos campos de IBS/CBS para optantes do Simples (inclui MEI) | Ato Conjunto RFB/CGIBS nº 4/2026 (DOU 31/07/2026), art. 1º, § 1º |
| 01/01/2027 | Optantes do Simples (inclui MEI): campos de IBS/CBS obrigatórios; MEI: nota obrigatória em todas as prestações; IBS/CBS passam a compor o valor fixo do Simei | Ato Conjunto RFB/CGIBS nº 4/2026; Res. CGSN 140/2018, arts. 101 e 106 (redação da Res. CGSN 190/2026) |

---

## 3. Regras gerais do MEI

### 3.1 Enquadramento
- **[CONFIRMADO]** Só pode ser MEI quem exerce ocupação listada no Anexo XI da Resolução CGSN 140/2018. A lista muda por resolução do CGSN e é consultável no Portal do Empreendedor.
- **[CONFIRMADO]** Limite de receita bruta: R$ 81.000,00 por ano, proporcional no ano de abertura (LC 123/2006, art. 18-A, §§ 1º e 2º). Confirmar no texto compilado do Planalto a cada uso, pois há projetos de lei para alterar o valor.
- **[SEM FONTE OFICIAL]** Limite diferenciado do MEI transportador autônomo de cargas (R$ 251.600,00): visto só em fontes secundárias. Conferir na LC 123/2006 antes de usar.
- **[LACUNA]** Se a receita de exportação de serviços tem tratamento separado no limite do MEI. Fontes encontradas tratam o limite como total. Encaminhar ao contador.
- **Regra da skill:** se o serviço descrito não corresponder a nenhuma ocupação permitida, alertar sobre risco de desenquadramento e recomendar contador. Não sugerir códigos que mascarem a atividade real.

### 3.2 Obrigação de emitir nota
- **[CONFIRMADO]** Até 31/12/2026: obrigatória para tomador pessoa jurídica; facultativa para tomador consumidor final pessoa física (Res. CGSN 140/2018, redação da Res. CGSN 169/2022).
- **[CONFIRMADO]** A partir de 01/01/2027: "O MEI deverá emitir os documentos fiscais nas vendas e nas prestações de serviços realizadas" (Res. CGSN 140/2018, art. 106, caput, redação da Res. CGSN 190/2026).
- **[CONFIRMADO]** Serviços sujeitos à Nota Fiscal de Serviços: uso obrigatório e sem custo da NFS-e de padrão nacional, pelo Emissor Nacional (Res. CGSN 140/2018, art. 106-A, redação da Res. CGSN 190/2026).
- **[CONFIRMADO]** É vedada a emissão de NFS-e pelo MEI em operações sujeitas apenas ao ICMS (Res. CGSN 140/2018, redação da Res. CGSN 169/2022).

### 3.3 Tributos no DAS
- **[CONFIRMADO]** O MEI recolhe ISS em valor fixo no DAS (LC 123/2006, art. 18-A).
- **[CONFIRMADO]** Não cabe retenção na fonte de ISS quando o optante está sujeito ao ISS por valores fixos mensais (LC 123/2006, art. 21, § 4º, IV). No mesmo sentido, a Res. CGSN 140/2018, art. 103, IV. A skill deve alertar se o tomador tentar reter ISS.
- **[CONFIRMADO]** A partir de 2027, IBS e CBS integram o valor fixo do Simei, "nos valores discriminados no Anexo XIII" (Res. CGSN 140/2018, art. 101, IV, redação da Res. CGSN 190/2026).
- **[SEM FONTE OFICIAL]** Valores do Anexo XIII (R$ 0,994 de CBS e R$ 0,006 de IBS em 2027) foram vistos só em fontes secundárias. Conferir no Anexo XIII antes de usar.
- **[CONFIRMADO]** O MEI fica dispensado "de destacar os valores de IBS e CBS nos documentos fiscais emitidos" (Res. CGSN 140/2018, art. 106, § 1º, V, redação da Res. CGSN 190/2026).
- **[CONFIRMADO]** A opção pelo regime regular de IBS/CBS é prevista para optantes do Simples (LC 214/2025, art. 41, § 3º; Res. CGSN 140/2018, art. 40-C). Os contribuintes optantes pelo MEI ficam sujeitos às regras desse regime (LC 214/2025, art. 41, § 2º).

---

## 4. Emissão completa no Emissor Nacional: campos e valores para MEI

### 4.1 Quando usar a emissão completa
- **[SEM FONTE OFICIAL]** A emissão completa seria obrigatória em casos como exportação e ISS devido no local do tomador (informação de fonte secundária). Conferir no manual do Emissor Nacional (Portal NFS-e, "Links com Passo a Passo").
- **[CONFIRMADO]** O grupo de comércio exterior (`comExt`) existe apenas no leiaute completo da DPS (NT 009, item 2.12), o que é compatível com a necessidade da emissão completa na exportação.

### 4.2 Prestador (regime tributário)

| Campo (XML) | Valor para MEI | Certeza | Fonte |
|---|---|---|---|
| opSimpNac | 2 – Optante MEI | [CONFIRMADO] | NT 009, item 2.4 |
| regApIBSCBSSN | Provavelmente 1 – IBS e CBS apurados pelo SN | [INFERIDO] | NT 009, item 2.4. Campo novo; pode não estar em produção |
| cAtvSN | Código da atividade no Simples (ex.: 7 – serviços com ISS, Anexo III) | [LACUNA] para MEI | NT 009, item 2.4 |

### 4.3 Pessoas (tomador e destinatário)
- **[CONFIRMADO]** `indDest`: 0 = destinatário é o próprio tomador/adquirente; 1 = destinatário diferente (NT 009, item 2.11).
- **[CONFIRMADO]** Pessoa no exterior: informar NIF (identificação fiscal estrangeira) ou o motivo de não informar (`cNaoNIF`: 0, 1 ou 2), e endereço no exterior (país ISO, código postal, cidade, estado/província) (NT 009, item 2.11, grupo `dest`; estrutura equivalente no grupo do tomador no Anexo VI).
- **[CONFIRMADO]** A Sefin Nacional valida o município do tomador e do destinatário contra o cadastro CNPJ/CPF. Divergência gera rejeição (NT 009, item 2.10).

### 4.4 Serviço
- **Código de Tributação Nacional (cTribNac):** 6 dígitos (item, subitem e desdobro da lista da LC 116/2003). Fonte: lista oficial do Portal da NFS-e. Cópia em `references/tabelas/codigos-tributacao-nacional.csv` (335 códigos, copiada em 14/10/2026).
- **NBS por subitem:** cópia do Anexo VIII em `references/tabelas/anexo-viii-item-nbs.csv` (980 pares, v1.01.00). O Emissor Nacional pede a NBS só com números (ex.: 122051900).
- **[CONFIRMADO]** As NBS mudam com o tempo. Todo código tirado das cópias passa pela conferência do Passo 4, item 4, do `SKILL.md`.
- **Tabela oficial da NBS:** NBS 2.0, publicada pelo MDIC (Portaria Conjunta RFB/SCS nº 1.429/2018 e alterações). Em 14/10/2026, as 980 NBS da cópia do Anexo VIII existiam na tabela oficial (arquivo atualizado em 03/07/2025), com a mesma descrição.
- **NBS:** obrigatória. Há rejeição específica quando não informada em exportação [CONFIRMAR NO ANEXO VI].
- **Atenção:** um mesmo código de tributação pode se desdobrar em mais de uma NBS. O Anexo VIII ajuda, mas não é normativo.

### 4.5 Tributação do ISSQN

| tribISSQN | Significado | Uso pelo MEI |
|---|---|---|
| 1 | Operação tributável | Padrão no mercado interno (ISS no DAS, sem destaque nem retenção) |
| 2 | Imunidade | Casos específicos |
| 3 | Exportação de serviço | Quando o resultado se verifica no exterior |
| 4 | Não incidência | Casos específicos |

- **[CONFIRMAR NO ANEXO VI]** Com tribISSQN = 2, 3 ou 4, não se informa o código do local de incidência (regra de rejeição E1301). Encontrada em transcrição secundária das regras de negócio; conferir na aba de regras do Anexo VI vigente.

### 4.6 IBS/CBS (grupo IBSCBS)

| Campo | Regra | Certeza |
|---|---|---|
| Preencher IBS/CBS? | Fato: o preenchimento é opcional para o MEI até 31/12/2026 e obrigatório a partir de 01/01/2027. Regra da skill: orientar sempre "Sim", para o MEI se preparar | Fato: [CONFIRMADO], Ato Conjunto RFB/CGIBS nº 4/2026 |
| CST | Depende do tipo de operação (seção 5.3) | ver 5.3 |
| cClassTrib | Os 3 primeiros dígitos coincidem com o CST | [CONFIRMADO], estrutura da Tabela CST/cClassTrib oficial (Informe Técnico 2025.002) |
| cIndOp | **Leiaute NT 004 (produção atual):** obrigatório. **Leiaute NT 009:** só é informado quando o CST exige tributação detalhada (indicador `ind_gIBSCBS`). Com CST 400, 410 ou 820, não deve ser preenchido | [CONFIRMADO], NT 009 item 2.16 |
| gIBSCBS (valores) | Não informado com CST 410 | [CONFIRMADO] |
| tpRBSN (indicador do cClassTrib) | Classifica a receita do Simples: 3 = exportação direta | [CONFIRMADO], NT 009 item 2.4 |

### 4.7 Comércio exterior (grupo comExt)

Obrigatório em exportação de serviço. Campos da NT 009, item 2.12:

| Campo | Opções | Orientação |
|---|---|---|
| mdPrestacao | 1 Transfronteiriço; 2 Consumo no Brasil; 3 Movimento temporário de pessoas físicas; 4 Consumo no exterior; 5 Consumo concomitante no Brasil e no exterior | Ver árvore 5.4 |
| vincPrest | 0 Sem vínculo; 1 Controlada; 2 Controladora; 3 Coligada; 4 Matriz; 5 Filial; 6 Outro | MEI com cliente independente: 0 |
| tpMoeda | Código da tabela de moedas do Banco Central | Conferir na tabela do BCB (ex.: euro, dólar) |
| nFatura / vFatura | Nº e valor da fatura ou documento da transação, na moeda estrangeira | Opcional no leiaute |
| nContCambio | Nº do contrato de câmbio ou comprovante de pagamento | Opcional no leiaute |
| mecAFComexP / mecAFComexT | Mecanismo de apoio à exportação (prestador/tomador) | MEI em geral: 01 – Nenhum |
| movTempBens | 1 Não; 2 Vinculada a DUIMP; 3 Vinculada a DU-E | Serviço sem bens: 1 |
| mdic | 0 Não enviar; 1 Enviar ao MDIC | [LACUNA] Escolha do emitente |

- **[CONFIRMADO]** Com mdPrestacao = 5, a nota de exportação traz só a parcela exportada; outra NFS-e deve ser emitida para a parcela consumida no Brasil (NT 009, item 2.12).
- **[CONFIRMADO]** Para IBS/CBS, a conversão da moeda usa a PTAX do Banco Central (LC 214/2025, art. 12, § 5º; NT 009, item 2.13). Se a regra de conversão usada para o ISS for diferente, a diferença vai no campo `vAjusteBCIBSCBSComExt` (NT 009, item 2.13).
- **[CONFIRMADO]** A partir de 01/01/2027, o valor "Desconhecido" não é aceito em `mdPrestacao` e `vincPrest` nas notas compartilhadas pelos municípios (NT 009, item 2.12).

---

## 5. Árvores de decisão

### 5.1 É exportação de serviço?

Os critérios do ISS e do IBS/CBS são diferentes. Avaliar os dois.

**IBS/CBS (LC 214/2025, art. 80, com redação da LC 227/2026)** [CONFIRMADO]
- É exportação o fornecimento para residente ou domiciliado no exterior **e** consumo no exterior.
- Considera-se consumo no exterior (§ 1º-A):
  - I – quando o local da operação não é no Brasil, nos casos dos incisos II a IX do art. 11 (imóveis, serviços presenciais sobre pessoa, eventos, serviços sobre bens móveis, transporte etc.); ou
  - II – nos demais casos, quando **adquirente e destinatário** são residentes ou domiciliados no exterior.
- Fornecimento concomitante no Brasil e no exterior: só a parcela consumida no exterior é exportação (§ 5º).
- Os §§ 2º, 3º e 6º (presunção pelo domicílio do adquirente) foram **revogados** pela LC 227/2026. Conteúdo antigo da internet que cite essa presunção está desatualizado.
- Serviços do art. 11, III (sobre a pessoa ou fruídos presencialmente) prestados à distância, ainda que parcialmente, seguem a regra do inciso X (domicílio do adquirente) (LC 214/2025, art. 11, § 5º).
- No inciso X, com operação onerosa: local do domicílio do adquirente residente no País; se o adquirente não for residente, local do domicílio do destinatário residente no País (LC 214/2025, art. 11, X, "a", redação da LC 227/2026).
- Valor em moeda estrangeira: conversão pela taxa de câmbio apurada pelo Banco Central, conforme regulamento (LC 214/2025, art. 12, § 5º).

**ISS (LC 116/2003, art. 2º, I e parágrafo único)** [CONFIRMADO]
- O ISS não incide sobre exportação de serviços.
- Não é exportação o serviço desenvolvido no Brasil cujo resultado aqui se verifique, ainda que pago por residente no exterior.
- [LACUNA] "Resultado" não tem definição legal única. O STJ tem decisões que usam o critério da utilidade/fruição. Casos de fronteira devem ir ao contador.

**Fluxo prático**
1. Quem paga (adquirente) está no exterior? Se não → não é exportação.
2. Quem recebe/usa o serviço (destinatário) está no exterior? Se não → não é exportação para IBS/CBS.
3. O serviço é presencial no Brasil (art. 11, III, sobre pessoa ou fruído presencialmente)? Se sim → local da operação é o Brasil → não é exportação.
4. O resultado/utilidade se verifica no exterior? Se sim → exportação também para o ISS (tribISSQN = 3). Se houver dúvida → [LACUNA].

### 5.2 Indicador de operação (cIndOp)

Aplicar apenas se o leiaute em produção exigir o campo para o CST escolhido (ver 4.6).

Fonte: arquivo oficial `AnexoVII-IndOp_IBSCBS_v1.03.00` (NT 009), conferido em 14/10/2026. A tabela traz só as linhas de serviço úteis ao MEI. Não use código fora desta tabela.

| Situação | cIndOp | Certeza |
|---|---|---|
| Serviço feito fisicamente sobre imóvel (local do imóvel) | 020201 | [CONFIRMADO] |
| Administração e intermediação de imóvel (local do imóvel) | 020301 | [CONFIRMADO] |
| Serviço feito exclusivamente sobre a pessoa, ou usado integralmente de forma presencial por pessoa física, no estabelecimento do MEI | 030101 | [CONFIRMADO] |
| Mesmo serviço da linha anterior, em local diferente do estabelecimento do MEI | 030102 | [CONFIRMADO] |
| Planejamento, organização e administração de eventos (local do evento) | 040101 | [CONFIRMADO] |
| Serviço feito fisicamente sobre objeto (bem móvel), no estabelecimento do MEI | 050101 | [CONFIRMADO] |
| Serviço feito fisicamente sobre objeto, em local diferente do estabelecimento do MEI | 050102 | [CONFIRMADO] |
| Transporte de passageiros (local de início do transporte) | 060101 | [CONFIRMADO] |
| Transporte de carga: 070101 (endereço de entrega) ou 070102 (local da retirada) | 070101 ou 070102 | Códigos: [CONFIRMADO]. Escolha entre os dois: [LACUNA] |
| Demais serviços, cobrados, com quem pagou residente no Brasil. Inclui serviço sobre a pessoa feito à distância, mesmo em parte | 100301 | [CONFIRMADO] |
| Demais serviços, cobrados, com quem pagou fora do Brasil e quem usou no Brasil | 100302 | [CONFIRMADO] |
| Demais serviços, não cobrados (local de quem usou, no Brasil) | 100401 | [CONFIRMADO] |
| Exportação: quem pagou e quem usou estão fora do Brasil | Ver nota abaixo | [CONFIRMAR NO ANEXO VII] |

**Nota sobre exportação.** O Anexo VII v1.03.00 não tem indicador próprio para exportação. Todas as linhas do grupo 10 apontam para alguém residente no País. Pela NT 009 (item 2.16), com CST 410 o cIndOp não é informado. No leiaute NT 004, ainda em produção, o campo é obrigatório. No Caso 1 (seção 6), o Emissor Nacional aceitou 100301 em outubro de 2026. Indique 100301 com a certeza "Confira no Emissor Nacional".

**Regras de uso.**
- As linhas 030101 e 030102 valem só para serviço exclusivamente sobre a pessoa ou usado integralmente de forma presencial por pessoa física. Serviço presencial que não cumpre isso segue as linhas do grupo 10. [CONFIRMADO], descrição do Anexo VII.
- A lógica de local da operação está na LC 214/2025, art. 11.

### 5.3 CST e cClassTrib para MEI

| Situação | CST | cClassTrib | Certeza |
|---|---|---|---|
| Exportação de serviço | 410 – Imunidade e não incidência (LC 214/2025, art. 8º) | 410027 – Exportação de serviço ou de bem imaterial (alternativa genérica: 410004) | Imunidade: [CONFIRMADO]. Códigos: conferir na tabela oficial (calculadora consumo.tributos.gov.br). Escolha entre os dois: [LACUNA] |
| Operação no mercado interno (2026 e 2027 em diante) | Não definido nas fontes oficiais encontradas | Não definido | [LACUNA] O MEI não destaca IBS/CBS (Res. CGSN 140/2018, art. 106, § 1º, V). Nenhuma fonte oficial define o CST e o cClassTrib do MEI no mercado interno. O par 000/000001 aparece só em fonte não oficial e não pode ser indicado. Resposta: "Não indicado" e "Consulte um contador" |
| Serviço com possível redução (saúde, educação etc.) | Possivelmente 200 | Conforme tabela | [LACUNA] Depende do anexo da LC 214 e da aplicação ao MEI |
| Nanoempreendedor (410035) | Não se aplica ao MEI | — | [CONFIRMADO]: nanoempreendedor é a pessoa física que não aderiu ao MEI (LC 214/2025, art. 26, IV) |

### 5.4 Modo de prestação (mdPrestacao), na exportação

Baseado nos modos de prestação do GATS/OMC usados no antigo Siscoserv. [INFERIDO] O leiaute oficial (NT 009, item 2.12) lista os valores, mas não define cada modo. Até haver definição oficial, tratar como sugestão.

| Como o serviço foi prestado | mdPrestacao |
|---|---|
| Remoto: MEI no Brasil, cliente no exterior (videoconferência, entrega digital) | 1 – Transfronteiriço |
| Cliente estrangeiro veio ao Brasil para usar o serviço | 2 – Consumo no Brasil (atenção: tende a não ser exportação para IBS/CBS) |
| MEI viajou ao exterior para prestar o serviço | 3 – Movimento temporário de pessoas físicas |
| Parte consumida no Brasil e parte no exterior | 5 – Consumo concomitante (emitir duas notas) |

---

## 6. Casos de referência

### Caso 1 – Formação online para docentes em Portugal

- **Fatos:** MEI no Brasil; contratante pessoa física em Portugal; participantes em Portugal; formação via Zoom; serviço remunerado.
- **Exportação?** Sim. Adquirente e destinatários no exterior (art. 80, § 1º-A, II); resultado fruído no exterior.

| Campo | Valor | Certeza |
|---|---|---|
| Código de Tributação Nacional e NBS | Não registrados aqui, de propósito. Consulte as tabelas de `references/tabelas/` e faça a conferência do Passo 4, item 4. Códigos de serviço mudam com o tempo | — |
| tribISSQN | 3 – Exportação de serviço | Não incidência: [CONFIRMADO] (LC 116/2003, art. 2º, I). Código do campo: [CONFIRMAR NO ANEXO VI] |
| CST | 410 | [CONFIRMADO] (LC 214/2025, arts. 8º e 80; NT 009, item 2.16) |
| cClassTrib | 410027 | [CONFIRMADO] existência; escolha [LACUNA] |
| cIndOp | Leiaute NT 004: 100301, aceito pelo Emissor Nacional. Leiaute NT 009: não informar (CST 410) | Regra da NT 009: [CONFIRMADO]. Código 100301 na exportação: [CONFIRMAR NO ANEXO VII] (ver nota da seção 5.2) |
| mdPrestacao | 1 – Transfronteiriço | [INFERIDO] |
| vincPrest | 0 – Sem vínculo | [INFERIDO] |
| mecAFComexP / T | 01 – Nenhum | [INFERIDO] |
| movTempBens | 1 – Não | [INFERIDO] |
| Validação | Não revisado por contador | — |

### Caso 2 – Mesma formação, contratante no Brasil
- Não é exportação. cIndOp 100301; tribISSQN 1. CST/cClassTrib do MEI em operação interna: [LACUNA].

### Caso 3 – Contratante em Portugal, participantes no Brasil
- Não é exportação para IBS/CBS (destinatário no Brasil). cIndOp 100302. ISS devido (resultado no Brasil).

### Caso 4 – Formação presencial no Brasil
- Não é exportação (serviço fruído presencialmente no Brasil, art. 11, III). cIndOp 030101 ou 030102, conforme o local. CST/cClassTrib: [LACUNA], como no Caso 2.

---

## 7. Lacunas (sempre encaminhar ao contador)

1. CST e cClassTrib do MEI em operações no mercado interno, em 2026 e a partir de 2027.
2. Escolha entre 410027 e 410004 na exportação de serviços.
3. Valor de `regApIBSCBSSN` e `cAtvSN` para o MEI.
4. Tratamento da receita de exportação no limite anual do MEI. Para ME/EPP há regra expressa (Res. CGSN 140/2018, art. 25, § 4º-B, redação da Res. CGSN 190/2026); para o MEI, não foi localizada regra oficial equivalente.
5. Conceito de "resultado" para ISS em serviços com efeitos nos dois países.
6. Aplicação de reduções de alíquota (educação, saúde) ao MEI.
7. Escolha do campo `mdic` (enviar ou não ao MDIC).
8. NBS exata quando o Anexo VIII lista mais de uma opção para o mesmo código de tributação.
9. Serviço que não corresponde a nenhuma ocupação permitida ao MEI.

---

## 8. Erros e alertas frequentes

| Situação | Alerta da skill |
|---|---|
| Tomador quer reter ISS de MEI | MEI não sofre retenção de ISS (LC 123/2006, art. 21, § 4º, IV; Res. CGSN 140/2018, art. 103, IV) |
| Local de incidência preenchido em exportação | Rejeição E1301 [CONFIRMAR NO ANEXO VI] |
| Município do tomador diferente do cadastro CNPJ/CPF | Rejeição pela validação cadastral (NT 009, item 2.10) |
| NBS ausente em exportação | Rejeição por falta de NBS [CONFIRMAR NO ANEXO VI] |
| Exportação com uso da emissão simplificada | Grupo de comércio exterior só existe na emissão completa |
| Conteúdo antigo citando "presunção pelo domicílio do adquirente" | Revogado pela LC 227/2026 |
| cIndOp 100401 usado em exportação remunerada | Incorreto: 100401 é para operação não onerosa |

---

## 9. Fontes

### 9.1 Oficiais (únicas que podem ser citadas como fundamento)

**Leis (Planalto, texto compilado)**
- LC 214/2025 – IBS/CBS (arts. 8º, 11, 12, 41, 79 e 80, com redação da LC 227/2026): https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp214.htm
- LC 123/2006 – Simples Nacional e MEI (arts. 18-A e 21, § 4º): https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm
- LC 116/2003 – ISS (art. 2º e lista de serviços): https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp116.htm

**Diário Oficial da União e normas infralegais**
- Res. CGSN 190/2026 (DOU 10/08/2026, seção 1 Extra A, p. 1): https://www.in.gov.br/web/dou/-/resolucao-cgsn-n-190-de-4-de-agosto-de-2026-724454118
- Res. CGSN 191/2026 (DOU 10/08/2026): cópia publicada pela Secretaria de Economia do DF: https://economia.df.gov.br/documents/d/seec/resol-cgsn-n-191-2026-pdf
- Ato Conjunto RFB/CGIBS nº 4/2026 (DOU 31/07/2026): resumo oficial da Secretaria de Economia do DF: https://www.economia.df.gov.br/documents/d/seec/_notas-fiscais_-conheca-o-cronograma-da-obrigatoriedade-de-emissao_-1-
- Res. CGSN 140/2018 (texto consolidado): http://normas.receita.fazenda.gov.br (busca por "Resolução CGSN nº 140")

**Portal Nacional da NFS-e**
- Documentação RTC (notas técnicas e anexos): https://www.gov.br/nfse/pt-br/biblioteca/documentacao-tecnica/rtc
- Nota Técnica SE/CGNFS-e nº 009 v1.01: https://www.gov.br/nfse/pt-br/biblioteca/documentacao-tecnica/rtc/nota-tecnica-009-se-cgnfs-e-v-1-01.pdf
- Atualizações e Implantações: https://www.gov.br/nfse/pt-br/biblioteca/documentacao-tecnica/atualizacoes-e-implantacoes
- Legislação Aplicável ao MEI: https://www.gov.br/nfse/pt-br/biblioteca/legislacao-aplicavel-ao-mei
- Lista de serviços (Código de Tributação Nacional de 6 números, em texto na página): https://www.gov.br/nfse/pt-br/mei-e-demais-empresas/codigos-de-tributacao-nacional-nbs
- Anexo VII v1.03.00 (cIndOp): https://www.gov.br/nfse/pt-br/biblioteca/documentacao-tecnica/rtc/anexovii-indop_ibscbs_v1-03-00-nt009.xlsx
- Anexo VIII v1.01.00 (correlação item × NBS × cClassTrib × cIndOp): https://www.gov.br/nfse/pt-br/biblioteca/documentacao-tecnica/rtc/anexoviii-correlacaoitemnbsindopcclasstrib_ibscbs_v1-01-00.xlsx

**Tabela oficial da NBS (MDIC)**
- NBS 2.0 em CSV (texto): https://www.gov.br/mdic/pt-br/assuntos/sdic/comercio-e-servicos/nbs-nomenclatura-brasileira-de-servicos/arquivos/nbs2-0.csv
- Página do arquivo, com a data de atualização: https://www.gov.br/mdic/pt-br/assuntos/sdic/comercio-e-servicos/nbs-nomenclatura-brasileira-de-servicos/arquivos/nbs2-0.csv/view

**Calculadora e tabelas oficiais de IBS/CBS**
- Tabela CST e cClassTrib (calculadora; a página carrega o conteúdo depois de abrir e pode aparecer vazia na leitura automática): https://consumo.tributos.gov.br/servico/calcular-tributos-consumo/calculadora/classificacoestributarias
- Tabela de classificação tributária do ambiente nacional de documentos fiscais (SVRS), com os códigos em texto: https://dfe-portal.svrs.rs.gov.br/DFE/TabelaClassificacaoTributaria

### 9.2 Não oficiais (usadas só para localizar normas; nunca citar como fundamento)

| Fonte | Usada para | Situação |
|---|---|---|
| LegJur (art. 80 da LC 214 consolidado) | Localizar o § 1º-A e as revogações | Confirmado no Planalto |
| Cópia em PDF do DOU (Rota da Jurisprudência) | Ler o texto da Res. CGSN 190/2026, pois o site do DOU bloqueia acesso automatizado | Texto idêntico ao DOU; citar o DOU |
| Buscador NCM (erro E1301 e tabela cIndOp) | Localizar regras de negócio | Tabela cIndOp substituída pelo Anexo VII oficial em 14/10/2026. Erro E1301: conferir no Anexo VI |
| Fontes secundárias sobre valores do Anexo XIII | Valores de IBS/CBS do Simei | [SEM FONTE OFICIAL] até conferência |
| Materiais sobre Siscoserv (modos GATS) | Interpretar `mdPrestacao` | [INFERIDO] |
| Conjur (jurisprudência do STJ sobre ISS) | Contexto do conceito de "resultado" | Apenas contexto; caso concreto vai ao contador |
