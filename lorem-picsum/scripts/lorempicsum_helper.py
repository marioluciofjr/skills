"""
lorempicsum_helper.py

Ferramenta de apoio da skill lorem-picsum: monta URLs do serviço
picsum.photos seguindo as regras oficiais (refs/tutorial-lorem-picsum.md).

Este script NUNCA acessa a rede — os 3 subcomandos só constroem URLs,
sem nenhuma chamada HTTP:
    imagem  -> gera um ou mais links de imagem prontos para uso (aleatória,
               por id ou por seed). O Picsum é um serviço público, sem
               autenticação, com regras de URL fixas e documentadas, então
               uma URL bem formada funciona por construção.
    lista   -> monta a URL paginada do acervo (/v2/list) e devolve uma
               instrução para o agente buscá-la com sua própria ferramenta
               de fetch nativa (ex: WebFetch).
    info    -> monta a URL de detalhes técnicos de uma imagem (/info) e
               devolve a mesma instrução de busca.

Esse desenho (script só monta URL, agente busca com sua ferramenta nativa)
segue o mesmo padrão já usado pela skill `aos-fatos` deste projeto, e existe
por dois motivos históricos: (1) ambientes com egress restrito, como o
Claude Chat, bloqueiam chamadas de rede feitas pelo script para domínios
fora de sua lista de permissão, mesmo quando a URL em si está correta;
(2) harnesses como o Gemini Spark simplesmente não aceitam scripts que
façam qualquer acesso à internet, então um script 100% livre de rede é
o único jeito da skill funcionar em todos os harnesses do projeto.
"""

import argparse
import json
import sys
import urllib.parse

# O console do Windows não usa UTF-8 por padrão, o que corrompe nomes de
# autores com acento (ex: "André") na saída. Força UTF-8 na saída padrão.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


BASE_URL = "https://picsum.photos"

QUANTIDADE_PADRAO = 3
QUANTIDADE_MAXIMA = 30

TAMANHO_PADRAO = 1024
TAMANHO_MINIMO = 1
TAMANHO_MAXIMO = 4000  # limite próprio da skill (bom-senso), não é uma regra oficial do Picsum

BLUR_MINIMO = 1
BLUR_MAXIMO = 10
EXTENSOES_VALIDAS = {"jpg", "webp"}

LIMITE_LISTA_PADRAO = 30  # default oficial do endpoint /v2/list
LIMITE_LISTA_MAXIMO = 100  # limite próprio da skill (bom-senso), não é uma regra oficial do Picsum


class ErroDeValidacao(Exception):
    """Parâmetro inválido ou combinação proibida."""


class ConstrutorDeUrlImagem:
    """Responsabilidade única: transformar parâmetros já validados em uma lista de
    URLs de imagem, sem nunca tocar rede."""

    def resolver_quantidade(self, quantidade, id_imagem, seed):
        """Se a pessoa usuária não informou quantidade, aplica o padrão — mas o
        padrão é 1 quando id/seed foi informado, pois eles identificam uma única
        imagem determinística (pedir "3 imagens" com um id fixo não faz sentido)."""
        if quantidade is None:
            return 1 if (id_imagem is not None or seed is not None) else QUANTIDADE_PADRAO
        return quantidade

    def construir(self, largura, altura, quantidade, id_imagem, seed, grayscale, blur, blur_nivel, extensao):
        self._validar_id_e_seed_mutuamente_exclusivos(id_imagem, seed)
        self._validar_quantidade(quantidade, id_imagem, seed)
        self._validar_blur(blur, blur_nivel)
        self._validar_extensao(extensao)
        largura, altura = self._resolver_dimensoes(largura, altura)
        blur = blur or blur_nivel is not None

        # ?random=n só se aplica ao modo aleatório puro: id/seed já são determinísticos,
        # então não há cache de navegador a evitar.
        usa_random = quantidade > 1 and id_imagem is None and seed is None

        itens = []
        for indice in range(1, quantidade + 1):
            indice_random = indice if usa_random else None
            itens.append(self._montar_item(largura, altura, id_imagem, seed, grayscale, blur, blur_nivel, extensao, indice_random))
        return itens

    def _montar_item(self, largura, altura, id_imagem, seed, grayscale, blur, blur_nivel, extensao, indice_random):
        caminho = self._montar_caminho_base(largura, altura, id_imagem, seed)
        caminho += self._montar_extensao(extensao)
        url = caminho + self._montar_query_string(grayscale, blur, blur_nivel, indice_random)
        return {
            "url": url,
            "parametros": {
                "largura": largura,
                "altura": altura,
                "id": id_imagem,
                "seed": seed,
                "grayscale": grayscale,
                "blur": blur,
                "blur_nivel": blur_nivel,
                "extensao": extensao,
                "random": indice_random,
            },
        }

    def _resolver_dimensoes(self, largura, altura):
        if largura is None and altura is None:
            largura = altura = TAMANHO_PADRAO
        elif largura is None:
            largura = altura
        elif altura is None:
            altura = largura
        for nome, valor in (("largura", largura), ("altura", altura)):
            if not (TAMANHO_MINIMO <= valor <= TAMANHO_MAXIMO):
                raise ErroDeValidacao(
                    f"O parâmetro '{nome}' deve estar entre {TAMANHO_MINIMO} e {TAMANHO_MAXIMO} pixels (recebido: {valor})."
                )
        return largura, altura

    def _validar_id_e_seed_mutuamente_exclusivos(self, id_imagem, seed):
        if id_imagem is not None and seed is not None:
            raise ErroDeValidacao("Os parâmetros 'id' e 'seed' são mutuamente exclusivos — use apenas um deles.")

    def _validar_quantidade(self, quantidade, id_imagem, seed):
        if not (1 <= quantidade <= QUANTIDADE_MAXIMA):
            raise ErroDeValidacao(f"A quantidade deve estar entre 1 e {QUANTIDADE_MAXIMA} (recebido: {quantidade}).")
        if (id_imagem is not None or seed is not None) and quantidade != 1:
            raise ErroDeValidacao(
                "Quando 'id' ou 'seed' é informado, a quantidade deve ser exatamente 1, "
                "pois eles identificam uma única imagem determinística."
            )

    def _validar_blur(self, blur, blur_nivel):
        if blur_nivel is not None and not (BLUR_MINIMO <= blur_nivel <= BLUR_MAXIMO):
            raise ErroDeValidacao(f"O nível de blur deve estar entre {BLUR_MINIMO} e {BLUR_MAXIMO} (recebido: {blur_nivel}).")

    def _validar_extensao(self, extensao):
        if extensao is not None and extensao not in EXTENSOES_VALIDAS:
            raise ErroDeValidacao(f"Extensão inválida: '{extensao}'. Use uma de: {', '.join(sorted(EXTENSOES_VALIDAS))}.")

    def _montar_caminho_base(self, largura, altura, id_imagem, seed):
        if id_imagem is not None:
            return f"{BASE_URL}/id/{id_imagem}/{largura}/{altura}"
        if seed is not None:
            # urllib.parse.quote protege contra seeds com espaço/acento e contra
            # injeção de caracteres especiais na URL.
            seed_codificada = urllib.parse.quote(str(seed), safe="")
            return f"{BASE_URL}/seed/{seed_codificada}/{largura}/{altura}"
        return f"{BASE_URL}/{largura}/{altura}"

    def _montar_extensao(self, extensao):
        return f".{extensao}" if extensao else ""

    def _montar_query_string(self, grayscale, blur, blur_nivel, indice_random):
        partes = []
        if grayscale:
            partes.append("grayscale")
        if blur:
            partes.append(f"blur={blur_nivel}" if blur_nivel else "blur")
        if indice_random is not None:
            partes.append(f"random={indice_random}")
        return f"?{'&'.join(partes)}" if partes else ""


class ConstrutorDeUrlLista:
    """Responsabilidade única: montar a URL paginada de listagem do acervo (/v2/list)."""

    def construir(self, pagina, limite):
        if pagina < 1:
            raise ErroDeValidacao(f"A página deve ser maior ou igual a 1 (recebido: {pagina}).")
        if not (1 <= limite <= LIMITE_LISTA_MAXIMO):
            raise ErroDeValidacao(f"O limite deve estar entre 1 e {LIMITE_LISTA_MAXIMO} (recebido: {limite}).")
        return f"{BASE_URL}/v2/list?page={pagina}&limit={limite}"


class ConstrutorDeUrlInfo:
    """Responsabilidade única: montar a URL de detalhes técnicos de uma imagem (/info)."""

    def construir(self, id_imagem, seed):
        if id_imagem is not None and seed is not None:
            raise ErroDeValidacao("Os parâmetros 'id' e 'seed' são mutuamente exclusivos — use apenas um deles.")
        if id_imagem is None and seed is None:
            raise ErroDeValidacao("Informe 'id' ou 'seed' para consultar os detalhes de uma imagem.")
        if id_imagem is not None:
            return f"{BASE_URL}/id/{id_imagem}/info"
        seed_codificada = urllib.parse.quote(str(seed), safe="")
        return f"{BASE_URL}/seed/{seed_codificada}/info"


INSTRUCAO_BUSCA = (
    "Busque esta URL com sua ferramenta de fetch nativa (ex: WebFetch) — este "
    "script nunca acessa a rede, só monta a URL."
)


class BuscadorDeLista:
    """Responsabilidade única: montar a URL de /v2/list e empacotar a instrução
    de busca para o agente. Nunca toca rede — mesmo padrão da skill aos-fatos."""

    def __init__(self, construtor):
        self._construtor = construtor

    def montar_pedido(self, pagina, limite):
        url = self._construtor.construir(pagina, limite)
        return {
            "url_a_buscar": url,
            "pagina": pagina,
            "limite": limite,
            "instrucao": INSTRUCAO_BUSCA,
        }


class BuscadorDeInfo:
    """Responsabilidade única: montar a URL de /info e empacotar a instrução
    de busca para o agente. Nunca toca rede — mesmo padrão da skill aos-fatos."""

    def __init__(self, construtor):
        self._construtor = construtor

    def montar_pedido(self, id_imagem, seed):
        url = self._construtor.construir(id_imagem, seed)
        return {
            "url_a_buscar": url,
            "instrucao": INSTRUCAO_BUSCA,
        }


class LoremPicsumCLI:
    """Orquestra a linha de comando: interpreta os argumentos e delega para as
    classes de domínio, sempre imprimindo JSON na saída padrão."""

    def __init__(self):
        self._construtor_imagem = ConstrutorDeUrlImagem()
        self._buscador_lista = BuscadorDeLista(ConstrutorDeUrlLista())
        self._buscador_info = BuscadorDeInfo(ConstrutorDeUrlInfo())

    def executar(self, argumentos=None):
        parser = self._parser()
        args = parser.parse_args(argumentos)
        try:
            if args.comando == "imagem":
                self._executar_imagem(args)
            elif args.comando == "lista":
                self._executar_lista(args)
            elif args.comando == "info":
                self._executar_info(args)
            else:
                parser.print_help()
                sys.exit(1)
        except ErroDeValidacao as erro:
            print(json.dumps({"erro": str(erro)}, ensure_ascii=False))
            sys.exit(1)

    def _executar_imagem(self, args):
        quantidade = self._construtor_imagem.resolver_quantidade(args.quantidade, args.id, args.seed)
        itens = self._construtor_imagem.construir(
            largura=args.largura,
            altura=args.altura,
            quantidade=quantidade,
            id_imagem=args.id,
            seed=args.seed,
            grayscale=args.grayscale,
            blur=args.blur,
            blur_nivel=args.blur_nivel,
            extensao=args.extensao,
        )
        resultado = {
            "quantidade_solicitada": quantidade,
            "imagens": itens,
        }
        print(json.dumps(resultado, ensure_ascii=False, indent=2))

    def _executar_lista(self, args):
        resultado = self._buscador_lista.montar_pedido(args.pagina, args.limite)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))

    def _executar_info(self, args):
        resultado = self._buscador_info.montar_pedido(args.id, args.seed)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))

    def _parser(self):
        parser = argparse.ArgumentParser(
            prog="lorempicsum_helper.py",
            description="Monta links de imagens do serviço Lorem Picsum (picsum.photos) e consulta seu acervo.",
        )
        subparsers = parser.add_subparsers(dest="comando")

        imagem = subparsers.add_parser("imagem", help="Gera um ou mais links de imagem.")
        imagem.add_argument("--largura", type=int, default=None)
        imagem.add_argument("--altura", type=int, default=None)
        imagem.add_argument("--quantidade", type=int, default=None)
        imagem.add_argument("--id", type=int, default=None)
        imagem.add_argument("--seed", type=str, default=None)
        imagem.add_argument("--grayscale", action="store_true")
        imagem.add_argument("--blur", action="store_true")
        imagem.add_argument("--blur-nivel", type=int, default=None)
        imagem.add_argument("--extensao", type=str, default=None, choices=sorted(EXTENSOES_VALIDAS))

        lista = subparsers.add_parser("lista", help="Monta a URL da lista paginada do acervo.")
        lista.add_argument("--pagina", type=int, default=1)
        lista.add_argument("--limite", type=int, default=LIMITE_LISTA_PADRAO)

        info = subparsers.add_parser("info", help="Monta a URL de detalhes técnicos de uma imagem.")
        info.add_argument("--id", type=int, default=None)
        info.add_argument("--seed", type=str, default=None)

        return parser


if __name__ == "__main__":
    LoremPicsumCLI().executar()
