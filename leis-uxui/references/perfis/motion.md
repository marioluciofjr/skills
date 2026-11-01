# Perfil: motion

Vale para vinheta, abertura, cartelas, motion de apresentação e animação de interface.

## Leis prioritárias

| ID | Lei | Limiar neste perfil |
|----|-----|---------------------|
| L01 | Proximidade | Ver G01 |
| L02 | Semelhança | Ver G02 |
| L05 | Prägnanz | Ver G05 |
| L06 | Destino comum | Ver G06 |
| L07 | Continuidade | Ver G07 |
| L08 | Efeito Von Restorff | 1 elemento em destaque por cartela |
| L12 | Carga cognitiva | 2 famílias tipográficas no filme inteiro |
| L15 | Coerência e redundância | 1 ideia por cartela; a tela não repete a narração |
| L23 | Regra do pico-fim | O roteiro declara o momento de pico e o encerramento |
| L26 | Navalha de Occam | Toda animação comunica algo; a animação sem função sai |

## Limiares transversais

| Tema | Limiar | Fonte |
|------|--------|-------|
| Contraste de texto normal | 4,5:1 | WCAG 2.2, 1.4.3 (AA) |
| Contraste de texto grande (24 px, ou 18,66 px em negrito) | 3:1 | WCAG 2.2, 1.4.3 (AA) |
| Contraste de componentes e gráficos | 3:1 | WCAG 2.2, 1.4.11 (AA) |
| Animação automática com mais de 5 s | Precisa de controle para pausar | WCAG 2.2, 2.2.2 (A) |
| Flashes | No máximo 3 por segundo | WCAG 2.2, 2.3.1 (A) |
| Redução de movimento | Toda animação não essencial respeita `prefers-reduced-motion` | Boa prática; WCAG 2.2, 2.3.3 (AAA) |
| Duração de microinteração de UI | 150 a 300 ms | Heurística |
| Duração de transição de tela | 300 a 500 ms | Heurística |

## Observações

- Um vídeo renderizado (MP4) não responde a `prefers-reduced-motion`. Confira esse limiar só em entrega HTML.
- Em um arquivo de vídeo, o controle para pausar é o do próprio player.
- Os limites de duração valem para interface. A duração de uma cena de filme segue o roteiro.
