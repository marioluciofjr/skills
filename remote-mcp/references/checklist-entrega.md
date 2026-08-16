# Checklist de entrega

Confira cada item antes de declarar o projeto pronto (etapa 6 do pipeline).

## Estrutura do projeto

- [ ] Pasta do projeto com o nome combinado na ficha de aprovação.
- [ ] `server.py` na raiz, com uma variável de nível de módulo chamada `app` (aplicação ASGI).
- [ ] `requirements.txt` com `fastmcp`, `starlette`, `uvicorn` e, se a fonte de dados exigir, `httpx` — todos com teto de versão maior.
- [ ] `LICENSE` (MIT, salvo se a pessoa usuária pedir outra).
- [ ] `.gitignore` cobrindo `__pycache__/`, `*.pyc`, `.venv/`, `venv/`.
- [ ] `README.md` completo (ver seção própria abaixo).

## `server.py`

- [ ] `from fastmcp import FastMCP` — nunca `from mcp.server.fastmcp import FastMCP`.
- [ ] Cada tool com `name` e `annotations` (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`) no decorator `@mcp.tool(...)`.
- [ ] Cada tool com docstring explicando o que faz, os parâmetros e o formato do retorno.
- [ ] Nome de cada tool em `snake_case`, prefixado com o tema (ex.: `tema_listar_algo`), para evitar colisão com outros MCPs no mesmo cliente.
- [ ] `app = mcp.http_app(path="/mcp", stateless_http=True, middleware=[...CORS com expose_headers=["mcp-session-id"]...])`.
- [ ] Bloco `if __name__ == "__main__":` com `uvicorn.run(app, ...)`, para rodar localmente.
- [ ] Se alguma tool faz scraping ou chama API externa: tratamento de erro (timeout, HTTP de erro) sem deixar a exceção subir crua, e um plano de degradação segura se o formato do dado de origem mudar.
- [ ] Nenhuma chave de API, token ou senha escrita diretamente no código — sempre via variável de ambiente (`os.environ.get(...)`).
- [ ] `python -m py_compile server.py` roda sem erro.

## Checklist mínimo de qualidade de tool (se a skill `mcp-builder` não estiver disponível)

- [ ] O nome da tool descreve exatamente o que ela faz, sem ambiguidade.
- [ ] A tool devolve texto ou dado estruturado consistente — não alterna formato de chamada para chamada.
- [ ] Mensagens de erro explicam o que aconteceu e, se possível, o que fazer a seguir (nunca só "erro").
- [ ] Se a tool tiver um parâmetro opcional, o comportamento sem esse parâmetro está documentado na docstring.

## `README.md`

- [ ] Segue a estrutura de `assets/readme-template.md`.
- [ ] Inclui `assets/passo-a-passo-clientes.md` sem reescrever (Gemini Spark, Claude Web, ChatGPT), só trocando a URL do MCP.
- [ ] Campos de contato preenchidos com o que a pessoa usuária informou, ou marcados como `[a preencher]` — nunca um contato de terceiros.
- [ ] Nenhuma chave de API nem segredo aparece no README, nem mesmo como exemplo — apenas a instrução de configurar como variável de ambiente na Vercel.

## Git e GitHub

- [ ] Confirmação explícita da pessoa usuária antes de rodar `git init`, `git commit` ou `gh repo create` — nome do repositório e visibilidade (público/privado) combinados.
- [ ] Repositório criado com `gh repo create` e o commit inicial enviado com `git push`.
- [ ] A pessoa usuária foi avisada de que falta conectar o repositório a um novo projeto na Vercel para publicar o MCP de verdade, e de que precisa substituir o placeholder de URL no README depois do deploy.
