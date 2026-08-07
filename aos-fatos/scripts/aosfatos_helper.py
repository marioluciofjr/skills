"""
aosfatos_helper.py — Lógica local de apoio para a skill "aos-fatos".

IMPORTANTE: este script NUNCA faz requisição de rede. Ele só monta URLs e
deduplica listas de itens já coletados pelo agente (que deve usar sua própria
ferramenta de fetch nativa, como WebFetch, para buscar aosfatos.org). Isso
mantém o script portável entre harnesses (Claude Code, Antigravity, Opencode)
que podem restringir rede a partir de scripts locais.

Uso (os filtros de montar-url são combináveis — informe um ou mais):
    python aosfatos_helper.py montar-url --selo falso
    python aosfatos_helper.py montar-url --formato tempo-real
    python aosfatos_helper.py montar-url --formato tempo-real --ano 2025
    python aosfatos_helper.py montar-url --ano 2026 --selo outro
    python aosfatos_helper.py montar-url --canal eleicoes-2026 --ano 2025
    python aosfatos_helper.py montar-url --q "vacina causa autismo" --formato checagem
    python aosfatos_helper.py deduplicar --arquivo itens.json --limite 12
    python aosfatos_helper.py preparar-itens --arquivo itens-brutos.json --limite 12

Saída: sempre JSON. Em caso de erro de validação, imprime {"erro": "..."} e
encerra com código de saída 1.
"""

import argparse
import json
import sys
from datetime import date
from urllib.parse import quote_plus


class ErroDeValidacao(Exception):
    """Erro de negócio (filtro inválido, JSON inválido etc.), nunca um erro técnico inesperado."""


class ConstrutorDeUrl:
    """
    Responsabilidade única: transformar filtros já validados em uma URL de
    busca de `https://www.aosfatos.org/noticias/`. Não conhece argparse, JSON
    ou I/O — só sabe montar URL a partir de valores primitivos.
    """

    BASE_URL = "https://www.aosfatos.org/noticias/"

    # Mapeamento de selo (label em PT-BR já resolvido pelo agente -> valor canônico)
    SELOS_VALIDOS = {"verdadeiro", "falso", "outro"}

    # Slugs de canal confirmados pelo usuário (ver references/mapa_urls.md)
    CANAIS_VALIDOS = {
        "boataria-politica",
        "pseudociencia",
        "negacionismo-climatico",
        "inteligencia-artificial",
        "fraudes-digitais",
        "tecnopolitica",
        "autoritarismo",
        "discurso-de-odio",
        "impacto",
        "eleicoes-2026",
    }

    # Formatos de conteúdo aceitos pelo site (sub-pergunta nos ramos ano/canal/q)
    FORMATOS_VALIDOS = {
        "checagem",
        "tempo-real",
        "explicador",
        "reportagem",
        "radar",
        "hq",
        "analise",
        "nota",
        "institucional",
    }

    # Ano mínimo suportado pelo portal (fixo — confirmado pelo usuário, não muda com o tempo)
    ANO_MINIMO = 2021

    def _ano_maximo(self) -> int:
        """
        Teto de ano aceito = ano corrente do sistema. Calculado a cada chamada
        (não é uma constante fixa) para a skill se manter válida sozinha ano
        após ano, sem precisar de edição manual quando o calendário virar.
        """
        return date.today().year

    def construir(
        self,
        selo: str | None = None,
        formato: str | None = None,
        ano: int | None = None,
        canal: str | None = None,
        q: str | None = None,
    ) -> str:
        """
        Monta a URL final a partir de QUALQUER combinação de filtros (selo,
        formato, ano, canal, q) — o site aceita todos simultaneamente, ex:
        `?formato=checagem&ano=2026&page=1&selo=outro`. É preciso informar
        pelo menos um filtro. `page=1` é sempre fixo — esta skill nunca
        pagina além da primeira página.
        """
        self._validar_pelo_menos_um_filtro(selo, formato, ano, canal, q)

        partes = []
        partes.extend(self._parte_formato(selo, formato))
        if selo is not None:
            partes.extend(self._parte_selo(selo))
        if ano is not None:
            partes.extend(self._parte_ano(ano))
        if canal is not None:
            partes.extend(self._parte_canal(canal))
        if q is not None:
            partes.extend(self._parte_palavra_chave(q))

        # page=1 é sempre o último parâmetro, nunca sobrescrevível
        partes.append("page=1")
        return f"{self.BASE_URL}?{'&'.join(partes)}"

    def _validar_pelo_menos_um_filtro(self, selo, formato, ano, canal, q) -> None:
        if all(f is None for f in (selo, formato, ano, canal, q)):
            raise ErroDeValidacao("Informe ao menos um filtro: --selo, --formato, --ano, --canal ou --q.")

    def _parte_formato(self, selo: str | None, formato: str | None) -> list[str]:
        # Selo sempre implica formato=checagem, independente do formato passado
        # (selos só existem para checagens no Aos Fatos).
        if selo is not None:
            return ["formato=checagem"]
        if formato is not None:
            if formato not in self.FORMATOS_VALIDOS:
                raise ErroDeValidacao(f"Formato inválido: '{formato}'. Valores aceitos: {sorted(self.FORMATOS_VALIDOS)}.")
            return [f"formato={formato}"]
        return []

    def _parte_selo(self, selo: str) -> list[str]:
        if selo not in self.SELOS_VALIDOS:
            raise ErroDeValidacao(f"Selo inválido: '{selo}'. Valores aceitos: {sorted(self.SELOS_VALIDOS)}.")
        return [f"selo={selo}"]

    def _parte_ano(self, ano: int) -> list[str]:
        ano_maximo = self._ano_maximo()
        if not (self.ANO_MINIMO <= ano <= ano_maximo):
            raise ErroDeValidacao(f"Ano inválido: {ano}. Aceito apenas entre {self.ANO_MINIMO} e {ano_maximo}.")
        return [f"ano={ano}"]

    def _parte_canal(self, canal: str) -> list[str]:
        if canal not in self.CANAIS_VALIDOS:
            raise ErroDeValidacao(f"Canal inválido: '{canal}'. Valores aceitos: {sorted(self.CANAIS_VALIDOS)}.")
        return [f"canal={canal}"]

    def _parte_palavra_chave(self, q: str) -> list[str]:
        return [f"q={quote_plus(q)}"]


class DeduplicadorDeItens:
    """
    Responsabilidade única: remover itens duplicados de uma lista de
    resultados (título/URL), preservando a ordem de descoberta. Não conhece
    URLs de busca nem argparse — só opera sobre a lista que recebe.
    """

    def deduplicar(self, itens: list[dict], limite: int) -> list[dict]:
        vistos: set[str] = set()
        resultado: list[dict] = []
        for item in itens:
            url_normalizada = self._normalizar_url(item.get("url", ""))
            if not url_normalizada or url_normalizada in vistos:
                continue
            vistos.add(url_normalizada)
            resultado.append(item)
            if len(resultado) >= limite:
                break
        return resultado

    def _normalizar_url(self, url: str) -> str:
        return url.strip().rstrip("/")


class ValidadorDeItens:
    """
    Responsabilidade única: descartar itens sem título, sem URL, ou cuja URL
    não pertence de fato ao domínio aosfatos.org. Reforça no código o mesmo
    guardrail de domínio travado que o SKILL.md exige em prosa — não confia
    apenas na instrução textual. Não conhece deduplicação nem argparse.
    """

    DOMINIOS_VALIDOS = ("https://www.aosfatos.org", "https://aosfatos.org")

    def filtrar(self, itens: list[dict]) -> list[dict]:
        validos = []
        for item in itens:
            titulo = (item.get("titulo") or "").strip()
            url = (item.get("url") or "").strip()
            if titulo and url and url.startswith(self.DOMINIOS_VALIDOS):
                validos.append({"titulo": titulo, "url": url})
        return validos


class AosFatosCLI:
    """
    Orquestra a linha de comando: interpreta argumentos e delega a
    construção de URL e a deduplicação para as classes especializadas acima.
    Não contém regra de negócio própria — só faz a ponte entre I/O e as
    classes de domínio, mantendo baixo acoplamento entre elas.
    """

    def __init__(self) -> None:
        self._construtor_url = ConstrutorDeUrl()
        self._deduplicador = DeduplicadorDeItens()
        self._validador = ValidadorDeItens()

    def executar(self, argumentos: list[str] | None = None) -> None:
        args = self._parser().parse_args(argumentos)
        try:
            if args.comando == "montar-url":
                self._executar_montar_url(args)
            elif args.comando == "deduplicar":
                self._executar_deduplicar(args)
            elif args.comando == "preparar-itens":
                self._executar_preparar_itens(args)
        except ErroDeValidacao as erro:
            self._imprimir_erro(str(erro))

    def _executar_montar_url(self, args: argparse.Namespace) -> None:
        url = self._construtor_url.construir(
            selo=args.selo,
            formato=args.formato,
            ano=args.ano,
            canal=args.canal,
            q=args.q,
        )
        print(json.dumps({"url": url}, ensure_ascii=False))

    def _executar_deduplicar(self, args: argparse.Namespace) -> None:
        itens = self._ler_itens_json(args.arquivo)
        resultado = self._deduplicador.deduplicar(itens, args.limite)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))

    def _executar_preparar_itens(self, args: argparse.Namespace) -> None:
        itens = self._ler_itens_json(args.arquivo)
        itens_validos = self._validador.filtrar(itens)
        resultado = self._deduplicador.deduplicar(itens_validos, args.limite)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))

    def _ler_itens_json(self, caminho_arquivo: str | None) -> list[dict]:
        conteudo = open(caminho_arquivo, "r", encoding="utf-8").read() if caminho_arquivo else sys.stdin.read()
        try:
            return json.loads(conteudo)
        except json.JSONDecodeError:
            raise ErroDeValidacao("JSON de entrada inválido — esperada uma lista de itens {'titulo': ..., 'url': ...}.")

    def _imprimir_erro(self, mensagem: str) -> None:
        print(json.dumps({"erro": mensagem}, ensure_ascii=False))
        sys.exit(1)

    def _parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description="Lógica local de apoio para a skill aos-fatos")
        subparsers = parser.add_subparsers(dest="comando", required=True)

        p_url = subparsers.add_parser("montar-url", help="Monta a URL de busca em aosfatos.org")
        p_url.add_argument("--selo", choices=sorted(ConstrutorDeUrl.SELOS_VALIDOS), default=None)
        p_url.add_argument("--ano", type=int, default=None)
        p_url.add_argument("--canal", choices=sorted(ConstrutorDeUrl.CANAIS_VALIDOS), default=None)
        p_url.add_argument("--q", type=str, default=None)
        p_url.add_argument("--formato", choices=sorted(ConstrutorDeUrl.FORMATOS_VALIDOS), default=None)

        p_dedup = subparsers.add_parser("deduplicar", help="Remove itens duplicados por URL")
        p_dedup.add_argument("--arquivo", type=str, default=None, help="Caminho de um JSON de itens (padrão: stdin)")
        p_dedup.add_argument("--limite", type=int, default=12)

        p_prep = subparsers.add_parser(
            "preparar-itens",
            help="Valida (domínio aosfatos.org + campos obrigatórios) e deduplica uma lista de itens em um só passo",
        )
        p_prep.add_argument("--arquivo", type=str, default=None, help="Caminho de um JSON de itens (padrão: stdin)")
        p_prep.add_argument("--limite", type=int, default=12)

        return parser


if __name__ == "__main__":
    AosFatosCLI().executar()
