"""Extrair a mídia (ppt/media) de apresentações PowerPoint e do Google Slides.

Uso:
  python extrair_media.py triagem <link | arquivo.gslides>
  python extrair_media.py slides <link | arquivo.gslides> --destino <pasta-nova> [--zip]
  python extrair_media.py extrair <apresentacao.pptx> --destino <pasta-nova> [--zip]
  python extrair_media.py link <link | arquivo.gslides>

Códigos de saída: 0 sucesso; 1 erro geral; 3 link restrito (o Google pediu login);
4 sem conexão com o Google a partir deste ambiente.

Só usa a biblioteca padrão do Python 3, para rodar em qualquer sistema sem instalar nada.
"""
import argparse
import hashlib
import json
import re
import shutil
import stat
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from dataclasses import asdict, dataclass, field
from pathlib import Path, PurePosixPath
from urllib.parse import parse_qs, urlparse


# ---------------------------------------------------------------------------
# Google Slides: descobrir o ID da apresentação
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ReferenciaGoogleSlides:
    """Dados de uma apresentação do Google Slides prontos para o agente usar."""

    id: str
    url_edicao: str
    url_exportacao_pptx: str


class LeitorAtalhoGslides:
    """Lê um atalho .gslides ou uma URL e devolve o ID da apresentação.

    Um arquivo .gslides não guarda os slides: é só um atalho em JSON que aponta para o
    documento na nuvem. Esta classe apenas LÊ o texto do atalho; nada é executado e
    nenhuma conexão de rede é aberta.
    """

    TAMANHO_MAXIMO_ATALHO = 1024 * 1024  # um atalho legítimo tem poucos bytes
    PADRAO_ID = re.compile(r'^[A-Za-z0-9_-]{20,}$')
    PADRAO_URL = re.compile(r'/presentation/d/([A-Za-z0-9_-]{20,})')

    def identificar(self, entrada):
        """Aceita o caminho de um .gslides, uma URL do Google ou o próprio ID."""
        caminho = Path(entrada).expanduser()
        if caminho.suffix.lower() == '.gslides' and caminho.is_file():
            identificador = self._ler_atalho(caminho)
        else:
            identificador = self._extrair_de_texto(str(entrada).strip())
        return self._montar_referencia(identificador)

    def _ler_atalho(self, caminho):
        if caminho.stat().st_size > self.TAMANHO_MAXIMO_ATALHO:
            raise ValueError('Atalho .gslides grande demais para ser um atalho legítimo.')
        try:
            dados = json.loads(caminho.read_text(encoding='utf-8-sig'))
        except (UnicodeDecodeError, json.JSONDecodeError) as erro:
            raise ValueError('O .gslides não contém o JSON esperado de um atalho do Drive.') from erro
        if not isinstance(dados, dict):
            raise ValueError('O .gslides não contém o JSON esperado de um atalho do Drive.')
        # O Drive costuma gravar "doc_id"; versões antigas usam "resource_id" ou só "url".
        candidatos = [
            dados.get('doc_id'),
            str(dados.get('resource_id', '')).split(':')[-1],
            dados.get('url'),
        ]
        for candidato in candidatos:
            if candidato:
                try:
                    return self._extrair_de_texto(str(candidato))
                except ValueError:
                    continue
        raise ValueError('Não encontrei o ID da apresentação dentro do atalho .gslides.')

    def _extrair_de_texto(self, texto):
        if self.PADRAO_ID.match(texto):
            return texto
        encontrado = self.PADRAO_URL.search(texto)
        if encontrado:
            return encontrado.group(1)
        # Formato https://docs.google.com/open?id=<ID>
        parametros = parse_qs(urlparse(texto).query)
        for valor in parametros.get('id', []):
            if self.PADRAO_ID.match(valor):
                return valor
        raise ValueError('Não reconheci um link ou ID válido do Google Slides.')

    @staticmethod
    def _montar_referencia(identificador):
        base = f'https://docs.google.com/presentation/d/{identificador}'
        return ReferenciaGoogleSlides(
            id=identificador,
            url_edicao=f'{base}/edit',
            url_exportacao_pptx=f'{base}/export/pptx',
        )


# ---------------------------------------------------------------------------
# Google Slides: baixar o .pptx pelo endpoint de exportação
# ---------------------------------------------------------------------------

class AcessoRestritoError(Exception):
    """O Google pediu login: o link não está liberado para quem não tem permissão."""


class SemConexaoError(Exception):
    """Este ambiente não conseguiu falar com o Google (sem internet ou domínio bloqueado)."""


class PoliticaDominiosGoogle:
    """Diz para quais endereços o download pode ir.

    A exportação começa em docs.google.com e costuma redirecionar para um servidor
    *.googleusercontent.com. Qualquer outro destino é recusado, para o script nunca ser
    usado para buscar endereços arbitrários.
    """

    HOSTS_EXATOS = {'docs.google.com'}
    SUFIXOS = ('.googleusercontent.com',)
    HOSTS_DE_LOGIN = {'accounts.google.com'}

    def conferir(self, url):
        host = (urlparse(url).hostname or '').lower()
        if host in self.HOSTS_DE_LOGIN:
            raise AcessoRestritoError('O Google pediu login: o link está restrito.')
        if host not in self.HOSTS_EXATOS and not host.endswith(self.SUFIXOS):
            raise ValueError(f'Redirecionamento inesperado para {host}; download interrompido.')


class RedirecionamentoSeguro(urllib.request.HTTPRedirectHandler):
    """Segue redirecionamentos só depois de a política de domínios aprovar o destino.

    A assinatura do método é a da biblioteca padrão (urllib), por isso tem tantos parâmetros.
    """

    def __init__(self, politica):
        super().__init__()
        self.politica = politica

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.politica.conferir(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class BaixadorExportacao:
    """Baixa o .pptx pelo endpoint /export/pptx, o mesmo do menu Arquivo > Fazer download.

    Diferente da exportação pela API do Google Drive (usada pelos conectores), este
    endpoint não tem o limite de 10 MB. Sem login, porém, ele só funciona quando a
    apresentação está como "Qualquer pessoa com o link".
    """

    ASSINATURA_ZIP = b'PK\x03\x04'  # todo .pptx começa com estes bytes
    MAX_BYTES = 4 * 1024**3
    BLOCO = 1024 * 1024
    TEMPO_LIMITE = 120
    CABECALHOS = {'User-Agent': 'Mozilla/5.0 (skill extrair-imagens)'}
    # Os servidores do Google se identificam no cabeçalho "Server". Um erro HTTP sem essa
    # assinatura veio de um intermediário (proxy ou firewall do ambiente), não do Google.
    SERVIDORES_GOOGLE = ('esf', 'gse', 'gws', 'sffe', 'uploadserver')

    def __init__(self, politica=None):
        self.politica = politica or PoliticaDominiosGoogle()
        self._abridor = urllib.request.build_opener(RedirecionamentoSeguro(self.politica))

    def sondar(self, referencia):
        """Lê só os primeiros bytes da exportação. Levanta erro se não houver acesso."""
        with self._abrir(referencia.url_exportacao_pptx) as resposta:
            self._conferir_inicio(resposta.read(len(self.ASSINATURA_ZIP)))

    def baixar(self, referencia, arquivo):
        """Grava o .pptx em 'arquivo' (que não pode existir) e devolve o caminho."""
        total = 0
        with self._abrir(referencia.url_exportacao_pptx) as resposta, arquivo.open('xb') as saida:
            inicio = resposta.read(len(self.ASSINATURA_ZIP))
            self._conferir_inicio(inicio)
            saida.write(inicio)
            total += len(inicio)
            for bloco in iter(lambda: resposta.read(self.BLOCO), b''):
                total += len(bloco)
                if total > self.MAX_BYTES:
                    raise ValueError('Download maior que 4 GiB; interrompido.')
                saida.write(bloco)
        return arquivo

    def _abrir(self, url):
        self.politica.conferir(url)
        requisicao = urllib.request.Request(url, headers=self.CABECALHOS)
        try:
            return self._abridor.open(requisicao, timeout=self.TEMPO_LIMITE)
        except urllib.error.HTTPError as erro:
            if not self._veio_do_google(erro.headers):
                raise SemConexaoError(f'A rede deste ambiente bloqueou o acesso ao Google (HTTP {erro.code}).') from erro
            if erro.code in (401, 403):
                raise AcessoRestritoError(f'O Google pediu login (HTTP {erro.code}): o link está restrito.') from erro
            if erro.code == 404:
                raise ValueError('Apresentação não encontrada (HTTP 404). Confira o link.') from erro
            raise ValueError(f'O Google respondeu com erro HTTP {erro.code}.') from erro
        except urllib.error.URLError as erro:
            raise SemConexaoError(f'Sem conexão com o Google a partir deste ambiente: {erro.reason}') from erro
        except (TimeoutError, ConnectionError) as erro:
            raise SemConexaoError(f'Sem conexão com o Google a partir deste ambiente: {erro}') from erro

    def _veio_do_google(self, cabecalhos):
        servidor = (cabecalhos.get('Server', '') if cabecalhos else '').lower()
        return servidor.startswith(self.SERVIDORES_GOOGLE)

    def _conferir_inicio(self, inicio):
        # Uma página de login ou de aviso chega como HTML, não como pacote .pptx.
        if not inicio.startswith(self.ASSINATURA_ZIP):
            raise AcessoRestritoError('O Google devolveu uma página em vez do .pptx: o link está restrito.')


@dataclass
class ResultadoTriagem:
    """Categoria do ambiente e próximo passo que o agente deve seguir."""

    CONSEGUE = 'consegue_endpoint'
    NAO_CONSEGUE = 'nao_consegue_endpoint'

    id: str
    categoria: str
    link_liberado: bool = None
    proximo_passo: str = ''
    detalhe: str = ''


class TriagemAmbiente:
    """Classifica o ambiente em 'consegue pelo endpoint' ou 'não consegue pelo endpoint'.

    A sonda pede só os primeiros bytes da exportação:
    - chegou o início do .pptx: consegue, e o link está liberado;
    - o próprio Google recusou: consegue (a rede funciona), mas o link está restrito;
    - não houve conversa com o Google (sem internet, domínio bloqueado): não consegue.
    """

    def __init__(self, baixador):
        self.baixador = baixador

    def classificar(self, referencia):
        try:
            self.baixador.sondar(referencia)
        except AcessoRestritoError as erro:
            return ResultadoTriagem(
                id=referencia.id, categoria=ResultadoTriagem.CONSEGUE, link_liberado=False,
                proximo_passo='Peça para liberar o link como "Qualquer pessoa com o link" e "Leitor" '
                              '(ou enviar o .pptx) e rode a triagem de novo.',
                detalhe=str(erro))
        except SemConexaoError as erro:
            return ResultadoTriagem(
                id=referencia.id, categoria=ResultadoTriagem.NAO_CONSEGUE,
                proximo_passo='Peça agora o arquivo .pptx na conversa e use o subcomando extrair.',
                detalhe=str(erro))
        return ResultadoTriagem(
            id=referencia.id, categoria=ResultadoTriagem.CONSEGUE, link_liberado=True,
            proximo_passo='Rode o subcomando slides com o mesmo link.',
            detalhe='O link está liberado: o download funciona sem login.')


class FluxoGoogleSlides:
    """Junta as peças da rota do link: identificar, baixar e extrair."""

    def __init__(self, leitor, baixador, extrator):
        self.leitor = leitor
        self.baixador = baixador
        self.extrator = extrator

    def executar(self, entrada, destino, gerar_zip=False):
        referencia = self.leitor.identificar(entrada)
        destino = Path(destino).expanduser().resolve()
        if destino.exists():
            # Confere antes de baixar, para não gastar tempo com um download inútil.
            raise ValueError('O destino já existe. Escolha uma pasta nova para evitar sobrescritas.')
        # O .pptx baixado fica numa pasta temporária, apagada no fim: a pessoa recebe só a mídia.
        with tempfile.TemporaryDirectory(prefix='extrair-imagens-') as temporaria:
            arquivo = self.baixador.baixar(referencia, Path(temporaria) / 'apresentacao.pptx')
            return self.extrator.extrair(arquivo, destino, gerar_zip)


# ---------------------------------------------------------------------------
# Segurança dos nomes de arquivo dentro do pacote
# ---------------------------------------------------------------------------

class PoliticaNomeSeguro:
    """Aprova ou recusa cada caminho de mídia antes de gravar no disco.

    Protege contra "zip slip" (caminhos com ../ que escapam da pasta), links simbólicos,
    nomes proibidos no Windows e nomes repetidos que se sobrescreveriam.
    Use uma instância nova por extração, porque ela lembra os nomes já aprovados.
    """

    CARACTERES_PROIBIDOS = set('\\:<>"|?*')
    NOMES_RESERVADOS = {'CON', 'PRN', 'AUX', 'NUL'} | {
        f'{prefixo}{numero}' for prefixo in ('COM', 'LPT') for numero in range(1, 10)
    }

    def __init__(self):
        self._vistos = set()

    def aprovar(self, item, nome_relativo):
        """Devolve o caminho relativo seguro ou levanta ValueError."""
        partes = nome_relativo.split('/')
        relativo = PurePosixPath(nome_relativo)
        if not nome_relativo or relativo.is_absolute() or any(self._parte_invalida(p) for p in partes):
            raise ValueError(f'Caminho de mídia inseguro ou incompatível com Windows: {nome_relativo}')
        if any(p.split('.')[0].upper() in self.NOMES_RESERVADOS for p in partes):
            raise ValueError(f'Nome de mídia reservado pelo Windows: {nome_relativo}')
        if stat.S_ISLNK(item.external_attr >> 16):
            raise ValueError(f'Links simbólicos não são permitidos: {nome_relativo}')
        chave = nome_relativo.casefold()
        if chave in self._vistos:
            raise ValueError(f'Nomes duplicados ou conflitantes no pacote: {nome_relativo}')
        self._vistos.add(chave)
        return relativo

    def _parte_invalida(self, parte):
        return (
            parte in ('', '.', '..')
            or any(c in self.CARACTERES_PROIBIDOS for c in parte)
            or parte.endswith((' ', '.'))
            or any(ord(c) < 32 for c in parte)
        )


# ---------------------------------------------------------------------------
# Validação do arquivo PowerPoint e seleção da mídia
# ---------------------------------------------------------------------------

class ValidadorPacotePptx:
    """Confere se o arquivo é mesmo um PowerPoint e escolhe o que sai de ppt/media."""

    EXTENSOES_ACEITAS = {'.pptx', '.pptm', '.ppsx', '.potx'}
    ARQUIVOS_OBRIGATORIOS = {'[Content_Types].xml', 'ppt/presentation.xml'}
    PREFIXO_MIDIA = 'ppt/media/'
    MAX_ARQUIVOS = 20000
    MAX_BYTES = 4 * 1024**3

    def validar_arquivo(self, caminho):
        if caminho.suffix.lower() == '.gslides':
            raise ValueError('O .gslides é só um atalho: exporte a apresentação como .pptx primeiro.')
        if caminho.suffix.lower() not in self.EXTENSOES_ACEITAS:
            raise ValueError('Envie um arquivo .pptx (também aceitos: .pptm, .ppsx, .potx).')
        if not caminho.is_file():
            raise ValueError(f'Arquivo não encontrado: {caminho}')
        # Um download que falhou costuma ser uma página HTML salva com o nome .pptx.
        if not zipfile.is_zipfile(caminho):
            raise ValueError('O arquivo não é um PowerPoint válido (pode ser uma página de login ou de erro salva como .pptx).')

    def validar_estrutura(self, pacote):
        if not self.ARQUIVOS_OBRIGATORIOS.issubset(set(pacote.namelist())):
            raise ValueError('O arquivo não contém a estrutura esperada de um PowerPoint.')

    def selecionar_midias(self, pacote, politica):
        """Lista (item do zip, caminho relativo seguro) de tudo que está em ppt/media/."""
        selecionados = []
        total = 0
        for item in pacote.infolist():
            if not item.filename.startswith(self.PREFIXO_MIDIA) or item.is_dir():
                continue
            relativo = politica.aprovar(item, item.filename[len(self.PREFIXO_MIDIA):])
            total += item.file_size
            selecionados.append((item, relativo))
            if len(selecionados) > self.MAX_ARQUIVOS or total > self.MAX_BYTES:
                raise ValueError('Limite de extração excedido (20.000 arquivos ou 4 GiB).')
        if not selecionados:
            raise ValueError('A apresentação não tem mídia incorporada em ppt/media/.')
        return selecionados


# ---------------------------------------------------------------------------
# Classificação, gravação e empacotamento
# ---------------------------------------------------------------------------

class ClassificadorMidia:
    """Diz se cada arquivo é imagem, vídeo, áudio ou outro, pela extensão."""

    TIPOS = {
        'imagem': {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tif', '.tiff', '.svg',
                   '.emf', '.wmf', '.webp', '.ico', '.heic', '.jfif'},
        'video': {'.mp4', '.mov', '.m4v', '.avi', '.wmv', '.webm', '.mpg', '.mpeg', '.mkv'},
        'audio': {'.mp3', '.wav', '.m4a', '.wma', '.aac', '.ogg', '.flac', '.mid', '.midi'},
    }

    def classificar(self, caminho):
        extensao = PurePosixPath(caminho).suffix.lower()
        for tipo, extensoes in self.TIPOS.items():
            if extensao in extensoes:
                return tipo
        return 'outro'


class GravadorMidia:
    """Grava um arquivo do pacote no disco e confere tamanho e integridade (SHA-256)."""

    BLOCO = 1024 * 1024

    def gravar(self, pacote, item, destino):
        destino.parent.mkdir(parents=True, exist_ok=True)
        resumo = hashlib.sha256()
        contagem = 0
        # 'xb' = criar arquivo novo; falha se já existir, então nada é sobrescrito.
        with pacote.open(item) as entrada, destino.open('xb') as saida:
            for bloco in iter(lambda: entrada.read(self.BLOCO), b''):
                contagem += len(bloco)
                if contagem > item.file_size:
                    raise ValueError(f'Tamanho extraído excede o declarado: {item.filename}')
                resumo.update(bloco)
                saida.write(bloco)
        if contagem != item.file_size:
            raise ValueError(f'Tamanho extraído diverge do declarado: {item.filename}')
        if self._resumo_do_disco(destino) != resumo.digest():
            raise ValueError(f'Falha de integridade na gravação: {item.filename}')

    def _resumo_do_disco(self, caminho):
        resumo = hashlib.sha256()
        with caminho.open('rb') as arquivo:
            for bloco in iter(lambda: arquivo.read(self.BLOCO), b''):
                resumo.update(bloco)
        return resumo.digest()


class EmpacotadorZip:
    """Compacta a pasta media em um .zip, para ambientes que não baixam pastas."""

    @staticmethod
    def empacotar(pasta, arquivo_zip):
        with zipfile.ZipFile(arquivo_zip, 'x', compression=zipfile.ZIP_DEFLATED) as pacote:
            for caminho in sorted(p for p in pasta.rglob('*') if p.is_file()):
                pacote.write(caminho, PurePosixPath(pasta.name, *caminho.relative_to(pasta).parts))
        return arquivo_zip


@dataclass
class RelatorioExtracao:
    """Resumo devolvido ao agente em JSON."""

    pasta: str
    arquivos: int
    bytes: int
    por_tipo: dict = field(default_factory=dict)
    zip: str = None

    def para_json(self):
        return json.dumps(asdict(self), ensure_ascii=False)


# ---------------------------------------------------------------------------
# Orquestração
# ---------------------------------------------------------------------------

class ExtratorMidia:
    """Coordena as peças: valida, seleciona, grava, confere e (se pedido) compacta.

    As dependências chegam pelo construtor (baixo acoplamento): cada classe pode ser
    trocada ou testada sozinha.
    """

    # Uma política nova a cada extração, porque ela memoriza os nomes já aprovados.
    fabrica_politica = PoliticaNomeSeguro

    def __init__(self, validador=None, gravador=None, classificador=None, empacotador=None):
        self.validador = validador or ValidadorPacotePptx()
        self.gravador = gravador or GravadorMidia()
        self.classificador = classificador or ClassificadorMidia()
        self.empacotador = empacotador or EmpacotadorZip()

    def extrair(self, origem, destino, gerar_zip=False):
        origem = Path(origem).expanduser().resolve()
        destino = Path(destino).expanduser().resolve()
        self.validador.validar_arquivo(origem)
        if destino.exists():
            raise ValueError('O destino já existe. Escolha uma pasta nova para evitar sobrescritas.')
        criado = False
        try:
            # O .pptx é um .zip por dentro: o zipfile lê direto, só em modo leitura,
            # sem copiar nem renomear o original.
            with zipfile.ZipFile(origem) as pacote:
                self.validador.validar_estrutura(pacote)
                selecionados = self.validador.selecionar_midias(pacote, self.fabrica_politica())
                destino.mkdir(parents=True, exist_ok=False)
                criado = True
                pasta = destino / 'media'
                pasta.mkdir()
                for item, relativo in selecionados:
                    self.gravador.gravar(pacote, item, pasta.joinpath(*relativo.parts))
            if sum(p.is_file() for p in pasta.rglob('*')) != len(selecionados):
                raise ValueError('Quantidade extraída diverge do esperado.')
            relatorio = self._montar_relatorio(pasta, selecionados)
            if gerar_zip:
                relatorio.zip = str(self.empacotador.empacotar(pasta, destino / 'media.zip'))
            return relatorio
        except Exception:
            # Só apaga o que esta execução criou; o original nunca é tocado.
            if criado:
                shutil.rmtree(destino)
            raise

    def _montar_relatorio(self, pasta, selecionados):
        por_tipo = {}
        for _, relativo in selecionados:
            tipo = self.classificador.classificar(relativo)
            por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
        return RelatorioExtracao(
            pasta=str(pasta),
            arquivos=len(selecionados),
            bytes=sum(item.file_size for item, _ in selecionados),
            por_tipo=por_tipo,
        )


class AplicacaoCli:
    """Interface de linha de comando: subcomandos triagem, slides, extrair e link.

    Cada tipo de falha tem um código de saída próprio, para o agente decidir a próxima
    rota sem precisar interpretar o texto do erro.
    """

    SAIDA_ERRO = 1
    SAIDA_RESTRITO = 3
    SAIDA_SEM_CONEXAO = 4

    def __init__(self, extrator=None, leitor_link=None, baixador=None):
        self.extrator = extrator or ExtratorMidia()
        self.leitor_link = leitor_link or LeitorAtalhoGslides()
        self.baixador = baixador or BaixadorExportacao()
        self.fluxo_slides = FluxoGoogleSlides(self.leitor_link, self.baixador, self.extrator)
        self.triagem = TriagemAmbiente(self.baixador)
        self.parser = self._criar_parser()

    @staticmethod
    def _criar_parser():
        parser = argparse.ArgumentParser(description='Extrai a mídia de apresentações PowerPoint e Google Slides.')
        sub = parser.add_subparsers(dest='comando', required=True)
        triagem = sub.add_parser('triagem', help='Classifica o ambiente: consegue ou não pelo endpoint /export/pptx.')
        triagem.add_argument('entrada')
        slides = sub.add_parser('slides', help='Baixa pelo endpoint /export/pptx e extrai ppt/media.')
        slides.add_argument('entrada')
        extrair = sub.add_parser('extrair', help='Extrai ppt/media de um .pptx para uma pasta nova.')
        extrair.add_argument('pptx', type=Path)
        for comando in (slides, extrair):
            comando.add_argument('--destino', type=Path, required=True)
            comando.add_argument('--zip', action='store_true', help='Também gera media.zip para download.')
        link = sub.add_parser('link', help='Lê um .gslides ou URL e mostra o ID e a URL de exportação.')
        link.add_argument('entrada')
        return parser

    def executar(self, argumentos=None):
        args = self.parser.parse_args(argumentos)
        try:
            print(self._despachar(args))
        except AcessoRestritoError as erro:
            self.parser.exit(self.SAIDA_RESTRITO, f'Restrito: {erro}\n')
        except SemConexaoError as erro:
            self.parser.exit(self.SAIDA_SEM_CONEXAO, f'Sem conexão: {erro}\n')
        except (OSError, ValueError, zipfile.BadZipFile) as erro:
            self.parser.exit(self.SAIDA_ERRO, f'Erro: {erro}\n')

    def _despachar(self, args):
        if args.comando == 'slides':
            return self.fluxo_slides.executar(args.entrada, args.destino, args.zip).para_json()
        if args.comando == 'extrair':
            return self.extrator.extrair(args.pptx, args.destino, args.zip).para_json()
        referencia = self.leitor_link.identificar(args.entrada)
        if args.comando == 'triagem':
            return json.dumps(asdict(self.triagem.classificar(referencia)), ensure_ascii=False)
        return json.dumps(asdict(referencia), ensure_ascii=False)


if __name__ == '__main__':
    # Garante acentos corretos no terminal do Windows, sem quebrar em outros sistemas.
    for canal in (sys.stdout, sys.stderr):
        if hasattr(canal, 'reconfigure'):
            canal.reconfigure(encoding='utf-8')
    AplicacaoCli().executar()
