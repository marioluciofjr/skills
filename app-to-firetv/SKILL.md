---
name: app-to-firetv
description: Cria um app Android (APK) para Amazon Fire TV a partir da descrição da pessoa usuária, com interface para TV navegável pelo controle remoto e no design system escolhido, e depois orienta a publicar o APK no Google Drive e a encurtar o link em https://go.aftvnews.com para instalar pelo app Downloader. Use sempre que a pessoa pedir um app, jogo, painel ou ferramenta para Fire TV, Fire Stick, Fire TV Cube ou Smart TV Fire TV, quiser gerar um APK para instalar na TV pelo Downloader, ou pedir ajuda para atualizar um app de Fire TV feito antes.
---

# app-to-firetv

Transforma a descrição de um app num APK instalável na Amazon Fire TV pelo Downloader. O app é uma Activity nativa mínima com um WebView que carrega `assets/index.html`, onde ficam toda a interface e a lógica. No fim, a skill orienta a pessoa usuária a subir o APK no Google Drive e a encurtar o link em https://go.aftvnews.com.

Responda sempre em português do Brasil, com tom profissional e objetivo, sem emojis. Antes de começar, leia `references/licoes.md`.

## Convenções

- `<SKILL>` é a pasta onde está este `SKILL.md`. Rode os scripts de lá: `python <SKILL>/scripts/firetv_build.py ...`.
- `<W>` é a pasta de trabalho do app: a pasta temporária (scratchpad) do ambiente, se houver, ou uma pasta indicada pela pessoa usuária.
- Todo script imprime um JSON com `success` e `details`. Leia o JSON e nunca declare sucesso se `success` for `false`.
- A skill roda no Linux (ambiente de código do claude.ai) e no Windows. Os scripts detectam o sistema sozinhos.
- Use as ferramentas que o ambiente oferecer: lista de tarefas, se existir; perguntas estruturadas, se existirem; senão, pergunte em texto.

## Fluxo

### 1. Levantar requisitos

Extraia da descrição o nome do app, o propósito, as telas, as ações principais, se precisa de internet e se precisa guardar dados. Se faltar algo essencial, pergunte (no máximo 4 perguntas, de uma vez):

- **Design system:** se houver uma ferramenta de Artifacts com design systems da pessoa, liste-os e ofereça-os como opções. Inclua sempre "Escuro padrão para TV (azul-marinho e dourado)" e "Material/Leanback escuro". Se ela escolher um design system existente, leia-o e converta cores, tipografia, raios e espaçamentos em tokens CSS.
- **Nome e package:** por padrão `com.firetv.<slug>`, com o slug em minúsculas, sem acentos e só com letras e números (ex.: `xadrez`).
- **Keystore:** se já existe uma de versões anteriores deste app, peça o arquivo `.p12` e o arquivo de senha. Sem eles, o app não atualiza por cima.

Se a pessoa não estiver presente para responder, use os padrões acima e informe a escolha no início da entrega.

### 2. Preparar o ambiente

```bash
python <SKILL>/scripts/firetv_build.py ambiente --instalar
```

- Confere o Java e o `keytool`.
- Baixa o apktool 2.10.0 e o uber-apk-signer 1.3.0 com verificação SHA-256: um arquivo adulterado é descartado.
- Prepara Pillow e Playwright num ambiente virtual próprio, sem alterar o Python do sistema.

Guarde o campo `python_para_icones_e_testes` do JSON e use esse Python nas etapas 6 e 7. Se o download falhar, avise a pessoa: não existe alternativa segura sem essas ferramentas, e montar o APK à mão está proibido.

### 3. Keystore

Primeira versão:

```bash
python <SKILL>/scripts/firetv_build.py keystore --slug <slug> --nome "<Nome do App>" --saida <W>/chaves
```

O script gera uma senha forte e grava a senha em `<slug>-keystore-senha.txt`, ao lado da `.p12`. **Nunca escreva a senha no chat.** Em atualizações, reaproveite a keystore e o arquivo de senha da versão anterior.

### 4. Gerar o projeto

```bash
python <SKILL>/scripts/firetv_build.py projeto --dir <W> --slug <slug> --nome "<Nome do App>" \
  --versao 1.0.0 --version-code 1 [--internet] [--html <arquivo.html>]
```

O script monta `<W>/proj` a partir dos modelos de `assets/`: o manifesto, o `apktool.yml`, o `strings.xml`, o `MainActivity.smali` (WebView em tela cheia, tela sempre ligada, teclas do controle enviadas ao JavaScript) e o `MainActivity$Client.smali` (fecha o app pelo endereço `<slug>://sair`). Também copia o esqueleto `assets/index-base.html` para `<W>/proj/assets/index.html`. Use `--internet` só se o app acessar conteúdo on-line. A cada nova versão, aumente o `--version-code`.

### 5. Construir a interface

Edite `<W>/proj/assets/index.html` seguindo `references/regras-tv.md`. O esqueleto já funciona: palco escalado com `fitStage()`, zonas de foco, menu lateral, margem da tela ajustável, confirmação de saída, toast, som opcional e retomada do estado. Troque os tokens CSS pelos do design system e o conteúdo de exemplo pelo app pedido, mantendo as regras. O arquivo final é um único HTML autocontido, sem CDN.

### 6. Ícone e banner

```bash
<python_para_icones_e_testes> <SKILL>/scripts/firetv_build.py icones --dir <W> --nome "<Nome do App>" \
  --fundo "#0a0f1a" --destaque "#f5b942" --texto "#f1f5f9" [--sigla XY]
```

Gera ícones de 96 e 192 px e o banner de 320x180 com arte original, nas cores do design system, nunca com logotipos ou personagens de terceiros. Abra os PNGs e confira antes de seguir.

### 7. Testar a interface (antes de empacotar)

```bash
<python_para_icones_e_testes> <SKILL>/scripts/testar_interface.py --html <W>/proj/assets/index.html \
  --saida <W>/shots --roteiro DOWN,RIGHT,SELECT,MENU,DOWN,BACK,BACK
```

- **O que o script faz:** abre a página em 960x540 (escala 2) e 1280x720 e simula o controle com `window.fireTvKey`.
- **O que ele confere a cada passo:** nenhum erro de JavaScript, palco inteiro dentro da tela, exatamente um elemento em foco e a retomada depois de recarregar.
- **Monte o `--roteiro`** para passar por todas as telas do app: menu, cada modal, estado vazio e estado de processamento.
- **Depois, abra as capturas** e confira: nada cortado, nada sobreposto, textos sem quebra indevida, foco sempre visível.
- Corrija e repita até ficar limpo.

### 8. Empacotar, assinar e verificar

```bash
python <SKILL>/scripts/firetv_build.py empacotar --dir <W> --slug <slug> --versao 1.0.0 --version-code 1 \
  --keystore <W>/chaves/<slug>-release.p12 --senha-arquivo <W>/chaves/<slug>-keystore-senha.txt
```

Em atualizações, acrescente `--version-code-anterior <n>` e `--cert-anterior <SHA-256 da versão anterior>`. Critérios de aceite, todos obrigatórios (o JSON precisa vir com `success: true`):

- `zipalign verified` e `signature verified [v1, v2, v3]`;
- package, `versionCode`, `LEANBACK_LAUNCHER`, ícone e banner conferidos no APK final;
- `index.html` empacotado idêntico ao do projeto;
- em atualizações, `versionCode` maior que o anterior e o mesmo certificado.

O APK final fica em `<W>/out/<slug>_v<versao>.apk`.

### 9. Entregar

- **APK:** envie-o como anexo, se o ambiente tiver uma ferramenta de envio de arquivos (no claude.ai, `SendUserFile` com `display: attach`). Senão, informe o caminho completo do arquivo. Mostre também uma captura da interface.
- **Primeira versão:** entregue a keystore e o arquivo de senha do mesmo jeito. Explique que os dois precisam ser guardados juntos para todas as atualizações, sem escrever a senha no chat.
- **Uso:** resuma em poucas linhas o que o app faz e como usar o controle.

### 10. Publicar no Drive e encurtar no go.aftvnews.com

Siga `references/publicacao-drive-aftvnews.md` e apresente os passos à pessoa usuária:

1. Enviar o APK ao Drive e compartilhar como **Qualquer pessoa com o link**, com a função **Leitor**.
2. Copiar o link do **arquivo** (não da pasta) e converter com `python <SKILL>/scripts/firetv_build.py link-drive "<link>"`.
3. Colar o link direto em https://go.aftvnews.com e gerar o código numérico.
4. Na Fire TV, instalar o Downloader, exibir as Opções do desenvolvedor (se estiverem escondidas), autorizar o Downloader a instalar apps desconhecidos, digitar o código e instalar.
5. Em atualizações, usar **Gerenciar versões > Enviar nova versão** no Drive para manter o mesmo código curto.

Se houver um conector do Google Drive, ajude a conferir o arquivo e a permissão, e **só altere a permissão com autorização explícita**.

## Regras

- Nunca monte binários Android à mão nem edite o APK fora do fluxo `projeto` → `empacotar`.
- Não altere os modelos smali sem necessidade. Se alterar, rode o fluxo completo e todos os critérios de aceite de novo.
- Peça a permissão de internet só quando o app precisar dela.
- Nunca escreva a senha da keystore no chat nem em resumos.
- Problemas na TV ou no build: consulte `references/solucao-de-problemas.md`.
