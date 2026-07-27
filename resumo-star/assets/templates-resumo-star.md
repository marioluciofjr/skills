# Templates de Saída: Skill `resumo-star`

Este documento contém o modelo único e estruturado de saída que a skill `resumo-star` deve utilizar.

---

## 1. Etapa Prévia Obrigatória: Questionário de Feedback

A IA DEVE apresentar EXATAMENTE as 3 perguntas abaixo à pessoa usuária e BLOQUEAR a geração do resumo STAR até obter as respostas:

```markdown
### Questionário de Feedback da Iteração

Para que eu possa gerar o Resumo STAR desta sessão, por favor responda às 3 perguntas abaixo:

1. De 0 a 5 qual foi o grau de satisfação com o resultado dessa tarefa?
2. Quais foram os pontos positivos desse fluxo de trabalho com a IA generativa?
3. Quais foram os pontos a melhorar?
```

---

## 2. Estrutura do Resumo STAR (Saída Final Unificada)

> **Regra Interna de Extensão (Piso Mínimo)**: 
> A IA deve garantir internamente os seguintes mínimos de palavras para cada seção do resumo (sem exibir estas contagens de palavras na saída final):
> - Situação: Mínimo de 50 palavras
> - Tarefa: Mínimo de 150 palavras
> - Ação: Mínimo de 200 palavras
> - Resultados: Mínimo de 100 palavras
> - Total do resumo: Mínimo de 500 palavras no total.

```markdown
> Disclaimer: Este resumo foi redigido em primeira pessoa pela IA generativa, descrevendo o que ela compreendeu a partir do contexto fornecido e o que realizou durante a execução da tarefa.

# Resumo STAR

---

### Situação
[Descrição em primeira pessoa do contexto, briefing, stack, dependências e cenário inicial do problema fornecido pela pessoa usuária. Cumprir o piso mínimo de 50 palavras.]

### Tarefa
[Descrição em primeira pessoa do objetivo prático, requisitos funcionais e não funcionais, restrições e expectativas de entrega. Cumprir o piso mínimo de 150 palavras.]

### Ação
[Descrição em primeira pessoa, combinando rigor técnico e clareza didática. Descrever a cadeia de raciocínio (Chain of Thought), decisões adotadas, chamadas de ferramentas/skills/MCPs, manipulação de arquivos e validações executadas. Cumprir o piso mínimo de 200 palavras.]

### Resultados
[Descrição em primeira pessoa dos artefatos concretos entregues, utilidade prática gerada e consolidação fiel do feedback fornecido pela pessoa usuária às 3 perguntas prévias. Cumprir o piso mínimo de 100 palavras.]

---

## Glossário

[Apresentar uma lista explicativa de todos os termos técnicos, ferramentas, MCPs, arquivos ou conceitos de engenharia/IA citados no resumo, traduzindo-os de forma simples e acessível.]

- **[Termo Técnico / Ferramenta 1]**: [Explicação didática do conceito ou função do recurso utilizado].
- **[Termo Técnico / Ferramenta 2]**: [Explicação didática do conceito ou função do recurso utilizado].
```
