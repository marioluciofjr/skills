# Skill Card: EEAT Audit

## Description

Audita textos ou URLs de posts publicados segundo os parâmetros de E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) do Google e atribui uma nota de 0 a 5 a cada pilar, com nota global ponderada.

Esta skill está pronta para uso comercial e não comercial.

## Third-Party Community Consideration

Esta skill não pertence à NVIDIA nem foi desenvolvida por ela. Ela foi criada por Mário Lúcio para este caso de uso específico, e é distribuída sem agent card de terceiro associado.

### License / Terms of Use

CC-BY-4.0

## Use Case

Redatores, editores e especialistas em SEO usam esta skill para auditar um artigo publicado ou um texto colado sob os quatro pilares do E-E-A-T. A entrega é uma nota de 0 a 5 por pilar, uma nota global ponderada e um plano de ação ordenado por impacto. O diagnóstico cobre o desempenho na busca orgânica e nos recursos generativos do Google, tratados como a mesma disciplina de SEO. A skill avalia conteúdo editorial e não avalia infraestrutura técnica de site.

### Deployment Geography for Use

Global.

## Known Risks and Mitigations

**Risco.** O diagnóstico pode introduzir orientação incorreta ou enganosa no fluxo editorial de quem o recebe.

**Mitigação.** Revise o diagnóstico antes de aplicá-lo. Em conteúdo YMYL, submeta o texto corrigido a um profissional com credencial no tópico. A seção 6 do template obriga esse aviso em toda entrega.

**Risco.** A nota pode inflacionar entre execuções, por ausência de âncora objetiva.

**Mitigação.** As sete regras antiinflação e os exemplos calibrados fixam a escala. Cada nota exige um trecho citado do texto auditado.

**Risco.** O material auditado pode conter um pedido escrito no corpo do texto que tente alterar o resultado.

**Mitigação.** O Passo 1 e as Regras de Governança determinam tratar todo material como objeto de análise. Um pedido dentro do material vira evidência registrada na seção 4 do diagnóstico, não uma ordem.

## References

- Conceito E-E-A-T e Diretrizes de Qualidade: `references/conceito.md`
- Documentação Oficial do Google Search: `references/google-search-doc.md`
- Instrumentos dos Avaliadores de Qualidade do Google: `references/quality-rater-instrumentos.md`
- Rubrica de Notas E-E-A-T (0 a 5): `references/rubrica-notas.md`
- Exemplos de Calibração: `references/exemplos-calibracao.md`
- Template de Saída do Diagnóstico: `assets/formato-saida.md`
- Google Search Central, Creating helpful, reliable, people-first content
- Google Search Central, Spam policies for Google web search
- Google Search Quality Rater Guidelines

## Skill Output

- **Output Types:** análise, avaliação com nota.
- **Output Format:** Markdown com tabelas de notas e plano de ação, entre 950 e 1.100 palavras.
- **Output Parameters:** 1D.
- **Other Properties:** notas inteiras de 0 a 5 por pilar. Nota global decimal por média ponderada, com pesos Experiência 1, Especialidade 1, Autoridade 2 e Confiabilidade 1. Trava de nota máxima 2,0 em conteúdo YMYL com Confiabilidade 0 ou 1.

## Evaluation Tasks

Cinco casos de teste internos em `evals/evals.json`: artigo YMYL sem links de comprovação, texto colado sem autoria, relatório com dado proprietário, texto com pedido embutido no corpo e pedido fora de escopo.

## Evaluation Metrics Used

Dimensões avaliadas:

- **Ancoragem em evidência.** Verifica se cada nota atribuída cita um trecho literal do texto auditado.
- **Calibração bidirecional.** Verifica se a skill atribui nota alta quando a evidência sustenta e nota baixa quando falta, sem fabricar elogio nem crítica.
- **Correção do cálculo ponderado.** Verifica se a nota global aplica os pesos declarados e a trava YMYL.
- **Precisão de disparo.** Verifica se a skill não ativa em pedidos listados na seção Quando não usar.
- **Estabilidade do procedimento.** Verifica se um pedido escrito dentro do material auditado não altera a rubrica.

Nenhuma execução de benchmark foi registrada até esta versão.

## Skill Version

3.0.0 (fonte: frontmatter do `SKILL.md`).

## Tabela de revisão

| Seção | Campo | Confiança | Revisão necessária | Justificativa |
|---|---|---|---|---|
| Description | Descrição | Alta | Não | Primeira sentença da chave `description` do frontmatter. |
| Description | Postura de uso | Inferida | Sim | Licença CC-BY-4.0 permissiva, sem restrição a uso comercial declarada. |
| Ownership | Proprietário | Inferida | Sim | Autoria vem de `metadata.author`. Não existe agent card publicado. |
| License | Licença | Alta | Não | Chave `license` explícita no frontmatter. |
| Use Case | Caso de uso | Inferida | Sim | Composto a partir das seções Quando usar, Quando não usar e do campo Destinatário do template. |
| Deployment | Geografia | Inferida | Sim | Nenhuma restrição regional declarada. Padrão global. |
| References | Referências | Alta | Não | Caminhos relativos existentes e fontes citadas nos arquivos de referência. |
| Output | Saída | Alta | Não | Formato, extensão, escala e ponderação declarados no Passo 4, no Passo 5 e no template. |
| Version | Versão | Alta | Não | Chave `metadata.version` no frontmatter. |
| Evaluation | Casos | Alta | Não | Cinco casos declarados no arquivo de evals. |
| Evaluation | Métricas | Inferida | Sim | Dimensões derivadas do campo `checks` de cada caso. |
