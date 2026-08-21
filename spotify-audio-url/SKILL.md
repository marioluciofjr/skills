---
name: spotify-audio-url
description: "Recebe um link de episódio do Spotify e devolve APENAS a URL direta do arquivo de áudio (MP3/M4A) publicada no feed RSS aberto do podcast, ou a mensagem de recusa quando o conteúdo não tem RSS aberto. Use SEMPRE que o usuário colar um link open.spotify.com ou spotify.link e pedir para baixar, salvar, extrair, converter, 'pegar o mp3', 'pegar o áudio', 'transcrever esse episódio' ou 'me manda o arquivo desse podcast' — mesmo que não use a palavra 'skill', 'RSS' ou 'download'. Ative também quando a pessoa perguntar 'dá pra baixar esse?', 'esse aqui é público?' ou mandar vários links do Spotify de uma vez."
license: CC-BY-4.0
compatibility: "Requer as ferramentas web_fetch e web_search"
metadata:
  author: "Mário"
  tags:
    - podcast
    - rss
    - spotify
    - audio
  domain: media
  network-scope: "open.spotify.com, feeds RSS públicos de podcast e CDNs de áudio"
  writes-files: false
---

# Spotify Audio URL

Resolve um link de episódio do Spotify para a URL direta do arquivo de áudio, quando ela existe publicamente.

## Princípio que sustenta a skill

O Spotify não hospeda a maior parte dos podcasts: ele lê feeds RSS públicos, os mesmos que abastecem Apple Podcasts, Deezer e Pocket Casts. Nesses feeds, cada episódio traz a tag `<enclosure url="...">` com o endereço do arquivo. O arquivo está no CDN do host (Acast, Omny, Megaphone e outros), não dentro do Spotify.

A decisão desta skill é, portanto, sobre origem do áudio, não sobre popularidade nem sobre o episódio estar visível na plataforma. Conteúdo Original ou Exclusive do Spotify, episódios pagos e música existem apenas nos servidores da plataforma, protegidos por DRM. Para esses não há caminho legítimo, e a skill recusa em vez de improvisar.

## Formato de saída

Esta é a parte mais importante da skill e a que mais tende a ser violada por hábito. A resposta é minimalista.

**Sucesso** — responda com a URL e nada mais. Sem tabela, sem título, sem `curl`, sem `wget`, sem o endereço do feed, sem nome do episódio, sem duração, sem frase de introdução, sem oferta de ajuda no final:

```
https://sphinx.acast.com/p/open/s/639392cb.../e/6a725b1a.../media.mp3
```

**Recusa** — responda exatamente esta frase, sozinha, sem explicar o motivo e sem sugerir alternativas:

```
Este não consigo, pois não está público.
```

Se o usuário mandar vários links, devolva uma linha por link, na ordem recebida, cada linha sendo uma URL ou a frase de recusa. Nada além disso.

## Fluxo

### 1. Ler a página do episódio

Faça `web_fetch` na URL do Spotify. Parâmetros como `?si=`, `&utm_source=` e `&nd=1` podem ser descartados; o ID do episódio é o suficiente.

Colete da página: título do episódio, nome do podcast, `meta-music:duration` (segundos), `meta-music:release_date` e o texto completo de `meta-description`.

Se a URL não for de episódio (`/track/`, `/album/`, `/playlist/`, `/artist/`) ou a página não carregar, vá direto para a recusa.

### 2. Identificar o host pelo rodapé da descrição

O rodapé da descrição quase sempre entrega quem hospeda. É o sinal mais barato e mais confiável disponível:

| Rodapé encontrado | Host | Onde procurar o feed |
| --- | --- | --- |
| "Hosted on Acast" | Acast | `feeds.acast.com/public/shows/{id}` |
| "omnystudio.com/listener" | Omny | `omnycontent.com/d/playlist/.../podcast.rss` |
| "megaphone.fm/adchoices" | Megaphone | `feeds.megaphone.fm/{slug}` |
| "podcastchoices.com/adchoices" | Art19 / Wondery | feed próprio do programa |
| Nenhum, com selo Original ou Exclusive | Spotify | não existe |

A lista não é exaustiva. Libsyn, Captivate, Buzzsprout, Simplecast, Transistor, Spreaker, RedCircle, Blubrry e Podbean também publicam RSS aberto e aparecem com assinaturas próprias ou sem rodapé algum. Ausência de rodapé conhecido não prova que é exclusivo — prova apenas que o passo 3 precisa trabalhar mais.

Atenção a um caso que engana: podcasts no Anchor / Spotify for Podcasters são hospedados pelo Spotify **e ainda assim** têm RSS aberto em `anchor.fm/s/{id}/podcast/rss`. Hospedagem pelo Spotify não é sinônimo de conteúdo fechado.

### 3. Localizar o feed

Use `web_search` com o nome do podcast somado ao host suspeito, ou ao termo `RSS feed`. Agregadores como Podbean, Listen Notes, Podtail, Player.fm e Podchaser costumam expor o endereço do feed em texto na página, o que resolve a busca sem precisar de API.

Faça `web_fetch` no feed encontrado.

Quando o feed vier de um host que importou o programa de outro, o cabeçalho pode trazer uma tag como `<acast:importedFeed>` apontando para o endereço antigo. Isso é útil quando o episódio procurado é anterior à migração e não aparece no feed atual.

### 4. Casar o episódio

Percorra os `<item>` e case pelo título. Como títulos podem repetir entre temporadas ou vir com pequenas diferenças de acentuação, confirme com pelo menos um segundo sinal: `<pubDate>` batendo com a data do Spotify, ou `<itunes:duration>` batendo com `meta-music:duration`.

Divergência nos dois sinais significa episódio errado. Entregar a URL errada é pior que recusar — nesse caso, prefira a recusa.

Se o feed estiver paginado e o episódio for antigo, siga os links `atom:link rel="next"` antes de desistir.

### 5. Extrair e limpar a URL

Pegue o atributo `url` da tag `<enclosure>`. Remova a query string de rastreamento (`?utm_source=`, `&in_playlist=`, `&dest-id=`) — ela não é necessária para o download e polui a saída.

Entregue a URL limpa, sozinha.

## Quando recusar

Responda com a frase de recusa nestes casos:

- Selo Original ou Exclusive do Spotify no programa
- Episódio de assinante, pago ou com feed autenticado por token individual
- Música, faixa, álbum ou playlist
- Feed do programa não localizado após busca razoável
- Episódio ausente do feed, ou casamento ambíguo entre título, data e duração
- Página do Spotify indisponível ou episódio removido

A frase é sempre a mesma, independentemente do motivo. O usuário pediu uma decisão binária, não um diagnóstico.

## Exemplos

**Exemplo 1 — podcast com RSS aberto**

Entrada: `https://open.spotify.com/episode/3QMPXVTq6Bo31n2UVvaeYn`

Saída:
```
https://sphinx.acast.com/p/open/s/639392cb6c25ea001115e06a/e/6a725b1a919aaf5974b09521/media.mp3
```

**Exemplo 2 — conteúdo exclusivo da plataforma**

Entrada: link de um Spotify Original

Saída:
```
Este não consigo, pois não está público.
```

**Exemplo 3 — dois links de uma vez**

Saída:
```
https://traffic.omny.fm/d/clips/2f6a79aa.../audio.mp3
Este não consigo, pois não está público.
```

## Limites

A skill trabalha apenas com o que o próprio produtor publicou abertamente em RSS. Ela não contorna DRM, não usa credenciais de conta, não captura stream e não recorre a serviços de terceiros que rippam áudio do Spotify. Quando o caminho legítimo não existe, a resposta é a recusa.

O arquivo obtido pelo feed pode conter inserção dinâmica de anúncios, o que faz o tamanho variar entre downloads e diferir do que se ouve no aplicativo. Isso é comportamento normal do host, não erro de resolução.
