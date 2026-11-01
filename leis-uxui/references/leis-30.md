# As 30 leis de UX/UI

Os limiares são o padrão desta skill. Um limiar que cita WCAG é norma. Os outros limiares são heurísticas, e o perfil do entregável pode ajustar uma heurística.

L01 a L07 não têm números aqui. Os limiares dessas leis ficam na skill `gestalt`, para evitar duas fontes.

| ID | Lei | Etapa | Regra operacional | Limiar | Verificação |
|----|-----|-------|-------------------|--------|-------------|
| L01 | Proximidade | Perceber | Ver G01 | Ver G01 | Ver G01 |
| L02 | Semelhança | Perceber | Ver G02 | Ver G02 | Ver G02 |
| L03 | Conectividade uniforme | Perceber | Ver G03 | Ver G03 | Ver G03 |
| L04 | Região comum | Perceber | Ver G04 | Ver G04 | Ver G04 |
| L05 | Prägnanz | Perceber | Ver G05 | Ver G05 | Ver G05 |
| L06 | Destino comum | Perceber | Ver G06 | Ver G06 | Ver G06 |
| L07 | Continuidade | Perceber | Ver G07 | Ver G07 | Ver G07 |
| L08 | Efeito Von Restorff | Perceber | Destaque só o elemento-chave de cada tela, slide ou cartela | No máximo 1 elemento que quebra o padrão visual por tela, slide ou cartela | Conte os elementos que quebram o padrão em cada tela |
| L09 | Atenção seletiva | Perceber | Conteúdo crítico não pode parecer anúncio nem depender de carrossel automático | Zero informações obrigatórias só em banners ou carrosséis com troca automática | Liste o conteúdo obrigatório e localize cada item |
| L10 | Efeito estética-usabilidade | Perceber | Mantenha o acabamento consistente com tokens, sem ornamento que compita com a informação | 100% das cores, espaçamentos e fontes vêm de tokens declarados | Procure valores fixos fora dos tokens |
| L11 | Lei de Miller | Compreender | Agrupe em blocos o que a pessoa precisa reter | Blocos de 3 a 5 itens quando houver retenção; a regra não vale para menus de reconhecimento | Conte os itens de cada bloco que a pessoa precisa lembrar |
| L12 | Carga cognitiva | Compreender | Reduza decisões e ruído visual | No máximo 2 famílias tipográficas; no máximo 3 pesos por família | Liste as famílias e os pesos em uso |
| L13 | Modelo mental | Compreender | Use rótulos e estrutura na linguagem do público | Nenhum rótulo de navegação com jargão interno sem explicação | Leia cada rótulo como uma pessoa de fora |
| L14 | Lei de Jakob | Compreender | Siga as convenções de estrutura | Logotipo no topo à esquerda com link para o início; navegação no topo ou à esquerda; busca com ícone de lupa | Compare a estrutura com a convenção |
| L15 | Coerência e redundância (Mayer) | Compreender | Coloque uma ideia por slide ou cartela; não repita na tela o texto narrado | Título em forma de afirmação; no máximo 3 blocos de apoio por slide; zero parágrafos lidos na íntegra pela narração | Compare a tela com o roteiro de narração |
| L16 | Lei de Hick | Decidir e agir | Mantenha uma ação primária por tela ou seção | 1 CTA primário por seção; as outras ações têm peso visual menor | Conte os CTAs primários por seção |
| L17 | Sobrecarga de escolha | Decidir e agir | Limite as opções paralelas e indique a recomendada | Tabelas de planos com 3 ou 4 opções e 1 opção marcada como recomendada | Conte as opções e localize a recomendada |
| L18 | Lei de Fitts | Decidir e agir | Faça alvos grandes e próximos da ação | Mínimo de 24×24 px CSS (WCAG 2.2, 2.5.8, AA); recomendado 44×44 px | Meça os alvos; rode `lint_design.py` (LD-08) |
| L19 | Limiar de Doherty | Decidir e agir | Dê resposta visível e rápida a toda ação | Retorno visual em menos de 400 ms; indicador de progresso para ações acima de 1 s | Teste cada ação e meça o tempo de resposta |
| L20 | Paradoxo do usuário ativo | Decidir e agir | Dê ajuda no contexto, sem tutorial que bloqueia | Zero tutoriais obrigatórios antes do primeiro uso; dicas junto do campo | Percorra o primeiro uso sem ler nada |
| L21 | Lei de Parkinson | Decidir e agir | Encurte tarefas com padrões e preenchimento automático | Formulários com `autocomplete` nos dados pessoais; valores padrão quando houver resposta provável | Procure `autocomplete` nos campos |
| L22 | Efeito de posição serial | Lembrar e continuar | Coloque os itens críticos nas extremidades | Ação ou mensagem mais importante na primeira ou na última posição de listas, menus e decks | Localize o item mais importante de cada lista |
| L23 | Regra do pico-fim | Lembrar e continuar | Defina o pico e o encerramento | Todo motion e todo deck têm um pico e um encerramento com chamada ou síntese declarados no roteiro | Localize o pico e o encerramento no roteiro |
| L24 | Efeito Zeigarnik | Lembrar e continuar | Mostre o que falta concluir | Fluxos com 3 ou mais passos exibem "Passo X de Y" ou barra de progresso | Percorra os fluxos com 3 ou mais passos |
| L25 | Efeito gradiente de meta | Lembrar e continuar | Mostre o avanço; comece com progresso parcial quando esse progresso for legítimo | Indicador de progresso visível em fluxos de várias etapas | Confira o indicador em cada etapa |
| L26 | Navalha de Occam | Sistema | Faça cada elemento justificar a própria função | Todo elemento removível sem perda de informação ou função é removido | Teste a remoção de cada elemento |
| L27 | Lei de Tesler | Sistema | Deixe o sistema absorver a complexidade | Valores padrão inteligentes; nenhum campo pede o que o sistema já sabe | Compare cada campo com os dados disponíveis |
| L28 | Lei de Postel | Sistema | Aceite formatos variados de entrada | Campos de telefone, data e CPF aceitam entrada com e sem máscara | Teste cada campo com e sem máscara |
| L29 | Lei de Murphy | Sistema | Preveja falha em todo componente | Todo componente com dados define os estados vazio, carregando, erro e sucesso | Confira os 4 estados de cada componente |
| L30 | Princípio de Pareto | Sistema | Priorize os 20% mais usados | O design system documenta primeiro os componentes de maior uso; a navegação expõe primeiro os fluxos mais usados | Compare a ordem com os dados de uso |
