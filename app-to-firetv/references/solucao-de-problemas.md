# Solução de problemas

## Na Fire TV

| Sintoma | Causa provável | Ação |
|---|---|---|
| "O aplicativo não foi instalado" | Assinatura inválida, chave diferente da versão instalada ou `versionCode` menor | Reassinar com a keystore original (subcomando `empacotar`). Se a chave foi perdida, desinstalar o app antigo antes. Aumentar o `versionCode`. |
| O Downloader baixa um arquivo pequeno ou uma página HTML | Link de pasta, arquivo privado ou página de aviso do Drive (arquivos acima de cerca de 100 MB) | Usar o link de `link-drive`, compartilhar como "Qualquer pessoa com o link" e manter o APK pequeno |
| "Opções do desenvolvedor" não aparece | Fire OS recente esconde o menu | Configurações > Minha Fire TV > Sobre: selecionar o primeiro item várias vezes até o aviso aparecer |
| O app instala, mas não abre | Binário inválido (montado à mão) ou erro na Activity | Reconstruir com `projeto` e `empacotar`. Para ver o erro, ativar a depuração ADB na TV e rodar `adb logcat` num computador |
| Tela cortada ou elementos fora da tela | Layout em px/vh sem escala ou overscan da TV | Usar o palco escalado com `fitStage()` e aumentar a "Margem da tela" no app |
| Teclas do controle não respondem | `window.fireTvKey` indefinido ou zona de foco errada | Conferir a definição global antes do primeiro render e rodar `testar_interface.py` |
| Símbolo aparece como emoji colorido | Falta o seletor de texto U+FE0E | Acrescentar `︎` logo depois do glifo |

## No computador (build)

| Sintoma | Causa provável | Ação |
|---|---|---|
| "SHA-256 de ... não confere" | Download corrompido ou adulterado | O script já descartou o arquivo. Rodar `ambiente` de novo; se repetir, não prosseguir e avisar a pessoa |
| "keytool não encontrado" | Java sem o keytool no PATH ou não instalado | Instalar um JDK ou JRE 8 ou mais novo; o script procura também em `JAVA_HOME` e nas pastas comuns do Java |
| `ambiente --instalar` falha com "Connection broken" | Queda de rede no download do pip ou do Chromium | Rodar de novo; o pip já tenta várias vezes |
| `apktool falhou` | Erro de sintaxe no smali, no XML ou nome de recurso inválido | Ler o fim do log devolvido no JSON e corrigir o arquivo apontado |
| Critério `index_html_identico` falso | O `index.html` mudou depois do build | Rodar `empacotar` de novo |
