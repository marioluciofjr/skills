## Description: <br>
Anima elementos de uma imagem enviada (setas tracejadas andando, setas piscando no sentido em que apontam, cards se iluminando, destaques) e entrega um arquivo GIF em loop infinito, preservando o resto da imagem pixel a pixel, com tradução opcional dos textos da imagem antes da animação. <br>

This skill is ready for commercial/non-commercial use. <br>

## Third-Party Community Consideration
This skill is not owned or developed by NVIDIA. This skill has been developed and built to a third-party's requirements for this application and use case; see link to Non-NVIDIA [Mário Lúcio Agent Card](https://github.com/marioluciofjr/skills). <br>

### License/Terms of Use: <br>
## Use Case: <br>
Pessoas usuárias de IAs generativas e/ou interfaces agênticas que permitam o uso de skills para ampliar as capacidades dos modelos generativos, e que querem transformar uma imagem estática (diagrama, fluxograma, infográfico ou card) em um GIF animado, movimentando somente os elementos pedidos (setas tracejadas andando, setas piscando, cards se iluminando em sequência), e, quando pedirem, traduzir os textos da imagem para outro idioma antes de animar. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [scripts/medir.py: medição de pixels, cor da tinta, linhas de texto e recortes ampliados](scripts/medir.py) <br>
- [scripts/traduzir.py: tradução opcional dos textos da imagem](scripts/traduzir.py) <br>
- [scripts/gerar_gif.py: tracejado andando, seta piscante, card iluminado, montagem e verificação do GIF](scripts/gerar_gif.py) <br>
- [assets/exemplo_tracejado.json](assets/exemplo_tracejado.json) <br>
- [assets/exemplo_setas_e_cards.json](assets/exemplo_setas_e_cards.json) <br>
- [assets/exemplo_traducao.json](assets/exemplo_traducao.json) <br>
- [Pillow: formato GIF (save_all, loop, duration, disposal)](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif) <br>
- [OpenCV: Image Inpainting (cv2.inpaint, INPAINT_TELEA)](https://docs.opencv.org/4.x/df/d3d/tutorial_py_inpainting.html) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Analysis] <br>
**Output Format:** [Arquivo GIF animado na mesma resolução da imagem original, com loop infinito, acompanhado de uma tabela Markdown curta com resolução, quadros, duração por quadro, loop, elementos animados e blocos traduzidos (quando houver)] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tracejado: 12 quadros de 60 ms; animações em etapas: cerca de 6 quadros por etapa. Paleta única de até 256 cores, sem dithering; quando há brilho, a paleta é calculada do original mais uma amostra dos quadros. Arquivo acima de ~5 MB é reduzido. O agente mede a imagem e escreve especificações JSON; os scripts Python (Pillow, numpy, OpenCV) geram a imagem traduzida, o GIF e relatórios de verificação, que são intermediários. Os scripts não acessam a internet. A tradução só ocorre a pedido e depende de uma fonte com licença adequada. Resposta sem introdução, sem conclusão e sem emojis.] <br>

## Evaluation Agents Used: <br>
- Claude Code (`claude-opus-5-5`) <br>



## Evaluation Tasks: <br>
(1) Equivalência entre o script inline da versão 1.1.0 e os scripts em OOP, em imagem sintética e no diagrama real de 1100 x 906 px, repetida após a refatoração da versão 1.3.0. (2) Diagrama real com cinco setas tracejadas e uma ramificação em fundo colorido. (3) Infográfico JPEG de 982 x 1300 px diferente dos exemplos: tradução completa para o português do Brasil (33 blocos, incluindo título sobre marca-texto, rótulos girados e trechos coloridos), oito setas piscando (seis retas e duas em L) e sete cards iluminados em sequência. (4) Validação do frontmatter e varredura heurística de prompt injection. A versão 1.0.0 foi usada em produção no Claude Chat, segundo o autor. <br>

## Evaluation Results: <br>
| Verificação | Resultado |
|---|---|
| Equivalência script antigo x novo (sintética e diagrama real) | Idênticos pixel a pixel, antes e depois da refatoração 1.3.0 |
| Diagrama tracejado (7 caminhos) | 1100 x 906, 12 quadros, 60 ms, loop infinito, 0,81 MB, 0 pixels alterados fora da animação |
| Tradução do infográfico (33 blocos) | Todos couberam; 1 bloco reduzido (título azul, 47 para 43 px); 3 sobras de letras corrigidas na conferência visual |
| Setas piscantes e cards (infográfico traduzido) | 982 x 1300, 42 quadros, 90 ms, loop infinito, 2,47 MB, 0 pixels alterados fora da animação |
| Tempo de execução dos scripts | Tradução cerca de 2 s; GIF de 42 quadros cerca de 13 s |
| Frontmatter (validador do skill-creator) | Válido |
| Varredura heurística de injection | Sem alertas nos arquivos da skill; links de documentação no card são falso positivo |

## Skill Version(s): <br>
1.3.0 (source: frontmatter) <br>


