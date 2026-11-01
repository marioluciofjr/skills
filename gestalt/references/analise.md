# Modo Análise

Use este arquivo para avaliar uma peça pronta: imagem, código, slide ou animação.

## Procedimento

1. Identifique o material recebido: código, arquivo vetorial, imagem ou vídeo.
2. Avalie G01 a G09 na ordem de `principios.md`.
3. Para motion, compare o movimento com `coreografia.md`.
4. Meça o que o material permite medir.
5. Registre cada problema no relatório abaixo.

## Como medir

| Material | Espaçamento e contraste | Linha obrigatória no relatório |
|----------|-------------------------|--------------------------------|
| Código ou vetor | Valores exatos do arquivo; rode `scripts/escala.py` e `scripts/contraste.py` | Nenhuma |
| Imagem (PNG, JPG) | Estimativa visual | `Medidas estimadas a partir de imagem` |
| Vídeo | Estimativa por quadros | `Medidas estimadas a partir de imagem` |

## Relatório

Use exatamente este formato, sem emojis:

```markdown
## Auditoria design-pro
Entregável: <tipo>
Perfil: <motion | slides | web | design-system>
Superfície: <Chat | Cowork | Claude Code>
Auditor: <nome do agente ou "autoauditoria">

| ID | Lei ou princípio | Etapa | Severidade | Local | Evidência | Correção |
|----|------------------|-------|-----------|-------|-----------|----------|

Passadas executadas: Perceber
RESULTADO: APROVADO
```

Preencha a coluna Etapa com "Perceber". Todos os princípios pertencem a essa etapa.

## Severidade

| Severidade | Critério |
|-----------|----------|
| Alta | Viola um critério WCAG 2.2 AA, ou impede a pessoa de entender ou concluir a tarefa |
| Média | Reduz a eficácia sem impedir o uso |
| Baixa | Refinamento |

A última linha tem um destes dois formatos:

- `RESULTADO: APROVADO`, só com zero itens de severidade Alta.
- `RESULTADO: REPROVADO (n altas)`, em que `n` é o número de itens de severidade Alta.

Uma medida estimada a partir de imagem não sustenta sozinha um item de severidade Alta. Marque o item como Média e peça o código ou o arquivo vetorial.
