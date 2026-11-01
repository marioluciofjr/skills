# Checklist de auditoria

Execute as 5 passadas nesta ordem. Registre cada problema na tabela de `formato-relatorio.md`. Pule uma lei só quando a lei não se aplicar ao entregável, e declare o motivo.

Antes da primeira passada:

1. Identifique o entregável e abra o perfil dele em `perfis/`.
2. Rode `scripts/lint_design.py` se houver arquivo de código.
3. Rode `scripts/contraste.py` para cada par de cor de texto e cor de fundo.

Se a execução de código não estiver disponível, calcule ou estime os valores e declare a limitação em uma linha.

## Passada 1: Perceber

- [ ] L01 a L07: aplique os princípios G01 a G07 da skill `gestalt`.
- [ ] L08: existe no máximo 1 elemento que quebra o padrão por tela?
- [ ] L09: o conteúdo obrigatório fica fora de banners e carrosséis automáticos?
- [ ] L10: as cores, os espaçamentos e as fontes vêm de tokens?
- [ ] Contraste: o texto normal atinge 4,5:1, e o texto grande e os componentes atingem 3:1?

## Passada 2: Compreender

- [ ] L11: os blocos que a pessoa precisa reter têm de 3 a 5 itens?
- [ ] L12: há no máximo 2 famílias e 3 pesos por família?
- [ ] L13: os rótulos usam a linguagem do público?
- [ ] L14: a estrutura segue as convenções?
- [ ] L15: há uma ideia por slide ou cartela, sem repetir o texto narrado?

## Passada 3: Decidir e agir

- [ ] L16: há 1 CTA primário por seção?
- [ ] L17: as tabelas de planos têm 3 ou 4 opções e 1 recomendada?
- [ ] L18: os alvos têm pelo menos 24×24 px?
- [ ] L19: o retorno visual chega em menos de 400 ms, e há progresso acima de 1 s?
- [ ] L20: a pessoa consegue usar sem tutorial obrigatório?
- [ ] L21: os formulários usam `autocomplete` e valores padrão?

## Passada 4: Lembrar e continuar

- [ ] L22: o item mais importante fica na primeira ou na última posição?
- [ ] L23: o roteiro declara o pico e o encerramento?
- [ ] L24: os fluxos com 3 ou mais passos mostram "Passo X de Y" ou barra?
- [ ] L25: o progresso fica visível em fluxos de várias etapas?

## Passada 5: Sistema

- [ ] L26: todo elemento removível foi removido?
- [ ] L27: nenhum campo pede o que o sistema já sabe?
- [ ] L28: telefone, data e CPF aceitam entrada com e sem máscara?
- [ ] L29: os componentes com dados têm os 4 estados?
- [ ] L30: os itens mais usados aparecem primeiro?

## Depois da quinta passada

1. Classifique a severidade de cada problema.
2. Se duas leis indicarem correções opostas, aplique `conflitos.md`.
3. Preencha `formato-relatorio.md` e termine com a linha `RESULTADO:`.
