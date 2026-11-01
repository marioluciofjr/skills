# Formato do relatório de auditoria

Use exatamente este formato. Use Markdown, sem emojis. Coloque o relatório no fim da resposta, depois da entrega.

```markdown
## Auditoria design-pro
Entregável: <tipo>
Perfil: <motion | slides | web | design-system>
Superfície: <Chat | Cowork | Claude Code>
Auditor: <nome do agente ou "autoauditoria">

| ID | Lei ou princípio | Etapa | Severidade | Local | Evidência | Correção |
|----|------------------|-------|-----------|-------|-----------|----------|

Passadas executadas: Perceber, Compreender, Decidir e agir, Lembrar e continuar, Sistema
RESULTADO: APROVADO
```

## Severidade

| Severidade | Critério |
|-----------|----------|
| Alta | Viola um critério WCAG 2.2 AA, ou impede a pessoa de entender ou concluir a tarefa |
| Média | Reduz a eficácia sem impedir o uso |
| Baixa | Refinamento |

## Linha final

A última linha do relatório tem um destes dois formatos, sem texto depois:

- `RESULTADO: APROVADO`
- `RESULTADO: REPROVADO (n altas)`, em que `n` é o número de itens de severidade Alta.

Use `APROVADO` só com zero itens de severidade Alta. Itens de severidade Média e Baixa não impedem a aprovação, mas ficam na tabela.

## Casos especiais

- **Sem problemas:** deixe a tabela só com o cabeçalho.
- **Conteúdo indisponível:** escreva a linha "Conteúdo indisponível para auditoria" e termine com `RESULTADO: REPROVADO (0 altas)`.
- **Sem execução de código:** escreva a linha "Scripts não executados" e explique como obteve os valores.
