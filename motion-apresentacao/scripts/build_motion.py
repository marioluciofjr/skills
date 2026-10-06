#!/usr/bin/env python3
"""build_motion.py — monta o HTML final do motion a partir de um projeto.

Projeto = pasta com config.json, scenes.html (marcação das cenas), scenes.js (coreografia via Motion.compose)
e o logo PNG. O runtime (scripts/runtime) é embutido no HTML; o logo vira data URI.

Uso:
  python build_motion.py <projeto> [--out arquivo.html] [--inline-gsap gsap.min.js] [--inline-fonts fonts.css]

Por padrão GSAP e Google Fonts entram por CDN (o arquivo abre em qualquer navegador com internet).
--inline-gsap / --inline-fonts geram um HTML 100% offline (use os arquivos de prepare_deps.py).
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import quote_plus

sys.path.insert(0, str(Path(__file__).resolve().parent))
from motion_config import ConfigError, MotionConfig  # noqa: E402


class DataUri:
    """Converte arquivos locais em data URI (o arquivo vira texto dentro do HTML, sem depender da pasta)."""

    MIMES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
             ".svg": "image/svg+xml", ".webp": "image/webp"}

    @classmethod
    def of(cls, path: str | Path, mime: str | None = None) -> str:
        path = Path(path)
        mime = mime or cls.MIMES.get(path.suffix.lower(), "application/octet-stream")
        return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


class HtmlBuilder:
    """Junta config, cenas, coreografia e runtime no esqueleto shell.html.

    Cada método produz um pedaço do HTML (tema, fontes, GSAP, config do navegador); build() só os encaixa
    nos marcadores {{...}} do esqueleto. Assim dá para trocar a origem de um pedaço sem mexer nos outros.
    """

    RUNTIME_DIR = Path(__file__).resolve().parent / "runtime"
    CSS_FILES = ("motion-base.css", "components.css", "motion-types.css")
    # ordem importa: core primeiro; módulos se plugam no Motion; receitas e tipos por último
    JS_FILES = ("motion-core.js", "motion-particles.js", "motion-chrome.js", "motion-brand.js",
                "motion-recipes.js", "motion-types.js")
    GSAP_CDN = "https://cdnjs.cloudflare.com/ajax/libs/gsap/{v}/gsap.min.js"

    def __init__(self, project: Path, inline_gsap: Path | None = None, inline_fonts: Path | None = None):
        self.project = Path(project)
        self.inline_gsap = inline_gsap
        self.inline_fonts = inline_fonts
        self.cfg = MotionConfig.load(self.project)

    # ------------------------------------------------------------ pedaços do HTML
    def theme_css(self) -> str:
        """Tokens CSS (--bg, --fg, --W...) que todo o runtime usa para cores, tamanho e fontes."""
        t, f = self.cfg["theme"], self.cfg["fonts"]
        tokens = {f"--{k}": v for k, v in t.items()}
        tokens["--W"] = f"{self.cfg['width']}px"
        tokens["--H"] = f"{self.cfg['height']}px"
        tokens["--font-display"] = f"'{f['display']['family']}'"
        tokens["--font-mono"] = f"'{f['mono']['family']}'"
        return ":root{" + ";".join(f"{k}:{v}" for k, v in tokens.items()) + "}"

    def fonts_tag(self) -> str:
        if self.inline_fonts:
            return "<style>\n" + self.inline_fonts.read_text(encoding="utf-8") + "\n</style>"
        fams = "&".join(
            f"family={quote_plus(fam)}:wght@{';'.join(map(str, weights))}"
            for fam, weights in MotionConfig.font_families(self.cfg)
        )
        return ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
                '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
                f'<link href="https://fonts.googleapis.com/css2?{fams}&display=swap" rel="stylesheet">')

    def gsap_tag(self) -> str:
        if self.inline_gsap:
            return "<script>\n" + self.inline_gsap.read_text(encoding="utf-8") + "\n</script>"
        return f'<script src="{self.GSAP_CDN.format(v=self.cfg["gsap_version"])}"></script>'

    def client_config(self) -> dict:
        """Subconjunto do config que o navegador precisa (logo embutido, sem caminhos locais)."""
        brand = {k: v for k, v in self.cfg["brand"].items() if not k.startswith("_")}
        if self.cfg["brand"].get("_logo_path"):
            brand["logo"] = DataUri.of(self.cfg["brand"]["_logo_path"], "image/png")
        return {
            "width": self.cfg["width"], "height": self.cfg["height"], "loop": self.cfg["loop"],
            "locale": self.cfg["locale"], "brand": brand, "chrome": self.cfg.get("chrome"),
        }

    def scenes_html(self) -> str:
        """Marcação das cenas com {{LOGO}} resolvido e imagens relativas embutidas."""
        html = (self.project / "scenes.html").read_text(encoding="utf-8")
        html = re.sub(r'(src=")([^"]+)(")', self._embed_image, html)
        logo = self.cfg["brand"].get("_logo_path")
        return html.replace("{{LOGO}}", DataUri.of(logo, "image/png") if logo else "")

    def scenes_js(self) -> str:
        js = (self.project / "scenes.js").read_text(encoding="utf-8")
        if "Motion.compose" not in js:
            raise ConfigError("scenes.js precisa registrar a coreografia com Motion.compose(function (M) { ... })")
        return js

    def runtime(self, files: tuple[str, ...]) -> str:
        return "\n".join((self.RUNTIME_DIR / f).read_text(encoding="utf-8") for f in files)

    # ------------------------------------------------------------ montagem
    def render(self) -> str:
        """Devolve o HTML completo como texto (sem gravar nada em disco)."""
        parts = {
            "LANG": self.cfg["lang"],
            "TITLE": self.cfg["title"],
            "FONTS": self.fonts_tag(),
            "GSAP": self.gsap_tag(),
            "THEME": self.theme_css(),
            "CSS": self.runtime(self.CSS_FILES),
            "SCENES_HTML": self.scenes_html(),
            "CONFIG": json.dumps(self.client_config(), ensure_ascii=False),
            "RUNTIME": self.runtime(self.JS_FILES),
            "SCENES_JS": self.scenes_js(),
        }
        html = (self.RUNTIME_DIR / "shell.html").read_text(encoding="utf-8")
        for key, value in parts.items():
            html = html.replace("{{" + key + "}}", value)
        return html

    def build(self, out: Path | None = None) -> Path:
        """Grava o HTML em `out` (ou em <projeto>/dist/<titulo>.html) e devolve o caminho."""
        html = self.render()
        out = out or self.project / "dist" / f"{self._slug(self.cfg['title'])}.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        return out

    # ------------------------------------------------------------ auxiliares
    def _embed_image(self, m: re.Match) -> str:
        src = m.group(2)
        path = self.project / src
        if src.startswith(("data:", "http:", "https:")) or not path.exists():
            return m.group(0)
        return f"{m.group(1)}{DataUri.of(path)}{m.group(3)}"

    @staticmethod
    def _slug(title: str) -> str:
        plain = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode().lower()
        return re.sub(r"[^a-z0-9]+", "-", plain).strip("-") or "motion"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--inline-gsap", type=Path, help="embute este gsap.min.js (HTML offline)")
    ap.add_argument("--inline-fonts", type=Path, help="embute este fonts.css com data URIs (HTML offline)")
    a = ap.parse_args()
    try:
        out = HtmlBuilder(a.project, a.inline_gsap, a.inline_fonts).build(a.out)
    except ConfigError as e:
        sys.exit(f"[build] {e}")
    print(f"[build] OK -> {out} ({out.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
