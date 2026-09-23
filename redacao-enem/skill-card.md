## Description: <br>
Gera uma proposta de redação inédita no modelo do Enem, com uma orientação curta de envio, quatro textos motivadores copiados literalmente de fontes confiáveis verificadas na web e um tema sorteado no contexto brasileiro. <br>

This skill is ready for commercial/non-commercial use. <br>

## Owner
Mário Lúcio — skill pessoal, sem vínculo com a NVIDIA ou qualquer terceiro corporativo. <br>

### License/Terms of Use: <br>
Nenhuma licença formal definida (skill de uso pessoal, não distribuída sob licença de código aberto). <br>

## Use Case: <br>
Pessoas usuárias de IAs generativas e/ou interfaces agênticas que permitam o uso de skills para ampliar as capacidades dos modelos generativos, em especial estudantes e professores que preparam o Enem, usam esta skill para obter propostas de redação inéditas, com textos motivadores reais e verificáveis, para treino de escrita. <br>

### Deployment Geography for Use: <br>
Brasil <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [Fontes confiáveis e protocolo de verificação](references/fontes-confiaveis.md) <br>
- [50 padrões de textos motivadores](references/padroes-de-textos-motivadores.md) <br>
- [50 padrões de temas e apêndice de temas já aplicados](references/padroes-de-temas.md) <br>
- [Cartilha do Participante Enem 2026 (trechos)](references/cartilha-enem-2026.md) <br>
- [Transcrições das propostas oficiais 2017–2025](references/provas/) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis] <br>
**Output Format:** [Markdown seguindo o template assets/instrucoes-redacao-enem.md (Instruções → Textos I a IV → Proposta), sem texto adicional] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exige ferramenta de busca e navegação web; sem ela, devolve apenas uma mensagem de recusa padronizada. Somente leitura: não escreve arquivos nem executa comandos. Trechos verbais de 70 a 85 palavras e tabelas de até 5 linhas; fluxo em duas fases (pesquisa e validação → emissão) com orçamento de até 8 buscas e 10 aberturas de página por tema.] <br>

## Evaluation Agents Used: <br>
- Claude (`claude-opus-5-5`) <br>



## Evaluation Tasks: <br>
Execução manual do fluxo da skill em 23/09/2026: geração de 1 proposta de teste com checagem literal de cada trecho no HTML bruto da fonte, verificação de acesso público de 124 domínios candidatos e auditoria com skill-injection-auditor. <br>

## Evaluation Results: <br>
| Verificação | Resultado |
|---|---|
| Trechos literais conferidos no HTML da fonte | 4 de 4 |
| Domínios das fontes na lista autorizada | 4 de 4 |
| Tema fora do apêndice de temas já aplicados | Sim |
| Fontes de Nível A com acesso público verificado | 100 |
| Auditoria de injeção (heurística + revisão manual) | Seguro (9 alertas falso-positivos: URLs de citações) |

## Skill Version(s): <br>
1.2.0 (source: frontmatter) <br>


