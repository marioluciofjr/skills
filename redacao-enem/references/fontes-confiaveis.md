# Fontes confiáveis para textos motivadores

Este arquivo é a **lista autorizada** da skill. Todo texto motivador precisa vir de uma fonte listada aqui. Todas as fontes foram citadas em algum caderno do Enem de 2017 a 2025, na proposta de redação ou nas questões de Linguagens e Ciências Humanas.

- **Coleta:** extração automática das referências "Disponível em:" dos 9 cadernos inteiros (419 referências, 310 domínios), filtradas por relevância brasileira e natureza institucional, jornalística, acadêmica ou cultural.
- **Verificação de acesso:** em 23/09/2026, a página principal de cada domínio foi aberta por um robô de IA (ferramenta de navegação do Claude), sem login, API ou assinatura. Páginas internas podem mudar com o tempo. Por isso, o passo 2 do protocolo é sempre obrigatório.

## 1. Protocolo obrigatório (guardrail de transparência)

A skill segue estes passos para **cada** texto motivador, sem exceção:

1. **Domínio autorizado:** a URL pertence a uma fonte do Nível A (seção 3) ou, como último recurso, do Nível B (seção 4).
2. **Página aberta na sessão:** a IA abre a URL exata com a ferramenta de navegação **na conversa atual**. Não vale lembrança, dedução ou URL "provável".
   - **Descarte imediato, sem nova tentativa:** diante de erro 403, 429 ou 5xx, tempo esgotado, erro de certificado ou alerta de segurança, login, paywall, "conteúdo restrito" ou "página desativada", a fonte é descartada na hora. **Não reabra o mesmo endereço**: passe direto para outro domínio da lista.
   - **Orçamento:** no máximo 8 buscas e 10 aberturas de página por tema, com até 2 aberturas por posição. Prefira páginas HTML: PDFs e arquivos pesados costumam falhar.
3. **Trecho literal:** o texto é copiado **palavra por palavra** da página aberta, com **70 a 85 palavras** (o mais perto possível de 85). A única edição permitida é o **corte**, marcado com `[...]`. Nunca reescrever, resumir, trocar palavras ou juntar frases de lugares diferentes sem `[...]`.
   - Algumas ferramentas de navegação **resumem** a página. Peça sempre a transcrição literal. Se a ferramenta devolver lista, tópicos ou "informações-chave", isso **não** é o texto da fonte e não pode ser usado.
   - **Não corrija** erros da fonte (ex.: um erro de digitação no original). Se o erro atrapalhar, corte o trecho com `[...]`.
4. **Rótulo correto:**
   - `(adaptado)`: houve corte de trechos.
   - `(fragmento)`: trecho contínuo de obra maior (lei, poema, letra).
   - Sem rótulo: o trecho está completo.
5. **Referência no padrão Enem:** `AUTOR. **Título**. Disponível em: URL. Acesso em: DD mês AAAA.` Sem autor identificado, começar por "Disponível em:". A data de acesso é a **data real** da consulta, e a URL é a **URL exata** aberta.
6. **Dados numéricos:** para o texto de dados, **prefira fontes que já tenham gráfico, infográfico ou tabela** (ex.: IBGE, Ipea). Os dados viram uma **tabela Markdown de até 5 linhas**, com rótulos e números **exatamente** como aparecem na fonte (mesmas casas decimais e unidades), título e "Fonte: …" como na página original. Se houver linhas cortadas, use `(adaptado)`. Se os números estão em **texto corrido**, eles ficam no trecho verbal literal (como no Enem 2025, Texto I): **nunca converta parágrafo em tabela**. Nunca estime, arredonde ou complete números.
7. **Sem fonte suficiente, sem proposta:** se não houver 4 textos que cumpram os passos 1 a 6, a skill sorteia **outro tema**. Nunca completa com invenção.

### Sinais de alerta (descarte imediato)

- Página sem data **ou** sem autoria/instituição responsável.
- Dado numérico sem origem declarada.
- Conteúdo contestado por agência de checagem ou por fonte oficial mais recente.
- Página de opinião anônima, fórum, rede social, loja virtual ou conteúdo patrocinado.
- Domínio que mudou de dono ou de finalidade (ver seção 5).
- Conteúdo que viole os princípios de direitos humanos da cartilha (ver `cartilha-enem-2026.md`).

## 2. Legenda

- **Uso no Enem:** `M` = texto motivador da proposta de redação; `Q` = texto-base de questão objetiva.
- **Nível A:** abriu normalmente para o robô de IA na verificação.
- **Nível B:** público e gratuito, mas bloqueia alguns robôs de IA. É **último recurso**: só entra quando o Nível A falhar naquela posição, e só se abrir de fato na sessão (passo 2).

## 3. Nível A — 100 fontes verificadas

### 3.1 Estatística, pesquisa e ciência oficial (6)

| # | Fonte | Domínio | Anos no Enem | Uso |
|---|---|---|---|---|
| 1 | IBGE – Instituto Brasileiro de Geografia e Estatística | ibge.gov.br | 2018, 2019, 2022, 2023, 2025 | M, Q |
| 2 | Ipea – Instituto de Pesquisa Econômica Aplicada | ipea.gov.br | 2021 | Q |
| 3 | Repositório do Ipea | repositorio.ipea.gov.br | 2023 | M |
| 4 | Embrapa | embrapa.br | 2021 | Q |
| 5 | Fiocruz – Fundação Oswaldo Cruz | fiocruz.br | 2020 | Q |
| 6 | DIHS/ENSP – Direitos Humanos, Saúde e Diversidade Cultural (Fiocruz) | dihs.ensp.fiocruz.br | 2020 | Q |

### 3.2 Legislação, Justiça e Ministério Público (5)

| # | Fonte | Domínio | Anos no Enem | Uso |
|---|---|---|---|---|
| 7 | Legislação do Senado (texto integral de leis, espelho do Planalto) | legis.senado.leg.br | 2018 | Q |
| 8 | Senado Notícias / Agência Senado | www12.senado.leg.br | 2021, 2022, 2024, 2025 | M, Q |
| 9 | TJDFT – Tribunal de Justiça do DF e Territórios | tjdft.jus.br | 2025 | Q |
| 10 | Ministério Público do Rio Grande do Sul | mprs.mp.br | 2020 | Q |
| 11 | Ministério Público do Trabalho – RS | prt4.mpt.mp.br | 2017 | M |

### 3.3 Governo federal e governos estaduais (10)

> **Portal gov.br inteiro:** o Enem cita o portal do Governo Federal como fonte (`brasil.gov.br` em 2017; `gov.br` em 2025). Por isso, **qualquer órgão federal** dentro de `gov.br` ou com domínio `.gov.br` (ex.: gov.br/cidades, gov.br/mcti, cemaden) é fonte autorizada, com o mesmo protocolo.
>
> **Atenção ao defeso eleitoral:** em anos de eleição (em geral, de julho a outubro), páginas de notícias de ministérios no gov.br e da Agência Gov/EBC podem ficar **temporariamente desativadas** ("Em respeito à legislação eleitoral vigente, esta página está desativada temporariamente"; em 23/09/2026 também "Conteúdo Restrito"). Nesses casos, use Agência Brasil, Senado Notícias, legis.senado.leg.br, IBGE, Ipea ou universidades públicas.

| # | Fonte | Domínio | Anos no Enem | Uso |
|---|---|---|---|---|
| 12 | Ministério do Esporte | gov.br/esporte | 2022, 2025 | Q |
| 13 | Ministério do Desenvolvimento e Assistência Social (MDS) | gov.br/mds | 2022 | M |
| 14 | Ministério da Educação (MEC) | gov.br/mec | 2020 | Q |
| 15 | Ministério do Meio Ambiente e Mudança do Clima | gov.br/mma | 2019 | Q |
| 16 | Ministério do Trabalho e Emprego | gov.br/trabalho-e-emprego | 2019 | Q |
| 17 | Iphan – Instituto do Patrimônio Histórico e Artístico Nacional | gov.br/iphan | 2021, 2023 | Q |
| 18 | Ancine – Agência Nacional do Cinema | gov.br/ancine | 2019 | M |
| 19 | Secretaria da Saúde do Paraná | saude.pr.gov.br | 2020 | M |
| 20 | Secretaria de Cultura e Economia Criativa do RJ | cultura.rj.gov.br | 2019 | Q |
| 21 | Defesa Civil do Rio Grande do Sul | defesacivil.rs.gov.br | 2024 | Q |

### 3.4 Comunicação pública (3)

| # | Fonte | Domínio | Anos no Enem | Uso |
|---|---|---|---|---|
| 22 | EBC – Empresa Brasil de Comunicação | ebc.com.br | 2020 | Q |
| 23 | Agência Brasil | agenciabrasil.ebc.com.br | 2019, 2022 | Q |
| 24 | TV Brasil | tvbrasil.ebc.com.br | 2024 | Q |

### 3.5 Organismos internacionais, terceiro setor e entidades (13)

| # | Fonte | Domínio | Anos no Enem | Uso |
|---|---|---|---|---|
| 25 | ONU Brasil | brasil.un.org | 2018, 2021 | Q |
| 26 | Nações Unidas (portal em português) | un.org/pt | 2025 | Q |
| 27 | UNICEF Brasil | unicef.org/brazil | 2025 | Q |
| 28 | Oxfam Brasil | oxfam.org.br | 2023 | M |
| 29 | WRI Brasil | wribrasil.org.br | 2024 | Q |
| 30 | Instituto Patrícia Galvão | agenciapatriciagalvao.org.br | 2017 | Q |
| 31 | Abrata – Associação Brasileira de Transtornos Afetivos | abrata.org.br | 2020 | M |
| 32 | SBGG – Sociedade Brasileira de Geriatria e Gerontologia | sbgg.org.br | 2023 | Q |
| 33 | AGB – Associação dos Geógrafos Brasileiros | agb.org.br | 2025 | Q |
| 34 | ABL – Academia Brasileira de Letras | academia.org.br | 2018 | Q |
| 35 | CNA – Confederação da Agricultura e Pecuária do Brasil | cnabrasil.org.br | 2025 | Q |
| 36 | Sesc Ceará | fecomercio-ce.com.br/sescce | 2025 | Q |
| 37 | CPB – Comitê Paralímpico Brasileiro | cpb.org.br | 2024 | Q |

### 3.6 Academia e divulgação científica (22)

| # | Fonte | Domínio | Anos no Enem | Uso |
|---|---|---|---|---|
| 38 | SciELO Brasil | scielo.br | 2025 | Q |
| 39 | Portal de Periódicos da UFBA | periodicos.ufba.br | 2025 | Q |
| 40 | Jornal da USP | jornal.usp.br | 2025 | Q |
| 41 | Jornal da Unesp | jornal.unesp.br | 2024 | M |
| 42 | Comunica UFU (Universidade Federal de Uberlândia) | comunica.ufu.br | 2025 | Q |
| 43 | Revista Pesquisa FAPESP | revistapesquisa.fapesp.br | 2021, 2023 | M, Q |
| 44 | FGV CPDOC | cpdoc.fgv.br | 2018, 2021 | Q |
| 45 | Museu Nacional / UFRJ | museunacional.ufrj.br | 2018 | Q |
| 46 | Humanista – Jornalismo e Direitos Humanos (UFRGS) | ufrgs.br/humanista | 2021 | M |
| 47 | UFES – Universidade Federal do Espírito Santo | ufes.br | 2024 | Q |
| 48 | UEL – Universidade Estadual de Londrina | uel.br | 2025 | Q |
| 49 | HISTEDBR/Unicamp | histedbr.fe.unicamp.br | 2021 | Q |
| 50 | DEG – Discurso & Gramática (UFF) | deg.uff.br | 2025 | Q |
| 51 | Revista Ciência Hoje | cienciahoje.org.br | 2019 | Q |
| 52 | Revista Ciência e Cultura (SBPC) | cienciaecultura.bvs.br | 2023 | Q |
| 53 | ANPUH-Rio – História & Parcerias | historiaeparcerias2019.rj.anpuh.org | 2024 | Q |
| 54 | Fapcom – Faculdade Paulus de Tecnologia e Comunicação | fapcom.edu.br | 2024 | Q |
| 55 | Uninter Notícias | uninter.com | 2025 | Q |
| 56 | Ludopédio | ludopedio.org.br | 2020 | Q |
| 57 | MIT Technology Review Brasil | mittechreview.com.br | 2023 | Q |
| 58 | SoCientífica | socientifica.com.br | 2024 | Q |
| 59 | Revista Planeta | revistaplaneta.com.br | 2020 | Q |

### 3.7 Imprensa (25)

| # | Fonte | Domínio | Anos no Enem | Uso |
|---|---|---|---|---|
| 60 | CartaCapital | cartacapital.com.br | 2017, 2018, 2021, 2022, 2023 | Q |
| 61 | Correio Braziliense | correiobraziliense.com.br | 2021, 2023, 2024 | Q |
| 62 | CNN Brasil | cnnbrasil.com.br | 2022, 2024 | Q |
| 63 | Outras Palavras | outraspalavras.net | 2018, 2021 | M, Q |
| 64 | Agência Pública | apublica.org | 2020 | Q |
| 65 | Observatório da Imprensa | observatoriodaimprensa.com.br | 2021 | Q |
| 66 | O Povo (CE) | opovo.com.br | 2018, 2021 | Q |
| 67 | Jornal Correio (BA) | correio24horas.com.br | 2025 | Q |
| 68 | ICL Notícias | iclnoticias.com.br | 2025 | Q |
| 69 | Exame | exame.com | 2020 | Q |
| 70 | Conexão Planeta | conexaoplaneta.com.br | 2021 | Q |
| 71 | Migalhas | migalhas.com.br | 2020 | Q |
| 72 | Lunetas | lunetas.com.br | 2024 | Q |
| 73 | Meio & Mensagem | meioemensagem.com.br | 2019 | M |
| 74 | ND Mais (SC) | ndmais.com.br | 2022 | Q |
| 75 | DOL – Diário Online (PA) | dol.com.br | 2024 | Q |
| 76 | O Imparcial (MA) | oimparcial.com.br | 2024 | Q |
| 77 | Tribuna PR | tribunapr.com.br | 2024 | Q |
| 78 | Folha de Londrina | folhadelondrina.com.br | 2019 | Q |
| 79 | O Popular (GO) | opopular.com.br | 2023 | Q |
| 80 | Catraca Livre | catracalivre.com.br | 2019 | Q |
| 81 | Vida Simples | vidasimples.co | 2020 | Q |
| 82 | Revista Encontro (MG) | revistaencontro.com.br | 2022 | Q |
| 83 | Portal do Trânsito | portaldotransito.com.br | 2022, 2023 | Q |
| 84 | Ambientebrasil | ambientes.ambientebrasil.com.br | 2020 | Q |

### 3.8 Cultura, artes e literatura (16)

| # | Fonte | Domínio | Anos no Enem | Uso |
|---|---|---|---|---|
| 85 | MASP – Museu de Arte de São Paulo | masp.com.br | 2021, 2025 | Q |
| 86 | Pinacoteca de São Paulo | pinacoteca.org.br | 2025 | Q |
| 87 | Rascunho (jornal literário) | rascunho.com.br | 2023, 2025 | M, Q |
| 88 | Revista Bula | revistabula.com | 2019, 2024 | Q |
| 89 | Escritas (poesia) | escritas.org | 2023 | Q |
| 90 | Vinicius de Moraes (site oficial) | viniciusdemoraes.com.br | 2019 | Q |
| 91 | Graciliano Ramos (site oficial) | graciliano.com.br | 2024 | Q |
| 92 | Prêmio PIPA | premiopipa.com | 2024 | Q |
| 93 | MAI – Museu de Arte Indígena | maimuseu.com.br | 2024 | Q |
| 94 | Dasartes | dasartes.com.br | 2022 | Q |
| 95 | PublishNews | publishnews.com.br | 2025 | Q |
| 96 | Grupo Corpo | grupocorpo.com.br | 2023 | Q |
| 97 | Coleção BEI – Bancos Indígenas do Brasil | colecaobei.com.br | 2025 | Q |
| 98 | Revista Prosa Verso e Arte | revistaprosaversoearte.com | 2021 | Q |
| 99 | Propagandas Históricas | propagandashistoricas.com.br | 2018 | Q |
| 100 | Minicontos | minicontos.com.br | 2025 | Q |

## 4. Nível B — públicas, mas bloqueiam alguns robôs de IA

Todas são gratuitas e sem login para pessoas. Algumas ferramentas de IA, porém, são bloqueadas. **Último recurso:** tente primeiro a alternativa do Nível A indicada na tabela. Só use uma fonte daqui se o Nível A falhar naquela posição e se a página abrir de verdade na sessão. Se não abrir, descarte na hora, sem nova tentativa.

| Fonte | Domínio | Anos no Enem | Uso | Alternativa no Nível A |
|---|---|---|---|---|
| g1 | g1.globo.com | 2020–2025 | M, Q | Agência Brasil, CNN Brasil |
| BBC News Brasil | bbc.com/portuguese | 2017–2025 | M, Q | Agência Brasil, CartaCapital |
| IBGE – Agência de Notícias | agenciadenoticias.ibge.gov.br | 2022, 2023, 2025 | M | ibge.gov.br |
| Planalto (legislação federal) | planalto.gov.br | 2017, 2019, 2020, 2025 | M, Q | legis.senado.leg.br |
| Domínio Público (obras literárias) | dominiopublico.gov.br | 2017, 2020–2022, 2024, 2025 | Q | Escritas, sites oficiais de autores |
| Superinteressante | super.abril.com.br | 2017, 2019, 2020, 2022 | Q | Revista Pesquisa FAPESP, Ciência Hoje |
| Revista Galileu | revistagalileu.globo.com | 2023, 2024, 2025 | Q | SoCientífica, Revista Planeta |
| R7 | noticias.r7.com / estudio.r7.com | 2021, 2023, 2024 | M, Q | CNN Brasil |
| Veja | veja.abril.com.br | 2018, 2021 | Q | Correio Braziliense |
| DW Brasil | dw.com/pt-br | 2021 | Q | ONU Brasil |
| Opera Mundi | operamundi.uol.com.br | 2025 | Q | Outras Palavras |
| Le Monde Diplomatique Brasil | diplomatique.org.br | 2023, 2024, 2025 | Q | Outras Palavras |
| Mangueira (G.R.E.S.) | mangueira.com.br | 2024 | M | Revista Bula |
| ACNUR Brasil | acnur.org/br | 2019 | Q | ONU Brasil |
| Jornal Opção | jornalopcao.com.br | 2021 | Q | O Popular |
| Sul21 | sul21.com.br | 2018 | Q | Tribuna PR |
| Insper | insper.edu.br | 2023 | Q | Jornal da USP |
| UOL (Notícias, TAB) | noticias.uol.com.br | 2020, 2022, 2024, 2025 | Q | CNN Brasil |
| Secretaria da Educação de SP | educacao.sp.gov.br | 2023 | Q | gov.br/mec |
| Biblioteca Nacional | bn.gov.br | 2019, 2021 | Q | Museu Nacional, FGV CPDOC |

## 5. Excluídas (e por quê)

| Fonte | Motivo |
|---|---|
| Folha de S.Paulo, Estadão, O Globo/Época, Valor Investe, Piauí | Paywall de matérias **e** bloqueio a robôs de IA |
| Nexo Jornal | Conteúdo carregado só por JavaScript e paywall: o robô não lê o texto |
| El País Brasil | Edição brasileira encerrada; o domínio redireciona para outra edição |
| humorpolitico.com.br | Domínio passou a ser uma loja virtual |
| reporterunesp.jor.br, cartanaescola.com.br | Domínios reaproveitados por sites sem relação com a fonte original |
| pebmed.com.br | Redireciona para portal comercial |
| Defensoria Pública de MT, Bienal de SP | Certificado de segurança inválido no domínio citado |
| direitoshumanos.usp.br, cartamaior.com.br | Domínio não existe mais (DNS) |
| bdjur.stj.jus.br, normas.leg.br | Página sem texto legível para robôs |
| Redes sociais (Facebook, Flickr, Instagram, Medium) | Autoria e data não verificáveis de forma estável |
| Sites comerciais (Zenklub, Imaterial, Foursquare, lojas) | Interesse comercial; não são fontes de referência |
| Veículos estrangeiros sem recorte brasileiro (NYT, Washington Post, Guardian, etc.) | Temas da skill são sempre no contexto brasileiro; muitos com paywall |
