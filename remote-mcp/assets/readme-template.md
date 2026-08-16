# Template do README final

Preencha este template na etapa 6 do pipeline. Escreva o texto livre (Introdução, Estrutura do projeto, Tecnologias) em português claro — ordem direta, uma ideia por frase, voz ativa, vocabulário comum. As três seções "Como instalar" vêm de `passo-a-passo-clientes.md`, sem reescrever.

---

```markdown
# [nome-do-projeto]

[![Made with Python](https://img.shields.io/badge/Python->=3.10-blue?logo=python&logoColor=white)](https://python.org "Ir para a página do Python")
![license - MIT](https://img.shields.io/badge/license-MIT-green)

## Índice

* [Introdução](#introdução)
* [Estrutura do projeto](#estrutura-do-projeto)
* [Tecnologias utilizadas](#tecnologias-utilizadas)
* [Requisitos](#requisitos)
* [Como instalar no Gemini Spark](#como-instalar-no-gemini-spark)
* [Como instalar no Claude Web](#como-instalar-no-claude-web)
* [Como instalar no ChatGPT](#como-instalar-no-chatgpt)
* [Links úteis](#links-úteis)
* [Contribuições](#contribuições)
* [Licença](#licença)
* [Contato](#contato)

## Introdução

[Um ou dois parágrafos: o que o MCP faz, de onde vem o dado, e que ele é remoto (Streamable HTTP, hospedado na Vercel) — quem for usar não precisa instalar nada, só apontar o cliente para a URL pública.]

> [!IMPORTANT]
> Esta URL só aceita pedidos `POST` e `DELETE`, no formato do protocolo MCP. Se você colar o link no navegador, ele faz um `GET` e aparece a mensagem "Method Not Allowed" — isso é esperado, não é um erro. É só a confirmação de que o servidor está no ar; use a URL num cliente MCP, não direto no navegador.

## Estrutura do projeto

É um MCP-Server simples que utiliza o pacote [FastMCP](https://gofastmcp.com), seguindo também as orientações do repositório oficial do [Model Context Protocol](https://github.com/modelcontextprotocol/python-sdk), da Anthropic.

Este MCP-Server tem a(s) seguinte(s) tool(s):

### `[nome_da_tool]` (Tool)
[O que ela faz, o parâmetro opcional/obrigatório, e o que acontece nos casos de borda.]

## Tecnologias utilizadas

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![FastMCP](https://img.shields.io/badge/FastMCP-servidor%20MCP-000000)
![Starlette](https://img.shields.io/badge/Starlette-ASGI-052F5F)
![Uvicorn](https://img.shields.io/badge/Uvicorn-servidor%20ASGI-2A6DB2)
![Vercel](https://img.shields.io/badge/Vercel-deploy-black?logo=vercel&logoColor=white)

* **Python** — linguagem do servidor.
* **FastMCP** — framework que implementa o protocolo MCP e expõe a tool via Streamable HTTP.
* **Starlette** — aplicação ASGI por baixo do FastMCP; aqui, adiciona o CORS liberado para clientes remotos.
* **Uvicorn** — servidor ASGI usado para rodar o projeto localmente.
[* **httpx** — busca o conteúdo da fonte de dados a cada chamada da tool. — inclua só se o projeto usar httpx.]
* **Vercel** — hospeda o servidor remoto e serve a URL pública.

## Requisitos

Para **usar** o servidor a partir de um cliente MCP (Gemini Spark, Claude Web ou ChatGPT), não é preciso instalar nada. Basta um cliente que aceite servidor MCP remoto via Streamable HTTP e a URL pública deste servidor.

Para **rodar o projeto localmente** (desenvolvimento ou testes), instale antes:
* [Python 3.10](https://www.python.org/downloads/) ou superior.
* As dependências do projeto: `pip install -r requirements.txt`.

[BLOCOS DE passo-a-passo-clientes.md AQUI, SEM REESCREVER — Gemini Spark, Claude Web, ChatGPT]

## Links úteis

* [Documentação oficial do Model Context Protocol](https://modelcontextprotocol.io/introduction) - Todos os detalhes dessa inovação da Anthropic
* [Documentação oficial do FastMCP](https://gofastmcp.com) - Framework usado para construir o servidor MCP deste projeto
* [Documentação da Vercel para Python](https://vercel.com/docs/functions/runtimes/python) - Como a Vercel roda uma aplicação Python/ASGI
[* Links específicos da fonte de dados do tema, se fizer sentido]

## Contribuições

Contribuições são bem-vindas! Se você tem ideias para melhorar este projeto, sinta-se à vontade para fazer um fork do repositório.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Contato

[nome da pessoa usuária, ou "[a preencher]"]
<div>
  [ícones/links de contato que a pessoa usuária informou na etapa 5 — LinkedIn, e-mail, site, GitHub — só os que ela quiser incluir. Nunca herde os contatos de quem criou esta skill.]
</div>
```
