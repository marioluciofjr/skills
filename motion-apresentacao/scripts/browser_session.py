"""browser_session.py — abre o HTML do motion num Chromium headless com relógio virtual.

Responsabilidade única: entregar uma página pronta e determinística para quem captura quadros
(render_mp4.py, preview_frames.py). Não sabe nada de vídeo nem de contact sheet.

Relógio virtual: performance.now, Date.now e requestAnimationFrame são substituídos antes de qualquer
script rodar; o tempo só avança quando step(ms) é chamado. Assim cada quadro cai exatamente no seu
instante, inclusive os tweens independentes do echo trail e o canvas de partículas.

Rede: se houver deps (prepare_deps.py), GSAP e Google Fonts são servidos localmente; caso contrário a
página tenta a internet normalmente.
"""
from __future__ import annotations

from pathlib import Path

VIRTUAL_CLOCK_JS = """
(() => {
  let vt = 0; const q = []; let id = 0;
  const base = Date.now();
  performance.now = () => vt;
  Date.now = () => base + vt;
  window.requestAnimationFrame = cb => { q.push([++id, cb]); return id; };
  window.cancelAnimationFrame = i => { const k = q.findIndex(x => x[0] === i); if (k >= 0) q.splice(k, 1); };
  window.__step = ms => {
    const sub = 4;
    for (let s = 0; s < sub; s++) { vt += ms / sub; q.splice(0).forEach(([, cb]) => cb(vt)); }
  };
})();
"""


class MotionPage:
    """Fachada mínima sobre a página: avançar tempo, ler tempo/duração, capturar quadro."""

    def __init__(self, page):
        self.page = page
        self.errors: list[str] = []
        self.size = (1920, 1080)
        page.on("pageerror", lambda e: self.errors.append(str(e)))

    async def step(self, ms: float) -> None:
        await self.page.evaluate(f"window.__step({ms}); 0")  # '; 0' evita serializar objetos do gsap

    async def time(self) -> float:
        return await self.page.evaluate("window.__tl.time()")

    async def duration(self) -> float:
        return await self.page.evaluate("window.__tl.duration()")

    async def frame(self, fmt: str = "jpeg", quality: int = 95) -> bytes:
        if fmt == "png":
            return await self.page.screenshot(type="png")
        return await self.page.screenshot(type="jpeg", quality=quality)

    async def fonts_ok(self, family: str) -> bool:
        return await self.page.evaluate(f"document.fonts.check('700 40px \"{family}\"')")


class LocalDeps:
    """GSAP e fontes baixados pelo prepare_deps.py, servidos no lugar das CDNs (que podem estar bloqueadas)."""

    def __init__(self, deps: str | Path | None):
        root = Path(deps).expanduser() if deps else None
        self.gsap_js = self._read(root, "gsap.min.js")
        self.fonts_css = self._read(root, "fonts.css")

    @staticmethod
    def _read(root: Path | None, name: str) -> str | None:
        return (root / name).read_text(encoding="utf-8") if root and (root / name).exists() else None

    async def route(self, r) -> None:
        """Intercepta cada requisição da página: responde com o arquivo local quando houver um."""
        url = r.request.url
        if self.gsap_js and "gsap" in url and url.endswith(".js"):
            await r.fulfill(body=self.gsap_js, content_type="application/javascript")
        elif self.fonts_css and "fonts.googleapis.com" in url:
            await r.fulfill(body=self.fonts_css, content_type="text/css")
        elif self.fonts_css and "fonts.gstatic.com" in url:
            await r.fulfill(status=404, body="")  # as fontes já vêm embutidas no fonts.css
        else:
            await r.continue_()


class MotionBrowser:
    """Abre o HTML num Chromium headless e entrega um MotionPage em t=0, pausado no relógio virtual.

    Uso:  async with MotionBrowser(html, deps) as mp: ...
    O viewport segue MOTION_CONFIG.width/height, então cada quadro sai no tamanho nativo do palco.
    """

    START_TIMEOUT_MS = 20000

    def __init__(self, html: str | Path, deps: str | Path | None = None):
        self.html = Path(html).resolve()
        self.deps = LocalDeps(deps)
        self._pw_ctx = None
        self._browser = None

    async def __aenter__(self) -> MotionPage:
        from playwright.async_api import async_playwright

        self._pw_ctx = async_playwright()
        pw = await self._pw_ctx.__aenter__()
        try:
            self._browser = await pw.chromium.launch()
            return await self._open_page()
        except BaseException:
            await self.__aexit__(None, None, None)
            raise

    async def __aexit__(self, *exc) -> None:
        if self._browser:
            await self._browser.close()
        if self._pw_ctx:
            await self._pw_ctx.__aexit__(None, None, None)

    async def _open_page(self) -> MotionPage:
        page = await self._browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        await page.add_init_script(VIRTUAL_CLOCK_JS)
        await page.route("**/*", self.deps.route)
        mp = MotionPage(page)
        await page.goto(self.html.as_uri())
        try:
            await page.wait_for_function("window.__tl && !window.__tl.paused()", polling=100, timeout=self.START_TIMEOUT_MS)
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(
                "O motion não iniciou. Verifique se o GSAP carregou (rode prepare_deps.py e passe --deps) "
                f"e os erros da página: {mp.errors}") from exc
        dims = await page.evaluate("[(window.MOTION_CONFIG||{}).width||1920, (window.MOTION_CONFIG||{}).height||1080]")
        await page.set_viewport_size({"width": dims[0], "height": dims[1]})
        mp.size = (dims[0], dims[1])
        await page.evaluate("window.dispatchEvent(new Event('resize')); window.__tl.play(0); window.__step(1); 0")
        return mp
