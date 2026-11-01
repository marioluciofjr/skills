# Coreografia de motion (G06 e G07)

Coreografia é a ordem e o ritmo em que os elementos se movem. Use estas regras para que a pessoa perceba grupos também no movimento.

## Defasagem

| Situação | Valor |
|----------|-------|
| Dentro de um grupo | 20 a 80 ms entre os elementos |
| Entre grupos | 120 a 300 ms entre o fim de um grupo e o início do próximo |

O intervalo entre grupos precisa ser maior que a defasagem dentro dos grupos. Sem essa diferença, a pessoa percebe um único bloco.

Um valor único serve para o grupo inteiro. Use o mesmo valor de defasagem em todos os elementos do grupo.

## Easing

| Movimento | Curva | Motivo |
|-----------|-------|--------|
| Entrada | `cubic-bezier(0.16, 1, 0.3, 1)` | Rápida no início e suave no fim |
| Saída | `cubic-bezier(0.7, 0, 0.84, 0)` | Lenta no início e rápida no fim |
| Mudança dentro da tela | `cubic-bezier(0.65, 0, 0.35, 1)` | Suave no início e no fim |

Todos os itens de um grupo usam a mesma curva e a mesma direção (G06).

## Duração

| Elemento | Duração |
|----------|---------|
| Microinteração de interface | 150 a 300 ms |
| Transição de tela | 300 a 500 ms |
| Saída | Mais curta que a entrada correspondente |

Os limites de interface não valem para cenas de filme. A duração de uma cena segue o roteiro. Mantenha cada tela com texto legível por pelo menos 0,8 s.

## Trajetória (G07)

- Use curvas contínuas.
- Evite mudança brusca de direção sem motivo narrativo.
- Mantenha a direção de saída de uma cena coerente com a entrada da cena seguinte.

## Tabela de timing

Declare os grupos nesta tabela antes de animar. A verificação de G06 usa esta tabela.

| Grupo | Elementos | Início | Duração | Easing | Direção | Defasagem interna |
|-------|-----------|--------|---------|--------|---------|-------------------|
| Título | Palavras do título | 0 ms | 500 ms | Entrada | Subida | 40 ms |
| Apoio | 3 cartões | 700 ms | 400 ms | Entrada | Subida | 60 ms |

## Acessibilidade

- Toda animação não essencial respeita `prefers-reduced-motion`.
- Animação automática com mais de 5 s precisa de controle para pausar.
- Use no máximo 3 flashes por segundo.
