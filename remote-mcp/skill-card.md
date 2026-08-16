## Description: <br>
Automatiza a criação de um servidor MCP (Model Context Protocol) remoto do zero: a partir de um tema, faz 5 perguntas de verificação, apresenta uma ficha de aprovação (nome sugerido, tools, prompts e resources) e, após aprovação, gera a estrutura completa do projeto — servidor em FastMCP com transporte Streamable HTTP, README.md (já com o passo a passo de instalação no Gemini Spark, Claude Web e ChatGPT), requirements.txt, LICENSE e .gitignore, publicados num repositório GitHub e prontos para deploy na Vercel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Third-Party Community Consideration
This skill is not owned or developed by NVIDIA. This skill has been developed and built to a third-party's requirements for this application and use case; see link to Non-NVIDIA [Mário Lúcio Agent Card](https://github.com/marioluciofjr). <br>

### License/Terms of Use: <br>
## Use Case: <br>
Pessoas usuárias de IAs generativas e/ou interfaces agênticas que permitam o uso de skills para ampliar as capacidades dos modelos generativos, que queiram criar e publicar um servidor MCP (Model Context Protocol) remoto do zero — do tema à publicação num repositório GitHub, pronto para deploy na Vercel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [Guia técnico do MCP remoto](references/guia-tecnico-mcp-remoto.md) <br>
- [Checklist de entrega](references/checklist-entrega.md) <br>
- [Exemplo completo do pipeline](references/exemplo-generico.md) <br>
- [Documentação oficial do FastMCP](https://gofastmcp.com) <br>
- [Documentação oficial do Model Context Protocol](https://modelcontextprotocol.io) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions] <br>
**Output Format:** [Ficha de aprovação em Markdown; arquivos de projeto (server.py em Python, README.md em Markdown, requirements.txt, LICENSE, .gitignore); comandos de shell (git, gh)] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter) <br>


