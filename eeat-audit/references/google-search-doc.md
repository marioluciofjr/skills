# Documentação Oficial do Google Search

Este arquivo sintetiza as diretrizes do Google Search Central usadas na auditoria.

## Índice

1. Conteúdo útil e centrado em pessoas (Helpful Content)
2. Políticas de spam da Pesquisa Google
3. Conteúdo gerado por IA
4. Guia de otimização para recursos de IA na Pesquisa
5. Fundamentos de SEO on-page
6. Como funciona a Pesquisa Google
7. Aviso de verificação

---

## 1. Conteúdo útil e centrado em pessoas (Helpful Content)

URL: `https://developers.google.com/search/docs/fundamentals/creating-helpful-content`

Este é o documento operacional mais importante da auditoria. Ele traz a lista de autoavaliação que o Google recomenda ao criador de conteúdo. Use-a na seção 4 do template de saída.

### Perguntas de conteúdo e qualidade

- O conteúdo apresenta informação original, relato, pesquisa ou análise própria?
- O conteúdo oferece descrição substancial e completa do tópico?
- O conteúdo traz análise interessante ou informação não óbvia?
- Quando cita outras fontes, o conteúdo acrescenta valor e originalidade em vez de copiar?
- O título descreve o conteúdo de forma útil, sem exagero e sem choque?
- A pessoa se sentiria confortável ao indicar este conteúdo a um amigo?
- A pessoa esperaria ver este conteúdo em uma revista, enciclopédia ou livro impresso?

### Perguntas de especialidade

- O conteúdo apresenta informação de modo a transmitir confiança na fonte?
- O conteúdo é produzido por pessoa com conhecimento comprovado do assunto?
- O site tem propósito principal claro?
- Após ler, a pessoa sente que pode confiar na informação para agir?
- O conteúdo tem erro factual, ortográfico ou de produção que sugira descuido?

### Perguntas de foco na pessoa

- O site tem público definido que consideraria o conteúdo útil?
- O conteúdo demonstra experiência em primeira mão ou profundidade de conhecimento?
- A pessoa sai da página sentindo que aprendeu o suficiente sobre o tema?
- A pessoa sai satisfeita, sem necessidade de nova busca pelo mesmo assunto?

### Sinais de conteúdo feito para o mecanismo de busca

Estes sinais indicam produção voltada ao ranking, não à pessoa. Registre cada ocorrência como evidência.

- O conteúdo existe apenas porque parece haver tráfego disponível no tópico.
- O site produz volume alto sobre temas variados, sem foco definido.
- O texto resume o que outros dizem, sem acrescentar valor.
- O conteúdo escreve sobre assunto da moda apenas para capturar busca.
- O texto tem tamanho definido por uma contagem arbitrária de palavras.
- O conteúdo promete responder a uma pergunta sem resposta confirmada.

---

## 2. Políticas de spam da Pesquisa Google

URL: `https://developers.google.com/search/docs/essentials/spam-policies`

Verifique estas violações. Cada ocorrência reduz a Confiabilidade e pode zerar o pilar.

- **Abuso de conteúdo em escala.** Produção em massa de páginas com pouco valor, com o objetivo principal de manipular o ranking. A política independe do método de produção: humano, automação ou IA.
- **Conteúdo raspado.** Reprodução de conteúdo de terceiros sem valor agregado.
- **Cloaking.** Entrega de conteúdo diferente ao rastreador e à pessoa.
- **Texto oculto e links ocultos.** Conteúdo invisível ao leitor e visível ao rastreador.
- **Preenchimento de palavras-chave.** Repetição de termo fora do uso natural.
- **Abuso de reputação do site.** Publicação de conteúdo de terceiros que explora a autoridade do domínio hospedeiro.
- **Links não naturais.** Compra de link ou troca em escala com intenção de manipular ranking.
- **Páginas de entrada.** Conjunto de páginas próximas criado apenas para capturar variações de busca.

---

## 3. Conteúdo gerado por IA

URL: `https://developers.google.com/search/docs/fundamentals/using-gen-ai-content`

- **Foco na pessoa.** O Google recompensa conteúdo original e confiável criado prioritariamente para pessoas, independentemente de ter sido produzido por humano, automação ou IA.
- **Abuso em escala.** O uso de IA para produzir páginas em massa sem valor agregado, com o objetivo primário de manipular ranking, viola as políticas de spam.
- **Esforço e originalidade.** Conteúdo produzido com pouco esforço, sem agregação de valor e sem perspectiva analítica sofre desvalorização.
- **Transparência.** Forneça contexto ao leitor sobre a metodologia e o uso de ferramentas de IA quando isso for relevante para a compreensão da precisão.
- **Imagens geradas por IA.** Mantenha os metadados IPTC padrão, incluindo `DigitalSourceType`.

---

## 4. Guia de otimização para recursos de IA na Pesquisa

URL: `https://developers.google.com/search/docs/fundamentals/ai-optimization-guide`

- **Fundamento.** Otimizar para recursos generativos, como AI Overviews e AI Mode, segue os mesmos fundamentos de SEO de alta qualidade.
- **Conteúdo não comoditizado.** O Google valoriza perspectiva única, dado original e relato de experiência direta, elementos que sistemas automatizados não reproduzem sozinhos.
- **Acesso técnico.** Garanta que os rastreadores acessem o conteúdo: renderização de JavaScript, código HTTP 200 e ausência de bloqueio indevido no `robots.txt`.
- **Dados estruturados.** A marcação Schema.org deve corresponder exatamente ao conteúdo visível na página.
- **Riqueza multimodal.** Use imagem de alta resolução e vídeo relevante, com metadados claros.
- **Práticas rejeitadas.** O Google descarta truques como criação de arquivos artificiais do tipo `llms.txt` e fragmentação forçada de texto sem coesão.

---

## 5. Fundamentos de SEO on-page

URL: `https://developers.google.com/search/docs/fundamentals/seo-starter-guide`

- **Título (`<title>`).** Único, descritivo e conciso para cada documento.
- **Meta descrição.** Resumo informativo e preciso do conteúdo.
- **Hierarquia de cabeçalhos.** Uso correto de `H1`, `H2` e `H3` para organizar a leitura.
- **Texto âncora.** Descritivo, sem expressão genérica do tipo "clique aqui".
- **Mídia.** Atributo `alt` contextual e nome de arquivo legível.

---

## 6. Como funciona a Pesquisa Google

URL: `https://developers.google.com/search/docs/fundamentals/how-search-works`

Três estágios:

1. **Rastreamento.** O Googlebot baixa código, texto, imagem e vídeo das páginas descobertas.
2. **Indexação.** O sistema processa o conteúdo, renderiza JavaScript, interpreta termos e agrupa variantes para selecionar a versão canônica.
3. **Exibição e classificação.** Os algoritmos selecionam os resultados mais úteis considerando relevância, localização, dispositivo, idioma e qualidade geral.

Páginas com conteúdo duplicado, texto de baixa qualidade ou bloqueio técnico podem ser descartadas na indexação.

---

## 7. Aviso de verificação

Todas as páginas acima são documentos vivos. O Google as revisa sem aviso.

Quando o diagnóstico depender de um critério específico dessas páginas, confirme o texto vigente antes de citá-lo. Nunca atribua ao Google um critério que a página não declara.
