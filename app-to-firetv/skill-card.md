## Description: <br>
Cria um app Android (APK) para Amazon Fire TV a partir da descrição da pessoa usuária, com interface para TV navegável pelo controle remoto e no design system escolhido, e depois orienta a publicar o APK no Google Drive e a encurtar o link em https://go.aftvnews.com para instalar pelo app Downloader. <br>

This skill is ready for commercial/non-commercial use. <br>

## Autoria
Skill desenvolvida por Mário Lúcio; veja o repositório [Mário Lúcio Agent Card](https://github.com/marioluciofjr/skills). <br>

### License/Terms of Use: <br>
## Use Case: <br>
Pessoas usuárias de IAs generativas e/ou interfaces agênticas que permitam o uso de skills para ampliar as capacidades dos modelos generativos, e que querem transformar a descrição de um app, jogo ou painel num APK instalável na Amazon Fire TV, com interface navegável pelo controle remoto, e publicá-lo no Google Drive com um código curto do go.aftvnews.com para instalar pelo app Downloader. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [references/licoes.md: lições que originaram a skill](references/licoes.md) <br>
- [references/regras-tv.md: regras de UI, UX e CX para TV](references/regras-tv.md) <br>
- [references/publicacao-drive-aftvnews.md: Drive, go.aftvnews.com e Downloader](references/publicacao-drive-aftvnews.md) <br>
- [references/solucao-de-problemas.md: sintomas na TV e no build](references/solucao-de-problemas.md) <br>
- [scripts/firetv_build.py: ambiente, keystore, projeto, ícones, empacotamento, verificação e link do Drive](scripts/firetv_build.py) <br>
- [scripts/testar_interface.py: teste da interface com Playwright](scripts/testar_interface.py) <br>
- [assets/index-base.html: esqueleto de interface para TV](assets/index-base.html) <br>
- [Apktool v2.10.0](https://github.com/iBotPeaches/Apktool/releases/tag/v2.10.0) <br>
- [uber-apk-signer v1.3.0](https://github.com/patrickfav/uber-apk-signer/releases/tag/v1.3.0) <br>
- [Encurtador da AFTVnews para o Downloader](https://go.aftvnews.com) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions] <br>
**Output Format:** [Arquivo APK assinado (v1, v2 e v3) em <W>/out/<slug>_v<versao>.apk, keystore PKCS12 com arquivo de senha na primeira versão, capturas de tela da interface e orientações em Markdown para publicar no Google Drive e encurtar no go.aftvnews.com] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Os scripts imprimem JSON com success e details. O apktool e o uber-apk-signer são baixados do GitHub com verificação SHA-256 fixada; Pillow e Playwright ficam num ambiente virtual próprio. A senha da keystore vai para um arquivo e nunca para o chat. O app gerado é um WebView com um HTML autocontido, sem internet, a não ser que a permissão seja pedida. Funciona no Linux (claude.ai) e no Windows. Resposta em português do Brasil, sem emojis.] <br>

## Evaluation Agents Used: <br>
- Claude Code (`claude-opus-5-5`) <br>



## Evaluation Tasks: <br>
Execução de ponta a ponta no Windows 11 com Java 8: preparo do ambiente, keystore, projeto, ícones, teste da interface, empacotamento da versão 1.0.0 e da atualização 1.1.0 com a mesma keystore, teste negativo de certificado e conversão de links do Drive (arquivo, open?id, pasta e domínio externo). <br>

## Evaluation Metrics Used: <br>
Underlying evaluation signals used in this run: <br>
- `sha256_toolchain`: Os JARs do apktool e do uber-apk-signer conferem com os SHA-256 fixados (GitHub, Bitbucket e checksum oficial). <br>
- `interface_tv`: Sem erros de JavaScript, palco dentro da tela e exatamente um foco em cada passo, em 960x540 e 1280x720. <br>
- `assinatura_apk`: Saída do uber-apk-signer com zipalign verified e signature verified [v1, v2, v3]. <br>
- `atualizacao_por_cima`: Versão nova com versionCode maior e o mesmo SHA-256 de certificado; certificado diferente é recusado. <br>
- `link_drive`: Link de arquivo vira uc?export=download&id=; link de pasta e de outro domínio são recusados com explicação. <br>



## Evaluation Results: <br>
| Verificação | Casos | Resultado |
|---|---:|---:|
| SHA-256 do toolchain | 2 | 2 de 2 |
| Passos do teste de interface | 18 | 18 de 18 |
| Critérios de aceite do APK (v1 e v2) | 2 | 2 de 2 |
| Teste negativo de atualização | 1 | recusado como esperado |
| Conversão de links do Drive | 4 | 4 de 4 |

## Skill Version(s): <br>
2.0.0 (source: refatoração de 25/10/2026; a versão anterior era um SKILL.md único sem número de versão) <br>


