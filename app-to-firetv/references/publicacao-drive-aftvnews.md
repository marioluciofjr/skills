# Publicar no Google Drive e encurtar no go.aftvnews.com

Passo a passo para a pessoa usuária, depois que o APK foi entregue. Apresente de forma objetiva, sem pular etapas.

## Enviar e compartilhar no Drive

1. **Enviar ao Drive:** faça o upload do APK, de preferência numa pasta só para os apps da Fire TV.
2. **Compartilhar:** clique com o botão direito no arquivo, vá em **Compartilhar** e, em **Acesso geral**, escolha **Qualquer pessoa com o link**, com a função **Leitor**. Sem isso, o Downloader recebe a página de login do Google em vez do APK.
3. **Copiar o link do arquivo:** use **Compartilhar > Copiar link** no próprio arquivo. O link tem o formato `https://drive.google.com/file/d/<ID>/view?...`. Um link de **pasta** (`/drive/folders/...`) não funciona.

## Montar o link direto e encurtar

4. **Link direto:** rode `python scripts/firetv_build.py link-drive "<link copiado>"`. O script devolve `https://drive.google.com/uc?export=download&id=<ID>` e recusa link de pasta com uma explicação. Esse é o link que vai no encurtador.
5. **Encurtar:** em https://go.aftvnews.com, cole o link direto e gere o código numérico.

## Instalar na Fire TV

6. **Instalar o Downloader:** pela loja da Amazon na Fire TV, instale o app **Downloader** (da AFTVnews).
7. **Exibir as Opções do desenvolvedor, se estiverem escondidas:** em **Configurações > Minha Fire TV > Sobre**, selecione o primeiro item da lista (o nome do aparelho) várias vezes seguidas, até aparecer o aviso de que as opções de desenvolvedor foram ativadas. Nas Smart TVs Fire TV, o caminho é **Configurações > Dispositivo e software > Sobre**.
8. **Autorizar o Downloader:** em **Configurações > Minha Fire TV > Opções do desenvolvedor > Instalar apps desconhecidos**, ative o **Downloader**.
9. **Instalar o app:** abra o Downloader, digite o código numérico e confirme a instalação.

## Atualizações

- Para manter o mesmo link e o mesmo código curto, no Drive use **Gerenciar versões > Enviar nova versão** no arquivo existente, em vez de enviar um arquivo novo. Um arquivo novo gera outro ID e exige outro código curto.
- A nova versão só instala por cima se usar a **mesma keystore** e um **versionCode maior**. O subcomando `empacotar` confere os dois quando recebe `--version-code-anterior` e `--cert-anterior`.

## Quando há um conector do Google Drive disponível

Ajude ativamente, sem alterar nada sem autorização:

- quando a pessoa mandar um link (de pasta ou de arquivo), localize o APK com a busca do conector (`search_files`, com `parentId` igual ao ID da pasta) e confira com `get_file_metadata` se o tamanho bate com o APK gerado;
- verifique com `get_file_permissions` se há permissão `anyone` com papel `reader`;
- devolva o link `uc?export=download&id=` já montado;
- se o arquivo estiver privado, avise e ofereça alterar a permissão. **Só altere se a pessoa autorizar.**
