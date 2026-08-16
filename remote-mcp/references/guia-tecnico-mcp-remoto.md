# Guia técnico do MCP remoto

Este guia define a arquitetura obrigatória de todo MCP remoto gerado por esta skill. Cada escolha aqui resolve um problema real, documentado abaixo — não são preferências de estilo.

## 1. Biblioteca do servidor: `fastmcp` (standalone), nunca `mcp.server.fastmcp`

```python
from fastmcp import FastMCP          # correto
from mcp.server.fastmcp import FastMCP   # NUNCA — ver o motivo abaixo
```

A SDK oficial do MCP (pacote `mcp`) lançou a versão 2.0.0 em julho de 2026 e removeu por completo o módulo `mcp.server.fastmcp`. A classe `FastMCP` foi renomeada para `MCPServer`, num módulo diferente (`mcp.server.mcpserver`). Grande parte dos tutoriais e exemplos ainda ensina o caminho antigo — se o `requirements.txt` não travar a versão do pacote `mcp`, um `pip install` puxa a 2.0.0 e o `import` quebra.

O pacote **standalone** `fastmcp` (PyPI: `fastmcp`, mantido em [gofastmcp.com](https://gofastmcp.com)) evita esse problema porque não expõe esse caminho de import — é um projeto independente, mais maduro, com versionamento próprio (não segue a versão do pacote `mcp`). Ele já entrega de fábrica o que um MCP remoto precisa: `http_app()` com caminho customizável e modo stateless.

No `requirements.txt`, sempre trave o teto de versão maior, porque uma major nova pode repetir o mesmo problema:

```
fastmcp>=3.4.0,<4.0.0
```

## 2. Transporte: Streamable HTTP, nunca SSE

```python
app = mcp.http_app(path="/mcp", stateless_http=True, middleware=[...])
```

O transporte SSE (Server-Sent Events) é o mais antigo dos dois transportes remotos do protocolo MCP, e a documentação oficial do MCP já o lista como "deprecated" (obsoleto), em favor do Streamable HTTP. Em hospedagem serverless (como a Vercel), o problema é mais grave que uma preferência de padrão: um servidor SSE mantém uma conexão HTTP aberta (`GET`) e espera receber, depois, chamadas `POST` separadas para cada ferramenta — mas nada garante que esse `POST` chegue à mesma instância de servidor que abriu a conexão `GET`. Em serverless, cada requisição pode subir uma instância nova, sem memória compartilhada com a anterior. O resultado é uma chamada de ferramenta que trava ou nunca recebe resposta.

O Streamable HTTP, com `stateless_http=True`, resolve isso: cada requisição cria um contexto de transporte novo, sem depender de nenhuma instância anterior.

O caminho `/mcp` já é o padrão de fábrica do FastMCP para Streamable HTTP — não é preciso nenhuma configuração extra para obter uma URL final terminando em `/mcp`.

## 3. CORS com o cabeçalho de sessão exposto

```python
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

app = mcp.http_app(
    path="/mcp",
    stateless_http=True,
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
            allow_headers=["*"],
            expose_headers=["mcp-session-id"],
        )
    ],
)
```

Sem `expose_headers=["mcp-session-id"]`, um cliente MCP baseado em navegador recebe o cabeçalho de sessão na resposta HTTP, mas o JavaScript do navegador não consegue lê-lo — porque, por padrão, o CORS só expõe um conjunto pequeno de cabeçalhos "seguros" ao código do lado do cliente. Isso quebra a gestão de sessão desses clientes.

## 4. `httpx` para dado ao vivo (quando a fonte de dados exigir)

Se a fonte de dados definida na etapa 2 do pipeline for um site (scraping) ou uma API externa, use `httpx` de forma assíncrona:

```python
import httpx

async with httpx.AsyncClient(timeout=10.0) as client:
    resposta = await client.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    resposta.raise_for_status()
```

Se a fonte de dados for estática (fornecida pela própria pessoa usuária, sem depender de terceiro em tempo real), a tool não precisa de nenhuma chamada de rede — e `httpx` nem entra no `requirements.txt`.

### Scraping resiliente

Quando a tool depende da estrutura de HTML de um terceiro, essa estrutura pode mudar sem aviso. Nunca deixe a tool arriscar um dado errado silenciosamente:

- Confira, antes de usar o resultado, se a quantidade de itens encontrados bate com o esperado.
- Se não bater, devolva um resumo ou uma mensagem de indisponibilidade — nunca uma divisão ou atribuição arriscada.
- Use um cache em memória com TTL curto (5 a 15 minutos) para não sobrecarregar o site de terceiro a cada chamada.

## 5. Hospedagem na Vercel: sem `vercel.json`

A Vercel detecta automaticamente um entrypoint Python em `server.py` (ou `app.py`, `index.py`, `main.py`) na raiz do repositório, desde que o arquivo exponha uma variável de nível de módulo chamada `app` (uma aplicação ASGI ou WSGI). Não é preciso `vercel.json` nem pasta `api/` para esse caso — a Vercel roteia toda requisição para essa aplicação.

Para rodar o projeto localmente (fora da Vercel), mantenha um bloco `if __name__ == "__main__":` com `uvicorn.run(app, ...)`. A Vercel nunca executa esse bloco — ela importa `app` direto do módulo.

```python
if __name__ == "__main__":
    import os
    import uvicorn

    porta = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=porta)
```

## 6. Anotações de tool

Toda tool exposta pelo MCP deve declarar `name` e `annotations` no decorator `@mcp.tool(...)`, usando `mcp.types.ToolAnnotations`:

```python
from mcp.types import ToolAnnotations

@mcp.tool(
    name="tema_nome_da_acao",
    annotations=ToolAnnotations(
        title="Título legível da tool",
        readOnlyHint=True,       # False se a tool escreve/altera algo externo
        destructiveHint=False,   # True se a tool pode apagar ou sobrescrever dado
        idempotentHint=True,     # True se chamar de novo com os mesmos argumentos não muda o resultado
        openWorldHint=True,      # True se a tool chama algo fora do controle do servidor (site, API externa)
    ),
)
```

Este checklist de tool é coberto em mais detalhe pela skill `mcp-builder`, se estiver disponível no ambiente.
