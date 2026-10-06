#!/usr/bin/env python3
"""extract_logo.py — prepara o logo da marca como silhueta PNG transparente + metadados (logo.json).

Subcomandos:
  page        renderiza uma página de PDF em baixa resolução para localizar o logo (imprime tamanho em pt)
  pdf         recorta uma área (em pt) de uma página de PDF em alta resolução e gera a silhueta
  image       gera a silhueta a partir de um PNG/JPG/WebP (ou SVG, se rsvg-convert existir)
  placeholder gera um logo provisório (símbolo circular + nome) quando não há arquivo da marca

Saída: <out>.png (silhueta na cor escolhida, fundo transparente, recortada justa)
       <out>.json {aspect, mark_end, word_start} — onde termina o símbolo e começa o nome (frações da largura),
       detectados pelo maior vão vertical entre o primeiro bloco e o resto. Sem vão: mark_end = word_start = 1.

Exemplos:
  python extract_logo.py page --pdf relatorio.pdf --page 1 --out pag1.png
  python extract_logo.py pdf --pdf relatorio.pdf --page 1 --bbox 306,36,132,38 --out logo.png
  python extract_logo.py image --src logo-site.png --out logo.png
  python extract_logo.py placeholder --text "Marca" --out logo.png
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


class LogoSilhouette:
    """Transforma qualquer imagem de logo em silhueta de uma cor e grava PNG + logo.json.

    Só lida com pixels: não sabe de onde a imagem veio (PDF, arquivo, placeholder).
    """

    MAX_HEIGHT = 600  # altura suficiente para o símbolo em tela cheia sem pesar o HTML
    PAD = 4           # respiro em px ao redor do recorte justo

    def __init__(self, color: str = "#ffffff"):
        self.color = color

    def from_image(self, img: Image.Image) -> Image.Image:
        """Converte o logo em silhueta de uma cor sobre transparente.

        Com canal alfa útil, usa o alfa. Sem ele, estima o fundo pela mediana das bordas e usa a distância
        de luminância ao fundo como opacidade (funciona para logo luminoso em fundo escuro e vice-versa).
        """
        rgba = np.array(img.convert("RGBA")).astype(float)
        alpha = rgba[..., 3]
        a = alpha if alpha.min() < 250 else self._alpha_from_luminance(rgba)
        r, g, b = Image.new("RGB", (1, 1), self.color).getpixel((0, 0))
        out = np.zeros(rgba.shape, dtype=np.uint8)
        out[..., 0], out[..., 1], out[..., 2] = r, g, b
        out[..., 3] = a.astype(np.uint8)
        return self._crop(Image.fromarray(out, "RGBA"))

    @staticmethod
    def split_meta(sil: Image.Image, min_gap: float = 0.025, max_mark: float = 0.45) -> dict:
        """Detecta símbolo x nome pelo maior vão vertical relevante entre blocos de tinta."""
        ink = np.array(sil.getchannel("A")).max(axis=0) > 60
        w = len(ink)
        runs, start = [], None
        for x, v in enumerate(ink):
            if v and start is None:
                start = x
            if not v and start is not None:
                runs.append((start, x))
                start = None
        if start is not None:
            runs.append((start, w))
        meta = {"aspect": round(sil.width / sil.height, 4), "mark_end": 1, "word_start": 1}
        # maior vão entre blocos cujo lado esquerdo (o símbolo) ocupe no máximo max_mark da largura
        best = None
        for left, right in zip(runs, runs[1:]):
            gap = right[0] - left[1]
            if left[1] / w <= max_mark and gap / w >= min_gap and (best is None or gap > best[0]):
                best = (gap, left[1], right[0])
        if best:
            gap, end, nxt = best
            meta["mark_end"] = round(min(1, (end + gap * 0.3) / w), 4)
            meta["word_start"] = round(max(0, (nxt - gap * 0.3) / w), 4)
        return meta

    def save(self, img: Image.Image, out: Path) -> None:
        """Gera a silhueta de `img` e grava <out>.png + <out>.json."""
        sil = self.from_image(img)
        out = out.with_suffix(".png")
        out.parent.mkdir(parents=True, exist_ok=True)
        if sil.height > self.MAX_HEIGHT:
            sil = sil.resize((round(sil.width * self.MAX_HEIGHT / sil.height), self.MAX_HEIGHT), Image.LANCZOS)
        sil.save(out, optimize=True)
        meta = self.split_meta(sil)
        out.with_suffix(".json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
        print(f"[logo] OK -> {out} {sil.size} | {meta}")

    # ------------------------------------------------------------ auxiliares
    @staticmethod
    def _alpha_from_luminance(rgba: np.ndarray) -> np.ndarray:
        lum = rgba[..., :3] @ np.array([0.2126, 0.7152, 0.0722])
        border = np.concatenate([lum[0], lum[-1], lum[:, 0], lum[:, -1]])
        dist = np.abs(lum - np.median(border))
        hi = np.percentile(dist, 99.5) or 1
        return np.clip((dist - hi * 0.15) / (hi * 0.85), 0, 1) * 255

    def _crop(self, sil: Image.Image) -> Image.Image:
        bbox = sil.getchannel("A").point(lambda v: 255 if v > 20 else 0).getbbox()
        if not bbox:
            raise SystemExit("[logo] nenhuma forma encontrada na área informada")
        p = self.PAD
        return sil.crop((max(0, bbox[0] - p), max(0, bbox[1] - p), min(sil.width, bbox[2] + p), min(sil.height, bbox[3] + p)))


class PdfRasterizer:
    """Converte páginas (ou recortes) de PDF em PNG com o poppler-utils (pdftoppm, pdfinfo)."""

    HIRES_DPI = 1200

    @staticmethod
    def _need(tool: str) -> None:
        if not shutil.which(tool):
            sys.exit(f"[logo] '{tool}' não encontrado (pacote poppler-utils)")

    def page_size_pt(self, pdf: Path, page: int) -> tuple[float, float]:
        self._need("pdfinfo")
        info = subprocess.run(["pdfinfo", "-f", str(page), "-l", str(page), str(pdf)], capture_output=True, text=True).stdout
        for line in info.splitlines():
            if line.startswith("Page") and "size" in line:
                nums = [float(t) for t in line.split(":")[1].split() if t.replace(".", "", 1).isdigit()]
                return nums[0], nums[1]
        return 595.0, 842.0  # A4 como último recurso

    def page(self, pdf: Path, page: int, dpi: int, stem: str) -> None:
        self._need("pdftoppm")
        subprocess.run(["pdftoppm", "-png", "-r", str(dpi), "-f", str(page), "-l", str(page), "-singlefile",
                        str(pdf), stem], check=True)

    def crop(self, pdf: Path, page: int, bbox_pt: tuple[float, ...], workdir: Path) -> Path:
        """Recorta a área (x, y, largura, altura em pt) em alta resolução; devolve o PNG."""
        self._need("pdftoppm")
        x, y, w, h = bbox_pt
        k = self.HIRES_DPI / 72  # 1 pt = 1/72 polegada
        stem = workdir / "crop"
        subprocess.run(["pdftoppm", "-png", "-r", str(self.HIRES_DPI), "-f", str(page), "-l", str(page), "-singlefile",
                        "-x", str(round(x * k)), "-y", str(round(y * k)), "-W", str(round(w * k)), "-H", str(round(h * k)),
                        str(pdf), str(stem)], check=True)
        return Path(f"{stem}.png")


class PlaceholderLogo:
    """Desenha um logo provisório: anel com ponto central + nome, para quando a marca não tem arquivo."""

    FONT_CANDIDATES = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    )
    HEIGHT = 400

    def __init__(self, color: str):
        self.color = color

    def _font(self) -> ImageFont.FreeTypeFont:
        for cand in self.FONT_CANDIDATES:
            if Path(cand).exists():
                return ImageFont.truetype(cand, 230)
        return ImageFont.load_default(size=230)

    def draw(self, text: str) -> Image.Image:
        h, font = self.HEIGHT, self._font()
        tw = int(ImageDraw.Draw(Image.new("L", (1, 1))).textlength(text, font=font))
        img = Image.new("RGBA", (h + 80 + tw + 20, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.ellipse([20, 20, h - 20, h - 20], outline=self.color, width=44)
        d.ellipse([h / 2 - 50, h / 2 - 50, h / 2 + 50, h / 2 + 50], fill=self.color)
        d.text((h + 80, h / 2), text, font=font, fill=self.color, anchor="lm")
        return img


class LogoExtractorCli:
    """Interface de linha de comando: um método por subcomando, cada um ligando a fonte certa à silhueta."""

    def __init__(self):
        self.pdf = PdfRasterizer()

    def cmd_page(self, a) -> None:
        w, h = self.pdf.page_size_pt(a.pdf, a.page)
        stem = str(a.out.with_suffix(""))
        self.pdf.page(a.pdf, a.page, a.dpi, stem)
        print(f"[logo] página {a.page}: {w:.1f} x {h:.1f} pt -> {stem}.png ({a.dpi} dpi; pt = px * 72 / {a.dpi})")

    @staticmethod
    def _export(img: Image.Image, a) -> None:
        """Ponto único de saída: toda origem (PDF, arquivo, placeholder) termina aqui como silhueta."""
        LogoSilhouette(a.color).save(img, a.out)

    def cmd_pdf(self, a) -> None:
        bbox = tuple(float(v) for v in a.bbox.split(","))
        with tempfile.TemporaryDirectory() as tmp:
            png = self.pdf.crop(a.pdf, a.page, bbox, Path(tmp))
            self._export(Image.open(png), a)

    def cmd_image(self, a) -> None:
        src = a.src
        if src.suffix.lower() == ".svg":
            if not shutil.which("rsvg-convert"):
                sys.exit("[logo] para SVG instale rsvg-convert (librsvg) ou exporte o SVG como PNG")
            tmp = Path(tempfile.mkdtemp()) / "logo.png"
            subprocess.run(["rsvg-convert", "-h", "800", "-o", str(tmp), str(src)], check=True)
            src = tmp
        self._export(Image.open(src), a)

    def cmd_placeholder(self, a) -> None:
        self._export(PlaceholderLogo(a.color).draw(a.text), a)

    def parser(self) -> argparse.ArgumentParser:
        ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
        sub = ap.add_subparsers(dest="cmd", required=True)
        p = sub.add_parser("page")
        p.add_argument("--pdf", type=Path, required=True)
        p.add_argument("--page", type=int, default=1)
        p.add_argument("--dpi", type=int, default=72)
        p.add_argument("--out", type=Path, required=True)
        p.set_defaults(fn=self.cmd_page)
        p = sub.add_parser("pdf")
        p.add_argument("--pdf", type=Path, required=True)
        p.add_argument("--page", type=int, default=1)
        p.add_argument("--bbox", required=True, help="x,y,largura,altura em pontos (origem no topo esquerdo)")
        p.add_argument("--color", default="#ffffff")
        p.add_argument("--out", type=Path, required=True)
        p.set_defaults(fn=self.cmd_pdf)
        p = sub.add_parser("image")
        p.add_argument("--src", type=Path, required=True)
        p.add_argument("--color", default="#ffffff")
        p.add_argument("--out", type=Path, required=True)
        p.set_defaults(fn=self.cmd_image)
        p = sub.add_parser("placeholder")
        p.add_argument("--text", required=True)
        p.add_argument("--color", default="#ffffff")
        p.add_argument("--out", type=Path, required=True)
        p.set_defaults(fn=self.cmd_placeholder)
        return ap

    def run(self) -> None:
        a = self.parser().parse_args()
        a.fn(a)


if __name__ == "__main__":
    LogoExtractorCli().run()
