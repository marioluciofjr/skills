## Description: <br>
Orienta o MEI (Microempreendedor Individual) a preencher os códigos da emissão completa da NFS-e nacional a partir do serviço prestado, indicando Código de Tributação Nacional, Código na NBS, Indicador de Operação, CST e cClassTrib do IBS/CBS, inclusive em exportação de serviço. <br>

This skill is ready for commercial/non-commercial use. <br>

## Autoria
Skill desenvolvida por Mário Lúcio; veja o repositório [Mário Lúcio Agent Card](https://github.com/marioluciofjr/skills). <br>

### License/Terms of Use: <br>
<span style="color:#d73a49">Apache 2.0</span> <!-- VERIFY: Licença herdada do repositório marioluciofjr/skills, onde a skill será publicada; a pasta da skill não tem arquivo LICENSE próprio. Confirmar antes de publicar. --> <br>
## Use Case: <br>
Pessoas usuárias de IAs generativas e/ou interfaces agênticas que permitam o uso de skills para ampliar as capacidades dos modelos generativos, em especial MEIs que precisam escolher os códigos da NFS-e no Emissor Nacional, inclusive IBS/CBS e exportação de serviço, com aviso obrigatório de consulta a uma pessoa contadora. <br>

### Deployment Geography for Use: <br>
Brasil <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [Base de conhecimento: MEI e NFS-e Nacional](references/base-conhecimento-mei-nfse.md) <br>
- [Manifesto de versões das fontes oficiais](references/manifest.json) <br>
- [Roteiro de perguntas ao MEI](references/perguntas-mei.md) <br>
- [Glossário para o MEI](references/glossario.md) <br>
- [Cópia da lista oficial de Códigos de Tributação Nacional](references/tabelas/codigos-tributacao-nacional.csv) <br>
- [Cópia do Anexo VIII (subitem x NBS)](references/tabelas/anexo-viii-item-nbs.csv) <br>
- [Formato da resposta final](assets/formato-saida.md) <br>
- [Portal NFS-e - Documentação técnica RTC](https://www.gov.br/nfse/pt-br/biblioteca/documentacao-tecnica/rtc) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis] <br>
**Output Format:** [Texto em Markdown: verificação de atualização, resumo do serviço, cinco códigos com O que é, Justificativa (até 50 palavras), Certeza e Fonte, outros campos da emissão completa, alertas e aviso final de consulta a uma pessoa contadora.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Códigos das tabelas incorporadas passam por conferência na fonte oficial; sem conferência, a certeza máxima é 'Confira no Emissor Nacional'. Nenhum código é indicado fora da base ou das tabelas; sem código seguro, a saída mostra 'Não indicado'.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter) <br>


