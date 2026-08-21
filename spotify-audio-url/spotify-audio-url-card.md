## Description: <br>
Resolve um link de episodio do Spotify para a URL direta do arquivo de audio publicada no feed RSS aberto do podcast, ou recusa quando o conteudo nao possui feed publico. <br>

This skill is for research and development only. <br>

## Third-Party Community Consideration
This skill is not owned or developed by NVIDIA. This skill has been developed and built to a third-party's requirements for this application and use case; see link to Non-NVIDIA [Mario Agent Card](Nao publicado — skill criada localmente, sem card de terceiro associado.). <br>

### License/Terms of Use: <br>
CC-BY-4.0 <br>
## Use Case: <br>
Pessoas que ouvem podcasts pelo Spotify e precisam do arquivo de audio original para escutar offline, arquivar ou transcrever. A skill decide se o episodio vem de um feed RSS aberto e, em caso positivo, entrega apenas a URL do arquivo; caso contrario, recusa com uma frase fixa. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [RSS 2.0 Specification - enclosure element](https://www.rssboard.org/rss-specification) <br>
- [Apple Podcasts - RSS feed requirements](https://podcasters.apple.com/support/823-podcast-requirements) <br>


## Skill Output: <br>
**Output Type(s):** [Text] <br>
**Output Format:** [Uma unica linha por link de entrada: a URL absoluta do arquivo de audio, ou a frase de recusa fixa.] <br>
**Output Parameters:** [Entrada: uma ou mais URLs open.spotify.com de episodio. Sem outros parametros.] <br>
**Other Properties Related to Output:** [Sem preambulo, sem comandos de shell, sem endereco do feed e sem metadados do episodio na saida. A URL e entregue sem query string de rastreamento.] <br>

## Skill Version(s): <br>
1.0.0 <br>


