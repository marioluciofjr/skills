# Explicação Detalhada: Módulos de um Prompt Estruturado

A estrutura modular de prompts foi desenvolvida para garantir máxima precisão, reprodutibilidade e eficácia ao comandar agentes de Inteligência Artificial. Cada módulo desempenha um papel fundamental. O preenchimento deve ser o mais qualificado possível.

## 1. ## persona
A **persona** define o papel, a identidade, o conjunto de habilidades e o nível de expertise que a IA deve assumir ao realizar a tarefa.
* **Por que é importante:** Modelos de linguagem baseiam sua forma de comunicação e profundidade técnica na identidade assumida. Uma persona genérica gera respostas genéricas; uma persona específica ("Engenheiro DevOps Sênior") gera jargões precisos e soluções consistentes com esse nível.
* **O que incluir:** Profissão, anos de experiência, tom de voz (formal, didático, irônico), viés analítico e principais focos de atuação.

## 2. ## contexto
O **contexto** fornece o pano de fundo histórico, o estado atual do problema ou do projeto e a motivação para a tarefa. 
* **Por que é importante:** A IA não sabe o que aconteceu antes da interação atual. Sem contexto, ela pode fazer suposições incorretas. O contexto ancora a IA na realidade do usuário.
* **O que incluir:** O cenário da empresa/usuário, o problema exato que precisa ser resolvido, o público-alvo do resultado final, e o que já foi tentado antes.

## 3. ## tarefa
A **tarefa** é a instrução direta, clara e acionável sobre o que o agente deve fazer.
* **Por que é importante:** É o núcleo lógico do prompt. Se a tarefa for confusa ou misturar a etapa de raciocínio, o resultado será inútil ou incompleto.
* **O que incluir:** Verbos de ação diretos no imperativo positivo (crie, analise, extraia, resuma). Se o processo for complexo ou exigir múltiplas avaliações, divida-o obrigatoriamente em passos numéricos (1, 2, 3...) para induzir um "pensamento passo a passo" no agente.

## 4. ## formato
O **formato** define exatamente como o output deve ser estruturado visualmente, tecnicamente e sintaticamente.
* **Por que é importante:** Facilita a integração do resultado em outros sistemas ou a leitura humana impecável. Bloqueia respostas livres que não podem ser parseadas em outras ferramentas.
* **O que incluir:** Estrutura desejada (ex: JSON puro, tabela Markdown, lista com marcadores, código Python em bloco), placeholders essenciais obrigatórios, e limites de contagem (ex: "máximo de 150 palavras", "exatamente 5 parágrafos").

## 5. ## regras
As **regras** estabelecem limites inegociáveis, restrições perigosas ou comportamentos frequentes não desejados (guardrails).
* **Por que é importante:** Previne alucinações ("hallucinations"), excessos de cortesia inúteis ("Aqui está o seu texto:") e garante a compatibilidade e a conformidade (compliance) da resposta. Útil para reprimir o instinto natural do LLM de adicionar disclaimers desnecessários.
* **O que incluir:** Proibições explícitas. (Ex: "Não mude o sentido do texto base", "Não escreva introduções ou conclusões", "Respeite totalmente a ausência de saudações", "Jamais inclua a formatação ```json").
