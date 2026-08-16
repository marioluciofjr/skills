# Exemplo completo do pipeline

Este exemplo é fictício — usa um restaurante inventado, "Sabor Caseiro" — só para calibrar o formato de cada etapa. Não copie os nomes, adapte ao tema real.

## Etapa 1 — Tema

> "Quero um MCP remoto que consulte o cardápio do site do restaurante Sabor Caseiro."

## Etapa 2 — As 5 perguntas e as respostas

1. **Fonte de dados**: o cardápio está publicado no site `saborcaseiro.exemplo/cardapio`, sem API — precisa de scraping.
2. **Ações/tools**: só consulta. Nenhuma tool escreve ou reserva nada.
3. **Público humano final**: clientes do restaurante que querem saber o cardápio e o preço de um prato antes de ir.
4. **Autenticação**: nenhuma — o site é público.
5. **Repositório**: `mcp-sabor-caseiro`, público. Git e GitHub CLI já instalados.

## Etapa 3 — Ficha de aprovação (resumida)

**Resumo (150 palavras):** um MCP remoto que consulta o cardápio publicado no site do restaurante Sabor Caseiro. Como o site não tem API, a tool busca a página ao vivo a cada chamada, com cache curto, e extrai os pratos e preços de cada categoria do cardápio (entradas, pratos principais, sobremesas, bebidas). Não há autenticação, porque o cardápio é público. O MCP só tem tools de leitura — nenhuma reserva nem pedido. O público final são clientes do restaurante que querem consultar o cardápio antes de ir, por Gemini Spark, Claude Web ou ChatGPT. O projeto vai para um repositório público no GitHub, chamado `mcp-sabor-caseiro`, hospedado na Vercel. Se a estrutura do site mudar e a extração falhar, a tool devolve uma mensagem clara em vez de um dado incompleto ou errado.

**Nome sugerido do servidor**: `SaborCaseiro-Cardapio`

**Tools propostas**:
- `saborcaseiro_listar_cardapio` — devolve o cardápio completo, ou filtrado por categoria.
- `saborcaseiro_buscar_prato` — busca um prato específico pelo nome e devolve preço e descrição.

**Prompts propostos**: nenhum — o tema não pede um prompt reutilizável.

**Resources possíveis**: nenhum — as duas tools já cobrem o caso de uso.

## Etapa 4 — Aprovação

A pessoa usuária aprova a ficha sem ajustes.

## Etapas 5 e 6 — Entrega

- Pasta `mcp-sabor-caseiro/` criada com `server.py`, `requirements.txt` (`fastmcp`, `starlette`, `uvicorn`, `httpx`), `LICENSE`, `.gitignore`, `README.md`.
- `server.py` com as duas tools, cada uma com `annotations` (`readOnlyHint=True`, `destructiveHint=False`), scraping resiliente (cache de 10 minutos, degradação segura se a página mudar de estrutura).
- `README.md` com o passo a passo fixo de instalação no Gemini Spark, Claude Web e ChatGPT, e um placeholder de URL para a pessoa usuária substituir depois do deploy na Vercel.
- Repositório `mcp-sabor-caseiro` criado no GitHub (público, como combinado) e o commit inicial enviado.
