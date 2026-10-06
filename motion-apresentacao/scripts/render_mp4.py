#!/usr/bin/env python3
"""render_mp4.py — renderiza o HTML do motion em MP4 (H.264), quadro a quadro, sem perder frames.

Usa browser_session.MotionBrowser (relógio virtual) e envia os quadros JPEG por pipe ao ffmpeg.
A duração padrão é uma volta completa da linha do tempo mestre (window.__tl.duration()).

Uso:
  python render_mp4.py <motion.html> [--out video.mp4] [--fps 30] [--duration S] [--deps DIR] [--crf 16]
"""
from __future__ import annotations

import argparse
import asyncio
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from browser_session import MotionBrowser  # noqa: E402


class FfmpegWriter:
    """Recebe quadros JPEG um a um e os codifica em H.264 (o ffmpeg lê os quadros pela entrada padrão)."""

    def __init__(self, out: Path, fps: int, crf: int):
        if not shutil.which("ffmpeg"):
            sys.exit("[render] ffmpeg não encontrado no PATH")
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-",
               "-c:v", "libx264", "-preset", "slow", "-crf", str(crf), "-pix_fmt", "yuv420p", "-movflags", "+faststart",
               str(out)]
        self._proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        self._stdin = self._proc.stdin  # canal por onde os quadros entram no ffmpeg

    def write(self, frame: bytes) -> None:
        self._stdin.write(frame)

    def close(self) -> int:
        """Fecha a entrada, espera o ffmpeg terminar e devolve o código de saída (0 = sucesso)."""
        self._stdin.close()
        return self._proc.wait()


@dataclass(frozen=True)
class RenderSettings:
    """Parâmetros do vídeo agrupados num só objeto (fps, qualidade, duração e fonte a validar)."""

    fps: int = 30
    crf: int = 16
    duration: float | None = None  # None = uma volta da linha do tempo
    font: str | None = None        # família que precisa ter carregado antes de renderizar


class Mp4Renderer:
    """Avança o relógio virtual 1/fps por vez, captura cada quadro e o entrega ao FfmpegWriter."""

    def __init__(self, html: Path, out: Path, settings: RenderSettings, deps: Path | None = None):
        self.html, self.out, self.s, self.deps = html, out, settings, deps

    async def render(self) -> None:
        s = self.s
        async with MotionBrowser(self.html, self.deps) as mp:
            total = s.duration or await mp.duration()
            frames = round(total * s.fps)
            if s.font and not await mp.fonts_ok(s.font):
                print(f"[render] aviso: fonte '{s.font}' não carregou; rode prepare_deps.py e passe --deps")
            writer = FfmpegWriter(self.out, s.fps, s.crf)
            try:
                for i in range(frames):
                    if i:
                        await mp.step(1000 / s.fps)
                    writer.write(await mp.frame("jpeg", 95))
                    if i % (s.fps * 5) == 0:
                        print(f"[render] quadro {i}/{frames}  t={await mp.time():.2f}s", flush=True)
            finally:
                code = writer.close()
            if mp.errors:
                print(f"[render] erros na página: {mp.errors}")
            size = mp.size
        if code != 0:
            sys.exit("[render] ffmpeg falhou")
        print(f"[render] OK -> {self.out} ({self.out.stat().st_size / 1e6:.1f} MB, {frames} quadros, "
              f"{s.fps} fps, {size[0]}x{size[1]})")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--duration", type=float, help="segundos (padrão: uma volta da linha do tempo)")
    ap.add_argument("--deps", type=Path, help="diretório do prepare_deps.py (GSAP e fontes locais)")
    ap.add_argument("--crf", type=int, default=16, help="qualidade H.264 (menor = melhor; 16-20 recomendado)")
    ap.add_argument("--check-font", default="Inter Tight", help="família a validar antes de renderizar ('' desliga)")
    a = ap.parse_args()
    out = a.out or a.html.with_suffix(".mp4")
    settings = RenderSettings(a.fps, a.crf, a.duration, a.check_font or None)
    renderer = Mp4Renderer(a.html, out, settings, a.deps)
    asyncio.run(renderer.render())


if __name__ == "__main__":
    main()
