#!/usr/bin/env python3
"""prepare_deps.py — baixa GSAP e as fontes do projeto para uso offline (renderização e HTML autocontido).

Fonte dos pacotes: registro npm (gsap e @fontsource/<família>), que costuma estar liberado em ambientes
onde CDNs e Google Fonts são bloqueados. Idempotente: reaproveita o que já existe no diretório.

Uso:
  python prepare_deps.py <projeto> [--dir ~/.cache/motion-deps]

Saída (no diretório de deps):
  gsap.min.js   — biblioteca GSAP na versão de config.gsap_version
  fonts.css     — @font-face com as fontes do config em data URI (latin + latin-ext)
"""
from __future__ import annotations

import argparse
import base64
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from motion_config import MotionConfig  # noqa: E402


def slugify(text: str) -> str:
    """'Inter Tight' -> 'inter-tight' (formato dos nomes de pacote do npm)."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


class NpmFetcher:
    """Baixa um pacote do npm (npm pack) e extrai numa pasta de trabalho. Não sabe o que há dentro dele."""

    SPEC = re.compile(r"@?[a-z0-9][a-z0-9._-]*(/[a-z0-9][a-z0-9._-]*)?(@[0-9A-Za-z.^~_-]+)?")

    def __init__(self, workdir: Path):
        self.workdir = workdir

    def fetch(self, spec: str) -> Path:
        """npm pack <spec> e extrai em workdir/<nome>; devolve a pasta 'package' (cache: não baixa duas vezes)."""
        # o spec vem do config.json (ex.: versão do GSAP); só nomes de pacote válidos passam, para que nenhum
        # caractere de shell (&, |, ;) chegue ao terminal do Windows, que executa o npm.cmd via cmd.exe
        if not self.SPEC.fullmatch(spec):
            sys.exit(f"[deps] nome de pacote inválido: {spec!r}")
        dest = self.workdir / slugify(spec)
        if (dest / "package").exists():
            return dest / "package"
        npm = shutil.which("npm")  # caminho completo: no Windows é npm.cmd, que o nome curto "npm" não acha
        if not npm:
            sys.exit("[deps] npm não encontrado; instale Node.js ou forneça gsap.min.js e fonts.css manualmente")
        dest.mkdir(parents=True, exist_ok=True)
        res = subprocess.run([npm, "pack", spec, "--silent"], cwd=dest, capture_output=True, text=True)
        tgz = res.stdout.strip().splitlines()[-1] if res.returncode == 0 and res.stdout.strip() else ""
        if not tgz:
            sys.exit(f"[deps] falha ao baixar {spec}: {res.stderr.strip()[:300]}")
        self._extract(dest / tgz, dest)
        return dest / "package"

    @staticmethod
    def _extract(tgz: Path, dest: Path) -> None:
        with tarfile.open(tgz) as tf:
            try:
                tf.extractall(dest, filter="data")  # filtro de segurança: impede arquivos fora de dest
            except TypeError:  # Python sem o parâmetro filter
                tf.extractall(dest)


class FontPackager:
    """Transforma os arquivos woff2 do @fontsource em regras @font-face com a fonte embutida (data URI)."""

    SUBSETS = ("latin", "latin-ext")  # latin-ext cobre acentos menos comuns

    def __init__(self, fetcher: NpmFetcher):
        self.fetcher = fetcher

    def font_faces(self, family: str, weights: list[int]) -> str:
        slug = slugify(family)
        pkg = self.fetcher.fetch(f"@fontsource/{slug}")
        css = []
        for w in weights:
            for subset in self.SUBSETS:
                f = pkg / "files" / f"{slug}-{subset}-{w}-normal.woff2"
                if not f.exists():
                    continue
                b64 = base64.b64encode(f.read_bytes()).decode()
                css.append(f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{w};font-display:block;"
                           f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")
        if not css:
            print(f"[deps] aviso: nenhum arquivo de fonte encontrado para {family} {weights}")
        return "\n".join(css)


class DepsPreparer:
    """Orquestra o preparo: GSAP + fonts.css no diretório de deps, a partir do config do projeto."""

    def __init__(self, project: Path, deps_dir: Path):
        self.cfg = MotionConfig.load(project)
        self.deps = deps_dir
        self.fetcher = NpmFetcher(deps_dir / "_npm")
        self.fonts = FontPackager(self.fetcher)

    def gsap(self) -> Path:
        out = self.deps / "gsap.min.js"
        if not out.exists():
            pkg = self.fetcher.fetch(f"gsap@{self.cfg['gsap_version']}")
            shutil.copy(pkg / "dist" / "gsap.min.js", out)
        return out

    def fonts_css(self) -> Path:
        css = "\n".join(self.fonts.font_faces(fam, ws) for fam, ws in MotionConfig.font_families(self.cfg))
        out = self.deps / "fonts.css"
        out.write_text(css, encoding="utf-8")
        return out

    def run(self) -> None:
        self.deps.mkdir(parents=True, exist_ok=True)
        gs = self.gsap()
        css = self.fonts_css()
        print(f"[deps] gsap  -> {gs}")
        print(f"[deps] fonts -> {css} ({css.stat().st_size / 1024:.0f} KB)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=Path)
    ap.add_argument("--dir", type=Path, default=Path.home() / ".cache" / "motion-deps")
    a = ap.parse_args()
    DepsPreparer(a.project, a.dir).run()


if __name__ == "__main__":
    main()
