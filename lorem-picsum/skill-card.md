## Description: <br>
Skill para gerar links de imagens do serviço Lorem Picsum (picsum.photos), aleatórias ou customizadas por tamanho, id, seed, escala de cinza e blur, além de consultar o acervo paginado e os detalhes técnicos de uma imagem específica. <br>

This skill is ready for commercial/non-commercial use. <br>

## Third-Party Community Consideration
<span style="color:#d73a49">This skill is not owned or developed by NVIDIA. This skill has been developed and built to a third-party's requirements for this application and use case; see link to Non-NVIDIA [Mário Lúcio Agent Card](https://github.com/marioluciofjr/skills).</span> <!-- VERIFY: Owner extraído do campo 'author' do frontmatter do SKILL.md. O link aponta para o repositório GitHub onde o autor publica suas skills (fluxo padrão da rotina-pos-skill), não um card de agente dedicado — confirmar se é a referência correta antes de publicar. --> <br>

### License/Terms of Use: <br>
## Use Case: <br>
Pessoas usuárias de IAs generativas e/ou interfaces agênticas que permitam o uso de skills para ampliar as capacidades dos modelos generativos, e que querem gerar rapidamente links de imagens placeholder do Lorem Picsum — aleatórias ou customizadas por tamanho, id, seed, escala de cinza e blur — para mockups, protótipos e testes visuais, além de consultar o acervo paginado ou os detalhes técnicos de uma imagem específica. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [Mapa de URLs do Lorem Picsum](references/mapa_urls_picsum.md) <br>
- [Exemplos de saída](assets/exemplo_saida.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls] <br>
**Output Format:** [Texto em Markdown: preview embutido (`![](url)`) e link em texto puro para cada imagem no subcomando imagem; tabela Markdown no subcomando lista; lista de definição no subcomando info. O script sempre retorna JSON estruturado como saída intermediária antes dessa formatação.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Máximo de 30 imagens por pedido (subcomando imagem, padrão 3); máximo de 100 itens por página (subcomando lista, padrão 30). O script nunca acessa a rede: imagem já entrega links prontos; lista e info entregam a URL a buscar, e a busca real é feita pela ferramenta de fetch nativa do agente (mesmo padrão da skill aos-fatos deste projeto), o que torna a skill compatível com harnesses que restringem scripts com acesso à internet (ex: Gemini Spark).] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter) <br>


