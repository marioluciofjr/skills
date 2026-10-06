#!/usr/bin/env python3
"""preview_frames.py — captura quadros do HTML em instantes escolhidos e monta uma grade de revisão.

Avança o relógio virtual de forma contínua (como no vídeo final), então echo trails, partículas e
contadores aparecem exatamente como no MP4. Use antes de renderizar para revisar cada cena.

Uso:
  python preview_frames.py <motion.html> --times 1.9 5.6 10.4 [--out preview/] [--deps DIR]
  python preview_frames.py <motion.html> --every 2.5            (um quadro a cada 2,5 s)
"""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from browser_session import MotionBrowser  # noqa: E402
from contact_sheet import ContactSheet  # noqa: E402


class FramePreviewer:
    """Captura quadros pontuais com o relógio virtual e monta a grade sheet.png na pasta de saída."""

    TICK_MS = 1000 / 60  # passo do relógio entre capturas (60 Hz, igual a um monitor comum)

    def __init__(self, html: Path, out: Path, deps: Path | None = None, sheet: ContactSheet | None = None):
        self.html, self.out, self.deps = html, out, deps
        self.sheet = sheet or ContactSheet()

    @staticmethod
    def spread(total: float, every: float) -> list[float]:
        """Instantes no meio de cada janela de `every` segundos (ex.: 1,25; 3,75; 6,25 para every=2,5)."""
        return [round(every * (i + 1) - every / 2, 2) for i in range(int(total // every))]

    async def capture(self, times: list[float] | None = None, every: float = 2.5) -> Path:
        self.out.mkdir(parents=True, exist_ok=True)
        paths: list[Path] = []
        async with MotionBrowser(self.html, self.deps) as mp:
            times = sorted(times or self.spread(await mp.duration(), every))
            now = 0.0
            for t in times:
                # o tempo só anda para a frente, em passos pequenos, para os efeitos rodarem como no vídeo
                while now + self.TICK_MS / 1000 <= t:
                    await mp.step(self.TICK_MS)
                    now += self.TICK_MS / 1000
                p = self.out / f"f_{t:06.2f}.png"
                p.write_bytes(await mp.frame("png"))
                paths.append(p)
            if mp.errors:
                print(f"[preview] erros na página: {mp.errors}")
        sheet = self.sheet.make(paths, self.out / "sheet.png", labels=[f"{t:.1f}s" for t in times])
        print(f"[preview] {len(paths)} quadros em {self.out} | grade: {sheet}")
        return sheet


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html", type=Path)
    ap.add_argument("--times", nargs="*", type=float)
    ap.add_argument("--every", type=float, default=2.5)
    ap.add_argument("--out", type=Path, default=Path("preview"))
    ap.add_argument("--deps", type=Path)
    a = ap.parse_args()
    asyncio.run(FramePreviewer(a.html, a.out, a.deps).capture(a.times, a.every))


if __name__ == "__main__":
    main()
