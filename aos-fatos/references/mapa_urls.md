# Mapa de URLs do Aos Fatos

Fonte de verdade para montar qualquer URL de busca em `https://www.aosfatos.org/noticias/`.
Todas as URLs desta skill DEVEM começar com essa base e terminar com `&page=1` (nunca outro número de página).

## 1. Selos de veracidade (implica `formato=checagem` sempre)

| Label mostrado à pessoa | Valor canônico no parâmetro `selo` |
|---|---|
| verdadeiro | `verdadeiro` |
| falso | `falso` |
| não é bem assim | `outro` |

Padrão de URL: `?formato=checagem&selo=<valor>&page=1`

## 2. Ano

Anos válidos: **de 2021 até o ano corrente do sistema** (qualquer outro valor é inválido — reperguntar). O teto **não é um número fixo**: `scripts/aosfatos_helper.py` calcula o ano máximo em tempo real (`date.today().year`) a cada execução, então a skill aceita automaticamente o ano novo assim que o calendário virar — nunca precisa de atualização manual por causa disso. Só o piso (2021) é fixo.

Padrão de URL: `?formato=checagem&ano=<AAAA>&page=1` (o `formato` pode ser trocado por outro valor da tabela 4, se a pessoa escolher um formato diferente na sub-pergunta).

## 3. Canais temáticos

| Label mostrado à pessoa | Slug (`canal=`) |
|---|---|
| boataria política | `boataria-politica` |
| pseudociência | `pseudociencia` |
| negacionismo climático | `negacionismo-climatico` |
| inteligência artificial | `inteligencia-artificial` |
| fraudes digitais | `fraudes-digitais` |
| tecnopolítica | `tecnopolitica` |
| autoritarismo | `autoritarismo` |
| discurso de ódio | `discurso-de-odio` |
| impacto | `impacto` |
| eleições 2026 | `eleicoes-2026` |

Padrão de URL: `?canal=<slug>&page=1` (sem `formato` por padrão — só entra se a pessoa escolher um na sub-pergunta de formato).

## 4. Formatos de conteúdo (filtro independente, combinável com ano/canal)

| Valor (`formato=`) | Observação |
|---|---|
| `checagem` | **Recomendado** — é o foco principal desta skill (verificação de fatos com selo) |
| `tempo-real` | |
| `explicador` | |
| `reportagem` | |
| `radar` | |
| `hq` | |
| `analise` | |
| `nota` | |
| `institucional` | |
| *(sem filtro)* | Não inclui o parâmetro `formato` na URL — todos os tipos de conteúdo |

`formato` é um filtro que pode ser usado **sozinho** (ex: `?formato=tempo-real&page=1`) ou **combinado** com ano e/ou canal. Se um `selo` for escolhido, `formato` é sempre forçado para `checagem` (não é uma escolha independente nesse caso).

## 5. Palavra-chave livre

Padrão de URL: `?q=<palavra-chave-codificada>&page=1` (o `formato` pode ser adicionado conforme a sub-pergunta).

A palavra-chave deve ser codificada para URL (espaços e acentos tratados via `urllib.parse.quote_plus`).

## 6. Combos (múltiplos filtros na mesma busca)

O site aceita **qualquer combinação** dos filtros acima na mesma URL — eles se combinam com "E" (todos os critérios precisam bater ao mesmo tempo), não com "OU". Exemplos confirmados:

| Combinação desejada | URL resultante |
|---|---|
| Só formato | `?formato=tempo-real&page=1` |
| Formato + ano | `?formato=tempo-real&ano=2025&page=1` |
| Formato + ano + selo | `?formato=checagem&ano=2026&page=1&selo=outro` |
| Canal + ano | `?canal=eleicoes-2026&ano=2025&page=1` |

A ordem dos parâmetros na URL não importa para o site — o script `scripts/aosfatos_helper.py` sempre gera na ordem: `formato`, `selo`, `ano`, `canal`, `q`, `page=1`.

É obrigatório informar **pelo menos um** filtro (selo, formato, ano, canal ou palavra-chave) — nunca chamar `montar-url` sem nenhum deles.

## Regra fixa de paginação

`page=1` é sempre o único valor usado. Esta skill nunca navega para `page=2` ou além — se a página 1 trouxer menos de 12 resultados, a skill informa a quantidade real encontrada.

## 7. Nota sobre ferramenta de fetch e limite de passos (harness-dependente)

Em testes diretos no Claude Code (ferramenta WebFetch), tanto a página de listagem quanto artigos individuais do Aos Fatos responderam normalmente a buscas estáticas, sem qualquer bloqueio — não é necessário navegador interativo nesse harness especificamente, e abrir cada artigo individualmente não causou problema de limite ali.

Em outros harnesses, que usam um navegador remoto interativo com orçamento limitado de ações por execução (`max_steps`) para acessar sites, abrir os 12 artigos individualmente pode consumir esse orçamento inteiro e truncar a lista antes de completar os 12 itens (relatado: truncou em 7 de 12). Como não é possível garantir de antemão qual mecanismo de fetch o harness em uso vai empregar, a skill sempre prioriza a **extração em lote a partir da página de listagem** (título + URL de cada card, em uma única busca) como caminho padrão, reservando a abertura de artigos individuais para quando houver dúvida real sobre um item específico — nunca como rotina para os 12. Ver `## tarefa` → Passo Fetch no `SKILL.md`.
