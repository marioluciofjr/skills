#!/usr/bin/env python3
"""contact_sheet.py — monta uma grade de miniaturas para revisão visual (QA) de quadros.

Responsabilidade única: imagens -> uma imagem em grade. Também extrai quadros de um MP4 via ffmpeg.

Uso:
  python contact_sheet.py --images a.png b.png ... --out sheet.png
  python contact_sheet.py --video video.mp4 --times 2 6 10 --out sheet.png
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw


class ContactSheet:
    """Grade de miniaturas com rótulo opcional (ex.: o instante do quadro) no canto de cada uma."""

    def __init__(self, cols: int = 3, thumb_w: int = 960):
        self.cols = cols
        self.thumb_w = thumb_w

    def make(self, images: list[Path], out: Path, labels: list[str] | None = None) -> Path:
        if not images:
            raise ValueError("nenhuma imagem para a grade")
        first = Image.open(images[0])
        thumb_h = round(self.thumb_w * first.height / first.width)  # mantém a proporção do primeiro quadro
        rows = (len(images) + self.cols - 1) // self.cols
        sheet = Image.new("RGB", (self.cols * self.thumb_w, rows * thumb_h), "#111")
        draw = ImageDraw.Draw(sheet)
        for i, path in enumerate(images):
            x, y = (i % self.cols) * self.thumb_w, (i // self.cols) * thumb_h
            sheet.paste(Image.open(path).convert("RGB").resize((self.thumb_w, thumb_h)), (x, y))
            if labels:
                draw.rectangle([x, y, x + 110, y + 34], fill="#e00")
                draw.text((x + 10, y + 10), labels[i], fill="#fff")
        out.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(out)
        return out


class VideoFrameExtractor:
    """Tira quadros de um vídeo em instantes exatos com o ffmpeg (para conferir o MP4 já renderizado)."""

    def __init__(self, video: Path):
        if not shutil.which("ffmpeg"):
            sys.exit("[sheet] ffmpeg não encontrado no PATH")
        self.video = video

    def frames(self, times: list[float], workdir: Path) -> list[Path]:
        paths = []
        for t in times:
            p = workdir / f"v_{t:07.2f}.png"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(self.video), "-frames:v", "1", str(p)],
                           check=True)
            paths.append(p)
        return paths


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--images", nargs="*", type=Path, default=[])
    ap.add_argument("--video", type=Path)
    ap.add_argument("--times", nargs="*", type=float, default=[])
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--cols", type=int, default=3)
    a = ap.parse_args()
    sheet = ContactSheet(a.cols)
    if a.video:
        with tempfile.TemporaryDirectory() as tmp:
            imgs = VideoFrameExtractor(a.video).frames(a.times, Path(tmp))
            sheet.make(imgs, a.out, labels=[f"{t:.1f}s" for t in a.times])
    else:
        sheet.make(a.images, a.out)
    print(f"[sheet] OK -> {a.out}")


if __name__ == "__main__":
    main()
