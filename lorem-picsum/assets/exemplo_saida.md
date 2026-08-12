# Exemplos de saída — skill lorem-picsum

## Subcomando `imagem`

### Uma única imagem, tamanho padrão (1024x1024)

Comando: `python scripts/lorempicsum_helper.py imagem --quantidade 1`

Resposta ao usuário:

![Imagem aleatória 1024x1024](https://picsum.photos/1024/1024)
`https://picsum.photos/1024/1024`

### Múltiplas imagens (padrão: 3)

![Imagem aleatória 1](https://picsum.photos/400/300?random=1)
`https://picsum.photos/400/300?random=1`

![Imagem aleatória 2](https://picsum.photos/400/300?random=2)
`https://picsum.photos/400/300?random=2`

![Imagem aleatória 3](https://picsum.photos/400/300?random=3)
`https://picsum.photos/400/300?random=3`

### Grayscale + blur combinados

![Imagem em preto e branco com blur nível 2](https://picsum.photos/536/354?grayscale&blur=2)
`https://picsum.photos/536/354?grayscale&blur=2`

### Imagem específica por ID

![Imagem específica (ID 237)](https://picsum.photos/id/237/536/354)
`https://picsum.photos/id/237/536/354`

### Imagem fixa por seed

![Imagem fixa (seed "picsum")](https://picsum.photos/seed/picsum/536/354)
`https://picsum.photos/seed/picsum/536/354`

## Subcomando `lista`

Passo 1 — comando: `python scripts/lorempicsum_helper.py lista --pagina 1 --limite 5`

```json
{
  "url_a_buscar": "https://picsum.photos/v2/list?page=1&limit=5",
  "pagina": 1,
  "limite": 5,
  "instrucao": "Busque esta URL com sua ferramenta de fetch nativa (ex: WebFetch) — este script nunca acessa a rede, só monta a URL."
}
```

Passo 2 — busque `url_a_buscar` com sua ferramenta de fetch nativa e formate o array de itens retornado:

| ID | Autor | Dimensões | Link |
|---|---|---|---|
| 0 | Alejandro Escamilla | 5616x3744 | https://picsum.photos/id/0/5616/3744 |
| 1 | Alejandro Escamilla | 2500x1667 | https://picsum.photos/id/1/2500/1667 |
| 10 | Paul Jarvis | 2500x1667 | https://picsum.photos/id/10/2500/1667 |

Como vieram 5 itens (igual ao `limite` pedido), há provavelmente mais páginas — peça a próxima com `--pagina 2`.

## Subcomando `info`

Passo 1 — comando: `python scripts/lorempicsum_helper.py info --id 0`

```json
{
  "url_a_buscar": "https://picsum.photos/id/0/info",
  "instrucao": "Busque esta URL com sua ferramenta de fetch nativa (ex: WebFetch) — este script nunca acessa a rede, só monta a URL."
}
```

Passo 2 — busque `url_a_buscar` com sua ferramenta de fetch nativa e formate o JSON retornado:

- **ID**: 0
- **Autor**: Alejandro Escamilla
- **Dimensões originais**: 5616x3744
- **Link da imagem**: https://picsum.photos/id/0/5616/3744

## Casos de erro

### ID inexistente (`info`)

O script sempre monta a URL normalmente (não sabe se o id existe); o erro só aparece quando você busca `url_a_buscar` e a ferramenta de fetch retorna 404.

Mensagem à pessoa usuária: "Não encontrei nenhuma imagem com o ID 999999999 no acervo do Picsum. Você pode conferir IDs válidos com o subcomando de lista."

### Combinação de parâmetros inválida (id + seed)

```json
{"erro": "Os parâmetros 'id' e 'seed' são mutuamente exclusivos — use apenas um deles."}
```

### Falha de rede (só ao buscar `url_a_buscar` de `lista`/`info` — `imagem` nunca depende de rede)

Se a sua ferramenta de fetch não conseguir buscar a URL (timeout, instabilidade do serviço, restrição de rede do ambiente), mensagem à pessoa usuária: "Não consegui consultar o acervo do Picsum agora — pode ser uma instabilidade momentânea do serviço ou uma restrição de rede deste ambiente. Pode tentar novamente em instantes?"
