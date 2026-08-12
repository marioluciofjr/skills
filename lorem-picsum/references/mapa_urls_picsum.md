# Mapa de URLs do Lorem Picsum

Referência técnica das regras de montagem de URL do serviço [picsum.photos](https://picsum.photos), usada pelo script `scripts/lorempicsum_helper.py`. Fonte oficial: `refs/tutorial-lorem-picsum.md`.

## 1. Padrões de path (imagem)

| Modo | Padrão | Exemplo |
|---|---|---|
| Aleatória | `/{largura}/{altura}` | `https://picsum.photos/1024/1024` |
| Por ID específico | `/id/{id}/{largura}/{altura}` | `https://picsum.photos/id/237/1024/1024` |
| Por seed (fixa) | `/seed/{seed}/{largura}/{altura}` | `https://picsum.photos/seed/gatinho/1024/1024` |

> A skill sempre usa a forma explícita `/{largura}/{altura}` (mesmo para imagens quadradas), nunca a forma abreviada `/{size}` do tutorial oficial — o resultado visual é idêntico, mas simplifica a lógica do script para um único caminho de código.

## 2. Query params (combináveis entre si)

| Param | Sintaxe | Efeito |
|---|---|---|
| `grayscale` | `?grayscale` (sem valor) | Imagem em escala de cinza |
| `blur` | `?blur` ou `?blur={1-10}` | Desfoque; sem número usa o padrão do serviço, com número define o nível (oficial: 1 a 10) |
| `random` | `?random={n}` | Evita cache do navegador; só usado pela skill quando `quantidade > 1` **e** nem `id` nem `seed` foram informados (id/seed já são determinísticos) |

Ordem fixa de concatenação usada pelo script: `grayscale`, `blur[=n]`, `random=n`.

## 3. Extensão de arquivo (opcional)

Adicionada antes da query string: `.jpg` ou `.webp`. Exemplo: `https://picsum.photos/1024/1024.webp?grayscale`.

## 4. Limites aplicados pela skill

| Regra | Valor | Origem |
|---|---|---|
| Quantidade de imagens por pedido | padrão 3, máx. 30 | Validado com o Mário |
| Tamanho padrão (quando não informado) | 1024×1024 | Validado com o Mário |
| Largura/altura permitidas | 1 a 4000 px | Regra própria da skill (bom-senso) — **não** é limite documentado pelo Picsum |
| Nível de blur | 1 a 10 | Oficial do Picsum |
| Extensão | `jpg` ou `webp` | Oficial do Picsum |
| Limite de itens em `lista` | padrão 30, máx. 100 | Padrão oficial (30) + teto próprio da skill (100) |

## 5. Endpoint de listagem (`/v2/list`)

```
https://picsum.photos/v2/list?page={pagina}&limit={limite}
```

Retorna um array JSON, um item por imagem do acervo:

```json
{
  "id": "0",
  "author": "Alejandro Escamilla",
  "width": 5616,
  "height": 3744,
  "url": "https://unsplash.com/...",
  "download_url": "https://picsum.photos/id/0/5616/3744"
}
```

O header `Link` da resposta HTTP indica se há próxima página (`rel="next"`).

## 6. Endpoint de detalhes (`/info`)

```
https://picsum.photos/id/{id}/info
https://picsum.photos/seed/{seed}/info
```

Retorna o mesmo schema de objeto do item de `/v2/list` (id, author, width, height, url, download_url).

## 7. Headers relevantes

| Header | Onde aparece | Uso |
|---|---|---|
| `Picsum-ID` | Resposta de qualquer imagem | Identifica o ID da imagem servida (útil no modo aleatório, onde o ID não é escolhido previamente) |
| `Link` | Resposta de `/v2/list` | Paginação (indica se existe próxima página) |

## 8. Fora do escopo desta skill

A listagem HTML voltada para humanos em `https://picsum.photos/images` **não** é usada pela skill — para listar imagens de forma programática, use sempre o subcomando `lista` (`/v2/list`), nunca faça scraping dessa página.
