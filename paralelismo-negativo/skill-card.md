## Description: <br>
Diagnostica e corrige o paralelismo negativo (o vício de escrita "não é X, é Y") em textos fornecidos pela pessoa usuária, com metodologia inspirada no comando /doctor do Claude Code, adaptada à gramática do idioma do texto. <br>

This skill is ready for commercial/non-commercial use. <br>

## Owner
Mário Lúcio — skill pessoal, sem vínculo com a NVIDIA ou qualquer terceiro corporativo. <br>

### License/Terms of Use: <br>
Nenhuma licença formal definida (skill de uso pessoal, não distribuída sob licença de código aberto). <br>

## Use Case: <br>
Pessoas que escrevem, editam ou revisam textos (incluindo saídas de IA generativa) usam esta skill para identificar e corrigir o vício de paralelismo negativo antes de publicar ou compartilhar o conteúdo. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [A armadilha invisível nos textos de IA que trava o seu pensamento crítico (Romulo Corrêa)](references/artigo-romulo-correa.md) <br>
- [The Most Famous AI Writing Tic Is Also the Most Mysterious (The Atlantic)](references/artigo-the-atlantic.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Code] <br>
**Output Format:** [Markdown com estrutura fixa (Entendimento do texto, Investigação de paralelismo negativo, Remodelando o paralelismo negativo, Plano de ação) ou frase curta quando nenhuma ocorrência é encontrada; internamente, scripts/detectar_paralelismo.py produz um JSON determinístico de candidatos usado como piso mínimo antes do diagnóstico final] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Nenhuma edição é aplicada ao texto original sem autorização explícita da pessoa usuária] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter) <br>


