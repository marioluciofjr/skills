# Regras de UI, UX e CX para apps de Fire TV

Leia este arquivo antes de adaptar o `assets/index-base.html` ao app pedido. O esqueleto já implementa estas regras; ao mudar o conteúdo, mantenha-as.

## UI (interface)

- **Palco fixo e escalado.** Tudo fica num `#stage` de 1720x960 px, centralizado e escalado pela função `fitStage()`. Nunca use `vw`/`vh` para dimensionar componentes: a Fire TV expõe ao WebView uma viewport de cerca de 960x540 ou 1280x720 px CSS.
- **Área segura contra overscan.** Muitas TVs cortam as bordas. A margem padrão é 5%, ajustável no próprio app (0, 3, 5, 8 e 10%) e salva.
- **Tamanhos mínimos no palco de 1720x960:** texto corrido com 20 px ou mais, títulos com 30 px ou mais, botões com 72 px ou mais de altura, alvos de foco com 100 px ou mais em grades.
- **Contraste** de pelo menos 4.5:1. Fundo escuro por padrão (TVs ficam em ambientes escuros), a não ser que o design system diga outra coisa.
- **Foco sempre visível.** Um único elemento em foco por vez, com borda de 5 a 7 px na cor de destaque, brilho e leve escala (1.03 a 1.06). Nada depende de hover ou de toque.
- **Modais, toasts e qualquer elemento fora do `#stage`** também escalam com `transform: scale(var(--s))`; a `fitStage()` define a variável `--s`. Toasts ficam acima da barra de ajuda, nunca por cima dela.
- **Glifos Unicode que têm versão emoji** (por exemplo ♟, ☎, ☰ e ⏯) recebem logo depois o seletor de texto U+FE0E. Em JavaScript: `'☰' + '︎'`. Em HTML: `&#x2630;&#xFE0E;`. Sem ele, a TV mostra um emoji colorido no lugar do símbolo.
- **Animações curtas** (até 250 ms). O hardware da Fire TV Stick é fraco: evite sombras e blur pesados em muitos elementos e prefira atualizar o DOM a recriá-lo.

## UX (navegação pelo controle)

- **Modelo de zonas de foco** (por exemplo `main`, `menu` e `modal`), com uma função central `window.fireTvKey(action)`. As ações enviadas pelo app nativo são `UP`, `DOWN`, `LEFT`, `RIGHT`, `SELECT`, `BACK`, `MENU`, `PLAY_PAUSE`, `REWIND` e `FAST_FORWARD`.
- **As setas movem o foco de forma previsível.** Chegar à borda de uma zona leva à zona vizinha (por exemplo, a seta para a direita na última coluna abre o menu lateral).
- **Voltar desfaz o último passo:** fecha o modal, cancela a seleção, volta ao conteúdo principal. Na raiz, abre a confirmação "Sair do app?". Nunca feche o app sem confirmar.
- **Menu** (☰) abre e fecha o menu lateral. **Play/Pause** é atalho para a ação principal do contexto.
- **Toda ação inválida dá retorno imediato** com toast e som curto, nunca silêncio.
- **Ações destrutivas** (recomeçar, apagar, trocar de modo) pedem confirmação, com o foco inicial em "Cancelar".
- **Barra de ajuda contextual** com as teclas que valem na tela atual (`OK`, `↩`, `☰`, `⏯`).
- **Listener de teclado** (setas, Enter, Esc e M) para testar no navegador do computador.

## CX (experiência contínua)

- **Estado e preferências** ficam em `localStorage`, sempre dentro de try/catch. O app retoma de onde a pessoa parou e avisa "Retomado de onde você parou".
- **Processamento pesado** (IA de jogo, cálculos, filtros) vai para um Web Worker criado a partir de um Blob, que funciona em `file://`, com alternativa síncrona se o Worker falhar. Enquanto processa, mostre o estado ("Pensando...") e mantenha a navegação responsiva.
  - Monte o Worker a partir das funções puras: `new Worker(URL.createObjectURL(new Blob([src], {type:'application/javascript'})))`, em que `src` concatena o `JSON.stringify` das constantes, o `fn.toString()` das funções e um `self.onmessage`.
  - Descarte respostas antigas com um token incremental.
- **Estados vazios explicativos** ("Nenhum item ainda"), mensagens curtas em português do Brasil e sons opcionais, desligáveis no menu.
- **Item "Sair" no menu**, que salva e depois chama `window.location.href = '<slug>://sair'`. O app nativo intercepta esse endereço e fecha.
- **Tudo num único HTML autocontido** (CSS e JS inline, sem CDN), para funcionar offline. Só peça a permissão de internet (`--internet`) se o app realmente usar conteúdo on-line.
