# Renderização e controle de qualidade

## Sumário
1. Por que relógio virtual
2. Fluxo de renderização
3. Parâmetros do vídeo
4. Checklist de QA
5. Problemas conhecidos e soluções

## 1. Por que relógio virtual

Gravar a tela em tempo real perde quadros quando o navegador engasga, e capturar com `seek` na linha do
tempo pula os callbacks (echo trail, partículas, digitação). O `browser_session.py` substitui
`performance.now`, `Date.now` e `requestAnimationFrame` antes de qualquer script; o tempo só anda quando
o renderizador manda. Cada quadro cai no instante exato e todos os efeitos rodam como no navegador.

## 2. Fluxo de renderização

1. `prepare_deps.py <projeto> --dir <deps>` — GSAP e fontes locais (o render serve os dois por rota,
   então funciona mesmo sem acesso a CDN e Google Fonts).
2. `build_motion.py <projeto> --out motion.html`.
3. `preview_frames.py motion.html --times ... --deps <deps>` — revisar a grade.
4. `render_mp4.py motion.html --out motion.mp4 --deps <deps>` — em segundo plano; acompanhe o log.
5. `contact_sheet.py --video motion.mp4 --times ... --out check.png` — conferir o arquivo final.

O renderizador valida se a fonte display carregou e avisa se não; um MP4 com fonte de fallback não deve
ser entregue.

## 3. Parâmetros do vídeo

- 30 fps (padrão). Use 60 fps só se a pessoa pedir e houver tempo (dobra o render).
- H.264, `yuv420p`, `+faststart`, CRF 16 (alta qualidade, ~9 MB para 30 s em 1080p). CRF 20 reduz
  para ~5 MB com perda pouco visível.
- Sem trilha de áudio. Se a pessoa quiser trilha, entregue o MP4 mudo e indique que a trilha pode ser
  adicionada num editor; não baixe músicas.
- A duração é uma volta da linha do tempo; o fade final do loop entra no vídeo. Para peça única que
  termina no logo, gere com `fade: false` no `outro`.

## 4. Checklist de QA

Revise a grade de preview e responda “sim” a todos:

- Fontes corretas (display condensada, mono nos rótulos), sem fallback.
- Nenhum texto cortado, sobreposto ou fora da área segura; headline em no máximo duas linhas.
- Cada cena: headline legível, UI coerente com a frase, números exatos da fonte e já parados.
- Transições: duas cenas convivendo só durante a troca; nenhum resto de cena anterior depois dela.
- Nenhuma cópia de echo presa na tela.
- Cursor só aparece quando interage e sai do quadro depois.
- Encerramento: partículas nascem dos elementos da última cena, formam o símbolo alinhado com o logo
  sólido, logo completo + tagline legíveis.
- Loop: o primeiro quadro após o fim é igual ao início (sem elementos herdados).

Momentos para capturar: meio de cada cena, meio de cada transição (+0,2 s da saída), início das
partículas (+0,8 s), símbolo formado (+2,1 s), logo final (+4,6 s).

## 5. Problemas conhecidos e soluções

| Sintoma | Causa | Solução |
|---|---|---|
| Página não inicia no preview/render | GSAP não carregou (CDN bloqueada) | rodar `prepare_deps.py` e passar `--deps` |
| Texto em fonte genérica | Google Fonts bloqueado | `--deps` com fonts.css; para HTML offline, `--inline-fonts` |
| Cópias de cena/logo presas na tela | elemento estilizado por id | mover o estilo para classe |
| Rótulo some depois de animar | transform no CSS somado ao GSAP | remover o transform do CSS; usar `T.set` |
| Partículas formam o símbolo deslocado | `mark_end` errado no logo.json | corrigir `mark_end`/`word_start` |
| Script de captura trava | `page.evaluate` devolvendo objeto do GSAP | terminar a expressão com `; 0` |
| Download de logo/CDN negado no shell | política de rede do ambiente | usar npm, o PDF ou pedir o arquivo |
| Comando `pkill -f` encerra o próprio shell | padrão casa com a linha de comando atual | matar pelo PID ou por padrão mais específico |
