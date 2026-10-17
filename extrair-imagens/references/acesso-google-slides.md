# Acesso ao Google Slides

Como chegar ao `.pptx` de uma apresentação do Google Slides com o mínimo de passos e sem expor o arquivo sem necessidade.

## O endpoint de exportação

Todo link de apresentação tem o mesmo formato: `https://docs.google.com/presentation/d/<ID>/...`. Basta trocar tudo o que vem depois do ID por `/export/pptx`:

- Link recebido: `https://docs.google.com/presentation/d/<ID>/edit?slide=id.abc#slide=id.abc`
- Endpoint de exportação: `https://docs.google.com/presentation/d/<ID>/export/pptx`

O subcomando `link` do script faz essa troca; o subcomando `slides` troca, baixa e extrai de uma vez.

| Via | Limite de tamanho | Precisa de login |
|---|---|---|
| Endpoint `/export/pptx` | Nenhum na prática (testado com 18 MB) | Não, se o link estiver liberado |
| Exportação pela API do Google Drive (conectores) | 10 MB por arquivo | Usa a conta conectada |

Apresentações com imagens passam de 10 MB com facilidade. Por isso a skill não usa a exportação de conectores.

## Triagem do ambiente

O subcomando `triagem` pede só os primeiros bytes da exportação e lê a resposta:

| O que aconteceu | Categoria | `link_liberado` |
|---|---|---|
| Chegou o início de um `.pptx` | `consegue_endpoint` | `true` |
| O próprio Google recusou (HTTP 401 ou 403, ou devolveu a página de login) | `consegue_endpoint` | `false` |
| Sem resposta do Google: sem internet, domínio bloqueado, proxy ou firewall do ambiente | `nao_consegue_endpoint` | `null` |

Como o script sabe que a recusa veio do Google: os servidores do Google se identificam no cabeçalho `Server` (por exemplo, `ESF`). Um erro HTTP sem essa assinatura veio de um intermediário do ambiente e conta como `nao_consegue_endpoint`. Assim, um bloqueio da sandbox nunca é confundido com link restrito.

Ambientes que não executam código entram direto em `nao_consegue_endpoint`, sem rodar a triagem.

Exemplos observados em testes reais de outubro de 2026 (podem mudar com o tempo; a triagem decide em cada execução):

- `consegue_endpoint`: Claude Code, Antigravity e Cue.
- `nao_consegue_endpoint`: Gemini, Claude Chat e Claude Cowork.

## Categoria consegue pelo endpoint

- Link liberado: rodar `slides` e entregar, sem perguntas.
- Link restrito no Claude Code (ou em outro agente que controle o navegador logado na conta dona do arquivo): o agente faz o ciclo completo, com o "sim" explícito da pessoa: libera, baixa, extrai, volta para "Restrito" e confirma com a triagem. É a rota prioritária, porque é a única em que a pessoa não precisa mexer no compartilhamento.
- Link restrito nos demais ambientes: pedir a liberação do link ou o `.pptx`, e lembrar a pessoa de voltar para "Restrito" ao final.

### Liberar o link

Passos para a pessoa, ou para o agente no Claude Code:

- Abra a apresentação e clique em **Compartilhar**.
- Em **Acesso geral**, troque "Restrito" por **Qualquer pessoa com o link**.
- Confirme que o papel ao lado é **Leitor**.
- Clique em **Concluído**.

Depois, rode a triagem de novo. Com `link_liberado: true`, rode `slides`.

### Voltar para "Restrito"

Se o link foi liberado só para a tarefa, volte logo após o download, mesmo que a extração falhe. No Claude Code, o próprio agente faz; nos demais ambientes, oriente a pessoa:

- Abra a apresentação e clique em **Compartilhar**.
- Em **Acesso geral**, troque "Qualquer pessoa com o link" por **Restrito**.
- Clique em **Concluído**.

Confirme com a triagem: o resultado precisa ser `link_liberado: false`.

### Atalho com navegador logado

Se o agente controla um navegador logado numa conta com permissão no arquivo, ele pode abrir o endpoint `/export/pptx` no navegador, sem liberar o link, e rodar `extrair` no arquivo baixado.

## Categoria não consegue pelo endpoint

Pedir o `.pptx` na conversa, na mesma hora, e seguir com `extrair --zip`. Não tentar conectores nem outras vias de download.

## Atalho .gslides

O arquivo `.gslides` que aparece no Google Drive para computador é um atalho em JSON, com campos como `doc_id`, `resource_id` (`presentation:<ID>`) e `url`. Os subcomandos `triagem`, `slides` e `link` leem esse JSON sem executar nada e usam o ID encontrado.

## Segurança do download

O script só segue redirecionamentos para `docs.google.com` e servidores `*.googleusercontent.com`, que entregam a exportação. Um redirecionamento para a tela de login conta como link restrito. Qualquer outro destino interrompe o download. O conteúdo baixado só é aceito se começar com a assinatura de um pacote `.zip`, o que barra páginas de login ou de erro.
