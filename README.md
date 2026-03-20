# skills
Repositório com minhas skills para Claude, Claude Code, Antigravity, Opencode, Agno, ADK, OpenClaw, Windsurf, Qwen Code e demais sistemas agênticos.

[![Made with Python](https://img.shields.io/badge/Python->=3.10-blue?logo=python&logoColor=white)](https://python.org "Go to Python homepage")
![license - Apache 2.0](https://img.shields.io/badge/license-Apache2.0-green)
![site - prazocerto.me](https://img.shields.io/badge/site-prazocerto.me-230023)
![linkedin - @marioluciofjr](https://img.shields.io/badge/linkedin-marioluciofjr-blue)

## Índice

* [Introdução](#introdução)
* [Estrutura do projeto](#estrutura-do-projeto)
* [Como adicionar uma skill deste repositório no Claude](#como-adicionar-uma-skill-deste-repositório-no-claude)
* [Como adicionar uma skill deste repositório no Antigravity](#como-adicionar-uma-skill-deste-repositório-no-antigravity)
* [Tecnologias utilizadas](#tecnologias-utilizadas)
* [Links úteis](#links-úteis)
* [Contribuições](#contribuições)
* [Licença](#licença)
* [Contato](#contato)

## Introdução
Este repositório reúne variadas skills para serem utilizadas em sistemas agênticos. Para saber mais detalhes sobre o conceito de skills e sua estrutura, basta verificar a seção de [Links úteis](#links-úteis).

## Estrutura do projeto
Cada pasta é uma skill diferente. Para baixar os arquivos .ZIP de maneira separada, só acessar os links abaixo:
* [prompt-personagem](https://downgit.github.io/#/home?url=https://github.com/marioluciofjr/skills/tree/main/prompt-personagem)
* [alt-text](https://downgit.github.io/#/home?url=https://github.com/marioluciofjr/skills/tree/main/alt-text)
* [prompt-estruturado](https://downgit.github.io/#/home?url=https://github.com/marioluciofjr/skills/tree/main/prompt-estruturado)
* [analise-semiotica](https://downgit.github.io/#/home?url=https://github.com/marioluciofjr/skills/tree/main/analise-semiotica)
* [prompt-skills](https://downgit.github.io/#/home?url=https://github.com/marioluciofjr/skills/tree/main/prompt-skills)
* [calculadora-cdi](https://downgit.github.io/#/home?url=https://github.com/marioluciofjr/skills/tree/main/calculadora-cdi)
* [bbb-estatisticas](https://downgit.github.io/#/home?url=https://github.com/marioluciofjr/skills/tree/main/bbb-estatisticas)
* [diagrama-mermaid](https://downgit.github.io/#/home?url=https://github.com/marioluciofjr/skills/tree/main/diagrama-mermaid)
* [analise-swot](https://downgit.github.io/#/home?url=https://github.com/marioluciofjr/skills/tree/main/analise-swot)
* [discurso-tadeu](https://downgit.github.io/#/home?url=https://github.com/marioluciofjr/skills/tree/main/discurso-tadeu)

## Como adicionar uma skill deste repositório no Claude

O passo a passo é bem simples: 

1. Em [Estrutura do projeto](#estrutura-do-projeto), clique no link da skill que deseja baixar a pasta .ZIP
2. Entre no [Claude](https://claude.ai/new)
3. Acesse o ícone 'Personalizar' ![Image](https://github.com/user-attachments/assets/0939a2d2-28f0-49f7-b527-00c0f7fc5fc4)
4. Clique em 'Habilidades' ![Image](https://github.com/user-attachments/assets/f5a31a26-34f8-43cd-b19d-5c8443d810ac) ou 'Criar novas habilidades' ![Image](https://github.com/user-attachments/assets/524bda5b-3477-4ebb-863a-211f8e7e1e9b)
5. Clique no ícone de adicionar nova habilidade ![Image](https://github.com/user-attachments/assets/3d9b6977-7229-45f9-8f7d-443a19c173bf)
6. Escolha a opção 'Fazer upload de uma nova habilidade'
7. Faça o upload da pasta .ZIP que acabou de baixar deste repositório

Se tiver dúvidas, só acessar os [Links úteis](#links-úteis)

## Como adicionar uma skill deste repositório no Antigravity
<img width="348" height="170" alt="Image" src="https://github.com/user-attachments/assets/145da45d-dc81-47e6-8a38-d2ad5a0519d0" /><br><br>

Delegue essa tarefa para o Antigravity instalar a skill. Basta só colocar este prompt abaixo no Agent do Antigravity e dar ENTER:

```text
## contexto
DIRETÓRIO PRINCIPAL = .gemini\antigravity
COMANDO = npx skills add https://github.com/marioluciofjr/skills --skill NOME DA SKILL

## tarefa
Pense passo a passo para executar a tarefa:
1 - Busque o DIRETÓRIO PRINCIPAL
2 - Use o COMANDO e dê enter
3 - Em `Additional agents`, procure por 'Antigravity' (pode aparecer como primeira opção inclusive), basta clicar em enter
4 - Em `Installation scope`, escolha a opção 'Project' e dê enter
5 - Em Installation method`, escolha 'Symlink' e dê enter
6 - Em `Proceed with installation?, confirme com 'Yes' e dê enter
7 - Verifique se a instalação deu certo, pois deve aparecer `◇  Installation complete`
8 - Verifique se no DIRETÓRIO PRINCIPAL já tem uma pasta chamada skills. Se tiver, pule para a próxima etapa. Se não tiver, crie para ficar assim .gemini\antigravity\skills
9 - Mova as skills deste diretório .gemini\antigravity\.agents\skills\ para este diretório .gemini\antigravity\skills
10 - Exclua as pastas .gemini\antigravity\.agents e .gemini\antigravity\.agent
11 - Exclua o arquivo skills-lock.json
12 - Finalize a tarefa
```

Se tiver dúvidas, só acessar os [Links úteis](#links-úteis)

## Tecnologias utilizadas

<div>
  <img align="center" height="60" width="80" src="https://camo.githubusercontent.com/a5c02c148c39e94df1be062d9ba35c3e2154aede22f8e95476492059ed5b3a1b/68747470733a2f2f63646e2e6a7364656c6976722e6e65742f67682f64657669636f6e732f64657669636f6e406c61746573742f69636f6e732f707974686f6e2f707974686f6e2d6f726967696e616c2d776f72646d61726b2e737667" />&nbsp;&nbsp;&nbsp
  <img align="center" height="60" width="80" src="https://camo.githubusercontent.com/0d1832aec3509ce9c986e93f33c112c2da495e818f579e1dc1f03da116e5d9c4/68747470733a2f2f63646e2e6a7364656c6976722e6e65742f67682f64657669636f6e732f64657669636f6e406c61746573742f69636f6e732f79616d6c2f79616d6c2d6f726967696e616c2e737667" />&nbsp;&nbsp;&nbsp
  <img align="center" height="60" width="80" src="https://camo.githubusercontent.com/ecba9820693ce92df70da152652c07adedcc44b5ee7dbc02ff863c6b546ec469/68747470733a2f2f63646e2e6a7364656c6976722e6e65742f67682f64657669636f6e732f64657669636f6e406c61746573742f69636f6e732f6d61726b646f776e2f6d61726b646f776e2d6f726967696e616c2e737667" />&nbsp;&nbsp;&nbsp
  <img align="center" height="60" width="80" src="https://github.com/lobehub/lobe-icons/raw/master/packages/static-svg/icons/antigravity-color.svg" />&nbsp;&nbsp;&nbsp
 </div><br>

* Python
* Yaml
* Markdown
* Antigravity

## Links úteis

* [Como criar Skills personalizadas](https://support.claude.com/pt/articles/12512198-como-criar-skills-personalizadas) - Documentação prática da Anthropic sobre Skills.
* [Skills - Anthropic](https://github.com/anthropics/skills/tree/main) - Repositório oficial da Anthropic sobre Skills.
* [What are skills?](https://agentskills.io/what-are-skills) - Explicação detalhada sobre agent skills.
* [Agent Skills](https://antigravity.google/docs/skills) - Documentação do Google Antigravity sobre Agent Skills.
* [Usando Skills no Claude](https://support.claude.com/pt/articles/12512180-usando-skills-no-claude) - Documentação da Anthropic sobre como usar skills no Claude.
* [Como instalar o VSCode](https://code.visualstudio.com/download)- Link direto para download.
* [Como baixar o Antigravity](https://antigravity.google/download) - Página oficial de download da IDE do Google DeepMind.
* [Documentação oficial do pacote uv](https://docs.astral.sh/uv/) - Você saberá todos os detalhes sobre o `uv` e como ele é importante no Python.
* [venv — Criação de ambientes virtuais](https://docs.python.org/pt-br/3/library/venv.html) - Explicação completa de como funcionam os venvs.
* [Conjunto de ícones de modelos de IA/LLM](https://lobehub.com/pt-BR/icons) - site muito bom para conseguir ícones do ecossistema de IA.
* [Devicon](https://devicon.dev/) - site bem completo também com ícones gerais sobre tecnologia.
* [DownGit](https://downgit.github.io/#/home) - Gera downloads automáticos de pastas zip a partir de arquivos específicos em repositórios do GitHub.
* [Skills.sh](https://skills.sh) - Biblioteca completa da Vercel com várias skills disponíveis gratuitamente.
* [Mermaid](https://github.com/mermaid-js/mermaid) - Repositório oficial da linguagem Mermaid.


## Contribuições

Contribuições são bem-vindas! Se você tem ideias para melhorar este projeto, sinta-se à vontade para fazer um fork do repositório.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](https://github.com/marioluciofjr/skills/blob/main/LICENSE) para detalhes.

## Contato
    
Mário Lúcio - Prazo Certo®
<div>  	
  <a href="https://www.linkedin.com/in/marioluciofjr" target="_blank"><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a> 
  <a href = "mailto:marioluciofjr@gmail.com" target="_blank"><img src="https://img.shields.io/badge/-Gmail-%23333?style=for-the-badge&logo=gmail&logoColor=white"></a>
  <a href="https://prazocerto.me/contato" target="_blank"><img src="https://img.shields.io/badge/prazocerto.me/contato-230023?style=for-the-badge&logo=wordpress&logoColor=white"></a>
</div> 

