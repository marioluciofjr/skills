## Description: <br>
Skill para buscar e comentar as checagens de fatos mais recentes do portal Aos Fatos (aosfatos.org), filtrando por selo de veracidade (verdadeiro, falso, não é bem assim), formato de conteúdo, ano e/ou canal temático — combináveis entre si (ex: formato + ano + selo) — ou a partir da descrição livre de algo que a pessoa ouviu e quer verificar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Third-Party Community Consideration
<span style="color:#d73a49">This skill is not owned or developed by NVIDIA. This skill has been developed and built to a third-party's requirements for this application and use case; see link to Non-NVIDIA [Mário Lúcio Agent Card](https://github.com/marioluciofjr/skills).</span> <!-- VERIFY: Owner extraído do campo 'author' do frontmatter do SKILL.md. O link aponta para o repositório GitHub onde o autor publica suas skills (fluxo padrão da rotina-pos-skill), não um card de agente dedicado — confirmar se é a referência correta antes de publicar. --> <br>

### License/Terms of Use: <br>
## Use Case: <br>
Pessoas usuárias de harnesses de IA (Claude Code, Antigravity/Gemini, Opencode) que querem consultar rapidamente checagens de fatos recentes do Aos Fatos, filtradas por veracidade, ano, canal temático ou por uma descrição livre de algo que ouviram e querem verificar. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [Mapa de URLs do Aos Fatos](references/mapa_urls.md) <br>
- [Exemplos de saída](assets/exemplo_saida.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis] <br>
**Output Format:** [Texto em Markdown: até 12 blocos por notícia (título, comentário de até 100 palavras e link de origem), seguidos de um disclaimer único ao final.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Máximo de 12 itens por resposta; nenhum item é apresentado sem um link real e verificado em aosfatos.org.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter) <br>


