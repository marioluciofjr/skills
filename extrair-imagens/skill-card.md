## Description: <br>
Extrai as imagens e demais mídias incorporadas (pasta ppt/media) de apresentações do Google Slides (link ou atalho .gslides) ou de arquivos PowerPoint (.pptx, .pptm, .ppsx, .potx) enviados na conversa, e entrega a pasta media pronta para uso. <br>

This skill is ready for commercial/non-commercial use. <br>

## Autoria
Skill desenvolvida por Mário Lúcio; veja o repositório [Mário Lúcio Agent Card](https://github.com/marioluciofjr/skills). <br>

### License/Terms of Use: <br>
<span style="color:#d73a49">Apache 2.0</span> <!-- VERIFY: Licença herdada do repositório marioluciofjr/skills; a pasta da skill não declara licença própria. Confirmar antes de publicar. --> <br>
## Use Case: <br>
Pessoas usuárias de IAs generativas e/ou interfaces agênticas que permitam o uso de skills para ampliar as capacidades dos modelos generativos: obter, numa pasta pronta para uso, todas as imagens e mídias incorporadas de uma apresentação do Google Slides ou de um arquivo PowerPoint. A skill começa por uma triagem do ambiente. Na categoria 'consegue pelo endpoint', o ambiente baixa a apresentação direto pelo endereço /export/pptx do Google, sem o limite de 10 MB dos conectores, desde que o link esteja como 'Qualquer pessoa com o link' e 'Leitor'; agentes que controlam o navegador logado da pessoa fazem o ciclo completo: liberam o link, baixam, extraem, voltam o link para 'Restrito' e confirmam o bloqueio. Na categoria 'não consegue pelo endpoint', o agente pede imediatamente o arquivo .pptx na conversa e extrai a pasta media a partir dele. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [acesso-google-slides.md](references/acesso-google-slides.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands] <br>
**Output Format:** [Pasta media descompactada ou arquivo media.zip, com resumo em texto simples (quantidade de arquivos, tamanho total e contagem por tipo)] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Triagem do ambiente em JSON (consegue_endpoint ou nao_consegue_endpoint, link_liberado); download somente leitura pelo endpoint /export/pptx, restrito a domínios do Google; códigos de saída por tipo de falha; extração com conferência SHA-256; script Python só com biblioteca padrão] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter) <br>


