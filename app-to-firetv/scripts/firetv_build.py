#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
firetv_build.py: monta, assina e verifica um APK de Fire TV (WebView + assets/index.html).

Funciona no Linux (ambiente de código do claude.ai) e no Windows (Claude Code, Antigravity,
Opencode). Toda saída é um JSON impresso no terminal, para o agente ler e relatar.

Subcomandos:
  ambiente   [--instalar]                       confere Java, keytool, JARs (com SHA-256) e dependências Python
  keystore   --slug S --nome N --saida DIR      cria a keystore com senha forte salva num arquivo .txt
  projeto    --dir W --slug S --nome N [...]    gera o projeto apktool a partir dos modelos de assets/
  icones     --dir W --nome N [...]             gera ícones (96 e 192 px) e banner (320x180) com Pillow
  empacotar  --dir W --slug S --keystore K ...  constrói, assina e verifica o APK
  link-drive URL                                converte o link do Google Drive no link direto de download
"""

import argparse
import hashlib
import json
import os
import platform
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path

PASTA_SKILL = Path(__file__).resolve().parent.parent
PASTA_ASSETS = PASTA_SKILL / "assets"


@dataclass
class ConfigApp:
    """Dados de identidade e versão do app, usados pelo projeto, pelo build e pela verificação."""
    slug: str
    nome: str
    pkg: str
    versao: str = "1.0.0"
    version_code: int = 1
    internet: bool = False
    html: str = None


@dataclass
class Paleta:
    """Cores do design system usadas nos ícones e no banner."""
    fundo: str = "#0a0f1a"
    destaque: str = "#f5b942"
    texto: str = "#f1f5f9"


@dataclass
class Credencial:
    """Keystore e senha usadas para assinar (a senha vem do arquivo .txt, nunca do chat)."""
    keystore: Path
    alias: str
    senha: str


@dataclass
class VersaoAnterior:
    """Dados da versão já instalada na TV, para garantir que a nova atualiza por cima."""
    version_code: int = None
    cert_sha256: str = None


class Resultado:
    """Padroniza a saída: sucesso, detalhes e dados extras, sempre em JSON."""

    @staticmethod
    def imprimir(sucesso: bool, detalhes: str, **dados) -> None:
        print(json.dumps({"success": sucesso, "details": detalhes, **dados}, indent=2, ensure_ascii=False))
        if not sucesso:
            sys.exit(1)


class Ambiente:
    """Descobre o sistema operacional, o Java, o keytool e a pasta de cache das ferramentas."""

    def __init__(self):
        self.windows = platform.system() == "Windows"
        self.cache = Path.home() / ".cache" / "app-to-firetv"
        self.cache.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def java():
        return shutil.which("java")

    def keytool(self):
        # O keytool vem com o Java, mas no Windows costuma ficar fora do PATH
        nome = "keytool.exe" if self.windows else "keytool"
        candidatos = [shutil.which("keytool")]
        if os.environ.get("JAVA_HOME"):
            candidatos.append(str(Path(os.environ["JAVA_HOME"]) / "bin" / nome))
        if self.java():
            candidatos.append(str(Path(os.path.realpath(self.java())).parent / nome))
        raizes = ([r"C:\Program Files\Java", r"C:\Program Files\Eclipse Adoptium", r"C:\Program Files\Microsoft",
                   r"C:\Program Files (x86)\Java"] if self.windows else ["/usr/lib/jvm"])
        for raiz in raizes:
            if os.path.isdir(raiz):
                candidatos += [str(p) for p in Path(raiz).glob(f"*/bin/{nome}")]
        return next((c for c in candidatos if c and os.path.isfile(c)), None)


class Toolchain:
    """Baixa o apktool e o uber-apk-signer e só aceita os arquivos se o SHA-256 bater."""

    # SHA-256 conferidos em 25/10/2026: apktool (GitHub e Bitbucket do autor) e uber-apk-signer (checksum oficial)
    JARS = {
        "apktool": ("apktool_2.10.0.jar",
                    "https://github.com/iBotPeaches/Apktool/releases/download/v2.10.0/apktool_2.10.0.jar",
                    "c0350abbab5314248dfe2ee0c907def4edd14f6faef1f5d372d3d4abd28f0431"),
        "uas": ("uber-apk-signer-1.3.0.jar",
                "https://github.com/patrickfav/uber-apk-signer/releases/download/v1.3.0/uber-apk-signer-1.3.0.jar",
                "e1299fd6fcf4da527dd53735b56127e8ea922a321128123b9c32d619bba1d835"),
    }

    def __init__(self, ambiente: Ambiente):
        self.pasta = ambiente.cache / "tools"
        self.pasta.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _sha256(arquivo: Path) -> str:
        h = hashlib.sha256()
        with open(arquivo, "rb") as f:
            for bloco in iter(lambda: f.read(1 << 20), b""):
                h.update(bloco)
        return h.hexdigest()

    def caminho(self, chave: str) -> Path:
        return self.pasta / self.JARS[chave][0]

    def garantir(self) -> dict:
        relatorio = {}
        for chave, (nome, url, esperado) in self.JARS.items():
            destino = self.pasta / nome
            if not destino.exists():
                urllib.request.urlretrieve(url, destino)
            obtido = self._sha256(destino)
            if obtido != esperado:
                destino.unlink()  # arquivo adulterado ou corrompido: nunca usar
                raise RuntimeError(f"SHA-256 de {nome} não confere (esperado {esperado}, obtido {obtido}). Download descartado.")
            relatorio[chave] = str(destino)
        return relatorio


class DependenciasPython:
    """Garante Pillow e Playwright num ambiente virtual próprio, sem mexer no Python do sistema."""

    MODULOS = {"PIL": "pillow", "playwright": "playwright"}

    def __init__(self, ambiente: Ambiente):
        self.venv = ambiente.cache / "venv"
        sub = "Scripts/python.exe" if ambiente.windows else "bin/python"
        self.python_venv = self.venv / sub

    def faltando(self, python: str) -> list:
        faltam = []
        for modulo, pacote in self.MODULOS.items():
            r = subprocess.run([python, "-c", f"import {modulo}"], capture_output=True)
            if r.returncode != 0:
                faltam.append(pacote)
        return faltam

    def python_recomendado(self) -> str:
        # Se o Python atual já tem tudo, usa ele; senão, usa o ambiente virtual da skill
        if not self.faltando(sys.executable):
            return sys.executable
        return str(self.python_venv)

    def situacao(self) -> dict:
        atual = self.faltando(sys.executable)
        venv = self.faltando(str(self.python_venv)) if self.python_venv.exists() else list(self.MODULOS.values())
        return {"faltando_no_python_atual": atual, "faltando_no_venv": venv}

    def instalar(self) -> str:
        if not self.faltando(sys.executable):
            python = sys.executable
        else:
            if not self.python_venv.exists():
                subprocess.run([sys.executable, "-m", "venv", str(self.venv)], check=True)
            python = str(self.python_venv)
            faltam = self.faltando(python)
            if faltam:
                # --retries e --timeout ajudam em conexões instáveis (quedas no meio do download)
                subprocess.run([python, "-m", "pip", "install", "-q", "--retries", "8", "--timeout", "60", *faltam], check=True)
        # O navegador do Playwright é baixado uma vez para a pasta de cache dele
        # capture_output evita que a barra de progresso do download suje o JSON de saída
        r = subprocess.run([python, "-m", "playwright", "install", "chromium"], capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"Falha ao baixar o Chromium do Playwright: {r.stderr[-800:]}")
        return python


class GeradorKeystore:
    """Cria a keystore PKCS12 com senha forte, gravada num arquivo e nunca no chat."""

    def __init__(self, ambiente: Ambiente):
        self.keytool = ambiente.keytool()

    def criar(self, slug: str, nome: str, saida: Path) -> dict:
        if not self.keytool:
            raise RuntimeError("keytool não encontrado. Instale um JDK ou JRE (Java 8 ou mais novo).")
        saida.mkdir(parents=True, exist_ok=True)
        keystore = saida / f"{slug}-release.p12"
        arquivo_senha = saida / f"{slug}-keystore-senha.txt"
        if keystore.exists():
            raise RuntimeError(f"Já existe {keystore}. Reaproveite essa keystore; criar outra impede atualizar o app por cima.")
        senha = secrets.token_urlsafe(18)
        # A senha vai para o keytool por arquivo temporário, não pela linha de comando
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") as tmp:
            tmp.write(senha)
        try:
            subprocess.run([self.keytool, "-genkeypair", "-keystore", str(keystore), "-storetype", "PKCS12",
                            "-storepass:file", tmp.name, "-keypass:file", tmp.name, "-alias", slug,
                            "-keyalg", "RSA", "-keysize", "2048", "-validity", "10000",
                            "-dname", f"CN={nome}, C=BR"], check=True, capture_output=True, text=True)
        finally:
            os.unlink(tmp.name)
        arquivo_senha.write_text(
            f"Keystore: {keystore.name}\nAlias: {slug}\nSenha: {senha}\n\n"
            "Guarde este arquivo e a keystore juntos e em local seguro.\n"
            "Sem eles não é possível publicar atualizações por cima do app instalado.\n", encoding="utf-8")
        return {"keystore": str(keystore), "alias": slug, "arquivo_senha": str(arquivo_senha)}


class ProjetoApktool:
    """Gera a pasta do projeto apktool a partir dos modelos de assets/."""

    def __init__(self, pasta_trabalho: Path):
        self.proj = pasta_trabalho / "proj"

    @staticmethod
    def validar(slug: str, pkg: str) -> None:
        if not re.fullmatch(r"[a-z][a-z0-9]*", slug):
            raise ValueError("slug inválido: use só letras minúsculas e números, começando por letra (ex.: xadrez).")
        if not re.fullmatch(r"[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+", pkg):
            raise ValueError("package inválido (ex.: com.firetv.xadrez).")

    def gerar(self, app: ConfigApp) -> dict:
        self.validar(app.slug, app.pkg)
        pkgpath = app.pkg.replace(".", "/")
        trocas = {"__PKG__": app.pkg, "__PKGPATH__": pkgpath, "__SCHEME__": app.slug, "__APP_NAME__": app.nome,
                  "__VERSION_CODE__": str(app.version_code), "__VERSION_NAME__": app.versao,
                  "__INTERNET_PERMISSION__": '<uses-permission android:name="android.permission.INTERNET"/>' if app.internet else ""}
        arquivos = {
            "AndroidManifest.xml.tpl": "AndroidManifest.xml",
            "apktool.yml.tpl": "apktool.yml",
            "strings.xml.tpl": "res/values/strings.xml",
            "MainActivity.smali.tpl": f"smali/{pkgpath}/MainActivity.smali",
            # O modelo não usa "$" no nome (o claude.ai recusa esse caractere no zip da skill),
            # mas o arquivo gerado precisa do "$": é o nome da classe interna no Android
            "MainActivity_Client.smali.tpl": f"smali/{pkgpath}/MainActivity$Client.smali",
        }
        for modelo, destino in arquivos.items():
            self._escrever(PASTA_ASSETS / modelo, self.proj / destino, trocas)
        origem_html = Path(app.html) if app.html else PASTA_ASSETS / "index-base.html"
        self._escrever(origem_html, self.proj / "assets" / "index.html", trocas)
        return {"projeto": str(self.proj), "package": app.pkg, "versionCode": app.version_code, "versionName": app.versao,
                "index_html": str(self.proj / "assets" / "index.html")}

    @staticmethod
    def _escrever(origem: Path, destino: Path, trocas: dict) -> None:
        texto = origem.read_text(encoding="utf-8")
        for marcador, valor in trocas.items():
            texto = texto.replace(marcador, valor)
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(texto, encoding="utf-8", newline="\n")


class AjustadorDeTexto:
    """Escolhe uma fonte disponível no sistema e encaixa um texto centralizado numa caixa."""

    FONTES = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", r"C:\Windows\Fonts\segoeuib.ttf",
              r"C:\Windows\Fonts\arialbd.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"]

    def __init__(self, image_font):
        self.ImageFont = image_font

    def _fonte(self, tamanho):
        for caminho in self.FONTES:
            if os.path.isfile(caminho):
                return self.ImageFont.truetype(caminho, tamanho)
        return self.ImageFont.load_default(size=tamanho)

    def centralizar(self, desenho, caixa, texto, cor):
        # Começa grande e diminui até o texto caber com folga na caixa
        largura, altura = caixa[2] - caixa[0], caixa[3] - caixa[1]
        tamanho = int(altura * 0.6)
        while tamanho > 10:
            fonte = self._fonte(tamanho)
            l, t, r, b = desenho.textbbox((0, 0), texto, font=fonte)
            if r - l <= largura * 0.86 and b - t <= altura * 0.7:
                break
            tamanho -= 2
        x = caixa[0] + (largura - (r - l)) / 2 - l
        y = caixa[1] + (altura - (b - t)) / 2 - t
        desenho.text((x, y), texto, font=fonte, fill=cor)


class GeradorIcones:
    """Desenha ícones e banner originais (sem logotipos de terceiros) com as cores do design system."""

    def __init__(self, pasta_trabalho: Path):
        from PIL import Image, ImageDraw, ImageFont  # import aqui: só este subcomando precisa do Pillow
        self.Image, self.ImageDraw = Image, ImageDraw
        self.texto = AjustadorDeTexto(ImageFont)
        self.res = pasta_trabalho / "proj" / "res"

    @staticmethod
    def _rgb(hexa):
        hexa = hexa.lstrip("#")
        return tuple(int(hexa[i:i + 2], 16) for i in (0, 2, 4))

    def gerar(self, nome: str, sigla: str, paleta: Paleta) -> dict:
        cf, cd, ct = self._rgb(paleta.fundo), self._rgb(paleta.destaque), self._rgb(paleta.texto)
        saidas = {}
        for pasta, lado in (("mipmap-xhdpi", 96), ("mipmap-xxxhdpi", 192)):
            img = self.Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
            d = self.ImageDraw.Draw(img)
            borda = max(3, lado // 24)
            d.rounded_rectangle((0, 0, lado - 1, lado - 1), radius=lado // 5, fill=cf, outline=cd, width=borda)
            self.texto.centralizar(d, (0, 0, lado, lado), sigla, cd)
            destino = self.res / pasta / "ic_launcher.png"
            destino.parent.mkdir(parents=True, exist_ok=True)
            img.save(destino)
            saidas[f"icone_{lado}"] = str(destino)
        banner = self.Image.new("RGB", (320, 180), cf)
        d = self.ImageDraw.Draw(banner)
        d.rectangle((0, 168, 320, 180), fill=cd)
        self.texto.centralizar(d, (12, 10, 308, 160), nome, ct)
        destino = self.res / "drawable-xhdpi" / "banner.png"
        destino.parent.mkdir(parents=True, exist_ok=True)
        banner.save(destino)
        saidas["banner"] = str(destino)
        return saidas


class Empacotador:
    """Constrói com apktool e assina com uber-apk-signer (zipalign + assinaturas v1, v2 e v3)."""

    def __init__(self, toolchain: Toolchain, pasta_trabalho: Path):
        self.tc = toolchain
        self.w = pasta_trabalho

    @staticmethod
    def _rodar(comando):
        r = subprocess.run(comando, capture_output=True, text=True, encoding="utf-8", errors="replace")
        return r.returncode, r.stdout + r.stderr

    def construir_e_assinar(self, app: ConfigApp, cred: Credencial) -> dict:
        senha = cred.senha
        saida = self.w / "out"
        assinado = self.w / "signed"
        saida.mkdir(exist_ok=True)
        if assinado.exists():
            shutil.rmtree(assinado)
        codigo, log = self._rodar(["java", "-jar", str(self.tc.caminho("apktool")), "b", str(self.w / "proj"),
                                   "-o", str(saida / "unsigned.apk")])
        if codigo != 0:
            raise RuntimeError(f"apktool falhou:\n{log[-2000:]}")
        codigo, log = self._rodar(["java", "-jar", str(self.tc.caminho("uas")), "-a", str(saida / "unsigned.apk"),
                                   "--ks", str(cred.keystore), "--ksAlias", cred.alias, "--ksPass", senha, "--ksKeyPass", senha,
                                   "-o", str(assinado)])
        log = log.replace(senha, "***")  # nunca devolver a senha no relatório
        if codigo != 0:
            raise RuntimeError(f"uber-apk-signer falhou:\n{log[-2000:]}")
        criterios = {"zipalign verified": "zipalign verified" in log,
                     "signature verified [v1, v2, v3]": bool(re.search(r"signature verified \[v1, v2, v3\]", log))}
        apk_assinado = next(assinado.glob("*-aligned-signed.apk"))
        final = saida / f"{app.slug}_v{app.versao}.apk"
        shutil.copyfile(apk_assinado, final)
        return {"apk": str(final), "criterios_assinatura": criterios}


class VerificadorApk:
    """Confere o APK final: package, versionCode, ícone, banner, certificado e o index.html empacotado."""

    def __init__(self, ambiente: Ambiente, toolchain: Toolchain, pasta_trabalho: Path):
        self.keytool = ambiente.keytool()
        self.tc = toolchain
        self.proj = pasta_trabalho / "proj"

    def verificar(self, apk: Path, app: ConfigApp, anterior: VersaoAnterior) -> dict:
        crit = {}
        with tempfile.TemporaryDirectory() as tmp:
            dec = Path(tmp) / "dec"
            # Decompila o APK inteiro (inclusive o código) para conferir o que foi realmente empacotado
            subprocess.run(["java", "-jar", str(self.tc.caminho("apktool")), "d", "-f", str(apk), "-o", str(dec)],
                           check=True, capture_output=True)
            manifesto = (dec / "AndroidManifest.xml").read_text(encoding="utf-8")
            yml = (dec / "apktool.yml").read_text(encoding="utf-8")
            pkg = re.search(r'package="([^"]+)"', manifesto).group(1)
            vc = int(re.search(r"versionCode:\s*'?(\d+)", yml).group(1))
            crit["package"] = pkg == app.pkg
            crit["versionCode"] = vc == app.version_code
            # Para atualizar por cima, o versionCode novo tem de ser maior que o anterior
            crit["versionCode_maior_que_anterior"] = (vc > anterior.version_code) if anterior.version_code else None
            crit["leanback_launcher"] = "LEANBACK_LAUNCHER" in manifesto
            crit["icone_e_banner"] = all((dec / "res" / p).is_file() for p in
                                         ("mipmap-xhdpi/ic_launcher.png", "mipmap-xxxhdpi/ic_launcher.png", "drawable-xhdpi/banner.png"))
            # As duas classes precisam existir no APK; sem a Client, o app fecha ao abrir
            pasta_classes = dec / "smali" / app.pkg.replace(".", "/")
            crit["classes_java"] = all((pasta_classes / nome).is_file()
                                       for nome in ("MainActivity.smali", "MainActivity$Client.smali"))
        with zipfile.ZipFile(apk) as z:
            crit["index_html_identico"] = z.read("assets/index.html") == (self.proj / "assets" / "index.html").read_bytes()
        cert = self._sha256_certificado(apk)
        crit["certificado_lido"] = bool(cert)
        crit["certificado_igual_ao_anterior"] = (
            cert == anterior.cert_sha256.upper().replace(":", "")) if anterior.cert_sha256 else None
        return {"package": pkg, "versionCode": vc, "sha256_certificado": cert, "criterios": crit}

    def _sha256_certificado(self, apk: Path) -> str:
        r = subprocess.run([self.keytool, "-printcert", "-jarfile", str(apk)], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        achado = re.search(r"SHA256:\s*([0-9A-F:]+)", r.stdout)
        return achado.group(1).replace(":", "") if achado else ""


class LinkDrive:
    """Transforma o link de compartilhamento do Drive no link direto que o Downloader consegue baixar."""

    PADROES = [r"/file/d/([A-Za-z0-9_-]{20,})", r"[?&]id=([A-Za-z0-9_-]{20,})"]

    def converter(self, url: str) -> dict:
        if "/folders/" in url:
            raise ValueError("Esse é um link de PASTA. Abra a pasta, clique com o botão direito no APK, "
                             "escolha Compartilhar > Copiar link e use o link do ARQUIVO.")
        for padrao in self.PADROES:
            achado = re.search(padrao, url)
            if achado:
                arquivo_id = achado.group(1)
                return {"id": arquivo_id, "link_para_encurtar": f"https://drive.google.com/uc?export=download&id={arquivo_id}"}
        raise ValueError("Não encontrei o ID do arquivo. O link deve ter o formato https://drive.google.com/file/d/<ID>/view")


class Cli:
    """Interpreta os argumentos e chama a classe certa para cada subcomando."""

    def __init__(self):
        self.parser = self._montar()

    @staticmethod
    def _montar():
        p = argparse.ArgumentParser(description="Build de APK para Fire TV")
        sub = p.add_subparsers(dest="cmd", required=True)
        a = sub.add_parser("ambiente"); a.add_argument("--instalar", action="store_true")
        k = sub.add_parser("keystore")
        k.add_argument("--slug", required=True); k.add_argument("--nome", required=True); k.add_argument("--saida", required=True)
        pr = sub.add_parser("projeto")
        pr.add_argument("--dir", required=True); pr.add_argument("--slug", required=True); pr.add_argument("--nome", required=True)
        pr.add_argument("--pkg"); pr.add_argument("--versao", default="1.0.0"); pr.add_argument("--version-code", type=int, default=1)
        pr.add_argument("--internet", action="store_true"); pr.add_argument("--html")
        ic = sub.add_parser("icones")
        ic.add_argument("--dir", required=True); ic.add_argument("--nome", required=True); ic.add_argument("--sigla")
        ic.add_argument("--fundo", default="#0a0f1a"); ic.add_argument("--destaque", default="#f5b942"); ic.add_argument("--texto", default="#f1f5f9")
        e = sub.add_parser("empacotar")
        e.add_argument("--dir", required=True); e.add_argument("--slug", required=True); e.add_argument("--pkg")
        e.add_argument("--versao", default="1.0.0"); e.add_argument("--version-code", type=int, default=1)
        e.add_argument("--keystore", required=True); e.add_argument("--alias")
        e.add_argument("--senha-arquivo", required=True)
        e.add_argument("--version-code-anterior", type=int); e.add_argument("--cert-anterior")
        l = sub.add_parser("link-drive"); l.add_argument("url")
        return p

    def executar(self, argv=None):
        a = self.parser.parse_args(argv)
        try:
            getattr(self, "_" + a.cmd.replace("-", "_"))(a)
        except Exception as erro:
            Resultado.imprimir(False, str(erro))

    @staticmethod
    def _app(a) -> ConfigApp:
        # Monta o objeto do app a partir dos argumentos comuns aos subcomandos
        return ConfigApp(slug=a.slug, nome=getattr(a, "nome", a.slug), pkg=a.pkg or f"com.firetv.{a.slug}",
                         versao=a.versao, version_code=a.version_code,
                         internet=getattr(a, "internet", False), html=getattr(a, "html", None))

    @staticmethod
    def _ambiente(a):
        amb = Ambiente(); deps = DependenciasPython(amb)
        python = deps.instalar() if a.instalar else deps.python_recomendado()
        jars = Toolchain(amb).garantir()
        dados = {"sistema": platform.system(), "java": amb.java(), "keytool": amb.keytool(), "jars": jars,
                 "python_para_icones_e_testes": python, "dependencias": deps.situacao()}
        python_ok = os.path.exists(python) and not deps.faltando(python)
        ok = bool(amb.java() and amb.keytool() and python_ok)
        Resultado.imprimir(ok, "Ambiente pronto." if ok else
                           "Faltam ferramentas: veja os campos vazios ou rode novamente com --instalar.", **dados)

    @staticmethod
    def _keystore(a):
        Resultado.imprimir(True, "Keystore criada. Entregue a keystore e o arquivo de senha à pessoa usuária.",
                           **GeradorKeystore(Ambiente()).criar(a.slug, a.nome, Path(a.saida)))

    @staticmethod
    def _projeto(a):
        Resultado.imprimir(True, "Projeto gerado.", **ProjetoApktool(Path(a.dir)).gerar(Cli._app(a)))

    @staticmethod
    def _icones(a):
        # Sigla com as iniciais das palavras principais (ignora "de", "da", "e"...)
        palavras = [p for p in a.nome.split() if len(p) > 2] or a.nome.split()
        sigla = a.sigla or "".join(p[0] for p in palavras[:2]).upper()
        paleta = Paleta(fundo=a.fundo, destaque=a.destaque, texto=a.texto)
        Resultado.imprimir(True, "Ícones e banner gerados. Abra os PNGs para conferir.",
                           **GeradorIcones(Path(a.dir)).gerar(a.nome, sigla, paleta))

    @staticmethod
    def _empacotar(a):
        amb = Ambiente(); tc = Toolchain(amb); tc.garantir()
        w = Path(a.dir); app = Cli._app(a)
        senha = re.search(r"^Senha:\s*(\S+)", Path(a.senha_arquivo).read_text(encoding="utf-8"), re.M).group(1)
        cred = Credencial(keystore=Path(a.keystore), alias=a.alias or a.slug, senha=senha)
        build = Empacotador(tc, w).construir_e_assinar(app, cred)
        anterior = VersaoAnterior(version_code=a.version_code_anterior, cert_sha256=a.cert_anterior)
        verif = VerificadorApk(amb, tc, w).verificar(Path(build["apk"]), app, anterior)
        todos = list(build["criterios_assinatura"].values()) + [v for v in verif["criterios"].values() if v is not None]
        Resultado.imprimir(all(todos), "Todos os critérios de aceite passaram." if all(todos)
                           else "Algum critério de aceite falhou: veja os campos com false.", **build, **verif)

    @staticmethod
    def _link_drive(a):
        Resultado.imprimir(True, "Cole este link no https://go.aftvnews.com para gerar o código.", **LinkDrive().converter(a.url))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    Cli().executar()
