# Perfil: design system

Vale para tokens, bibliotecas de componentes e guias de estilo.

## Leis prioritárias

| ID | Lei | Limiar neste perfil |
|----|-----|---------------------|
| L02 | Semelhança | Ver G02 |
| L04 | Região comum | Ver G04 |
| L05 | Prägnanz | Ver G05 |
| L10 | Efeito estética-usabilidade | 100% dos componentes usam tokens declarados |
| L12 | Carga cognitiva | No máximo 2 famílias tipográficas e 3 pesos por família |
| L13 | Modelo mental | Nomes de token e de componente explicados no guia |
| L18 | Lei de Fitts | Componentes interativos com no mínimo 24×24 px |
| L26 | Navalha de Occam | Sem variante de componente sem uso documentado |
| L29 | Lei de Murphy | Todo componente com dados documenta os 4 estados |
| L30 | Princípio de Pareto | Documente primeiro os componentes de maior uso |

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

- Declare os tokens de duração dentro das faixas acima.
- Confira o contraste de todo par de token de texto e token de fundo.
