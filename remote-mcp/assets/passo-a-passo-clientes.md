# Passo a passo fixo de instalação (Gemini Spark, Claude Web, ChatGPT)

Use estes três blocos sem reescrever no README de todo projeto gerado por esta skill. Troque só `{{URL_MCP}}` pela URL real do MCP depois do deploy na Vercel. Mantenha os nomes de botão entre aspas exatamente como estão — são rótulos da interface real, e traduzir ou reformular pode fazer a pessoa não encontrar o botão na tela.

Esta skill entrega sempre um MCP sem autenticação na conexão com o cliente (nenhum login/OAuth para usar o MCP) — é o que mantém o passo a passo abaixo simples e igual em todo projeto. Isso não impede a tool de usar uma chave de API para acessar a fonte de dados; essa chave fica guardada como variável de ambiente na Vercel, do lado do servidor, sem aparecer nesse passo a passo.

## Como instalar no Gemini Spark

O Gemini Spark é o modo agêntico do Gemini App.

1. Acesse a barra lateral do Gemini Web e clique em "Spark".
2. Clique na aba "Apps Conectados".
3. Desça a barra de rolagem e clique no botão "Adicionar app personalizado".
4. Cole o link do MCP (`{{URL_MCP}}`) no espaço "Adicione um link de app personalizado".
5. Clique no botão "Avançar".
6. Desça a barra de rolagem da nova tela e marque a caixa de seleção que tem a mensagem "Entendo e aceito os riscos de segurança e privacidade ao conectar este app personalizado".
7. Clique no botão "Conectar" e aguarde a próxima tela.
8. Aparecerá uma tela chamada "Salvar app personalizado". Você pode editar o nome do app.
9. Depois de conferir se está tudo certo e a tool estar listada, clique no botão "Conectar".

> Você saberá que está tudo certo se o MCP aparecer como um novo app em "Apps personalizados para o Spark".

## Como instalar no Claude Web

1. Na barra lateral do Claude Web, clique em "Personalizar".
2. Escolha a aba "Conectores".
3. Clique no botão "Adicionar" e escolha a opção "Adicionar conector personalizado".
4. Dê um nome para o conector.
5. Cole o link do MCP (`{{URL_MCP}}`) no espaço abaixo do nome que escolheu na etapa 4.
6. Clique no botão "Adicionar".
7. Clique no botão "Vincular".
8. Clique no botão "Requer aprovação" e mude para "Sempre permitir".

## Como instalar no ChatGPT

1. Na barra lateral, clique em "Plugins".
2. Clique no botão "+", que fica do lado de "Pesquisar plugins".
3. Na tela "Novo plugin", dê um nome no espaço "Nome".
4. Em "Conexão", cole o link do MCP (`{{URL_MCP}}`) e deixe a opção "URL do Servidor" habilitada.
5. Em "Autenticação", escolha a opção "Sem autenticação" (esta skill não gera MCP com OAuth).
6. Clique na caixa de seleção "Entendi e quero continuar".
7. Clique no botão "Criar".
8. Na nova tela, clique no botão "Conectar".
