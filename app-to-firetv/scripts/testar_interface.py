#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
testar_interface.py: testa o assets/index.html como se fosse a Fire TV, antes de empacotar.

Abre a página no Chromium (Playwright) nas viewports que a Fire TV expõe ao WebView,
simula o controle remoto chamando window.fireTvKey e confere, a cada passo:
  - nenhum erro de JavaScript (pageerror ou console.error);
  - o palco (#stage) inteiro dentro da tela;
  - exatamente um elemento em foco (.focus);
  - a retomada do estado depois de recarregar a página.
As capturas de tela ficam na pasta de saída para o agente abrir e conferir.

Uso:
  python testar_interface.py --html proj/assets/index.html --saida shots \
         --roteiro DOWN,RIGHT,SELECT,MENU,DOWN,BACK,BACK
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ConfigTeste:
    """O que testar: arquivo HTML, pasta das capturas e a sequência de teclas do controle."""
    html: Path
    saida: Path
    roteiro: list
    viewports: list = field(default_factory=lambda: [(960, 540, 2), (1280, 720, 1)])

    def url(self) -> str:
        # Endereço file:// do HTML, igual ao que o WebView da Fire TV abre
        return self.html.resolve().as_uri()


class InspetorDePagina:
    """Faz as conferências automáticas numa página já carregada."""

    def __init__(self, pagina):
        self.pagina = pagina

    def fire_tv_key_definido(self) -> bool:
        return self.pagina.evaluate("typeof window.fireTvKey === 'function'")

    def palco_dentro_da_tela(self) -> bool:
        return self.pagina.evaluate("""() => {
            const s = document.getElementById('stage'); if (!s) return false;
            const r = s.getBoundingClientRect();
            return r.left >= -1 && r.top >= -1 && r.right <= innerWidth + 1 && r.bottom <= innerHeight + 1;
        }""")

    def focos(self) -> int:
        return self.pagina.evaluate("document.querySelectorAll('.focus').length")


class TesteInterface:
    """Roda o roteiro de teclas em cada viewport e monta o relatório."""

    def __init__(self, config: ConfigTeste):
        self.config = config
        self.saida = config.saida
        self.url = config.url()
        self.saida.mkdir(parents=True, exist_ok=True)

    def executar(self) -> dict:
        from playwright.sync_api import sync_playwright  # import aqui: só este script precisa do Playwright
        relatorio = {"viewports": [], "capturas": []}
        with sync_playwright() as p:
            navegador = p.chromium.launch()
            for largura, altura, escala in self.config.viewports:
                relatorio["viewports"].append(self._testar_viewport(navegador, (largura, altura, escala), relatorio["capturas"]))
            navegador.close()
        relatorio["success"] = all(v["ok"] for v in relatorio["viewports"])
        return relatorio

    def _testar_viewport(self, navegador, viewport, capturas) -> dict:
        largura, altura, escala = viewport
        contexto = navegador.new_context(viewport={"width": largura, "height": altura}, device_scale_factor=escala)
        pagina = contexto.new_page()
        erros = []
        pagina.on("pageerror", lambda e: erros.append(f"pageerror: {e}"))
        pagina.on("console", lambda m: erros.append(f"console: {m.text}") if m.type == "error" else None)
        pagina.goto(self.url)
        pagina.wait_for_timeout(300)
        inspetor = InspetorDePagina(pagina)
        prefixo = f"{largura}x{altura}"
        passos = [self._registrar(pagina, inspetor, f"{prefixo}_00_inicial", capturas)]
        passos[0]["fireTvKey_definido"] = inspetor.fire_tv_key_definido()
        for i, tecla in enumerate(self.config.roteiro, start=1):
            pagina.evaluate("a => window.fireTvKey && window.fireTvKey(a)", tecla)
            pagina.wait_for_timeout(280)  # animações da TV duram até 250 ms
            passos.append(self._registrar(pagina, inspetor, f"{prefixo}_{i:02d}_{tecla.lower()}", capturas))
        pagina.reload()
        pagina.wait_for_timeout(400)
        passos.append(self._registrar(pagina, inspetor, f"{prefixo}_99_retomada", capturas))
        contexto.close()
        ok = (not erros and passos[0]["fireTvKey_definido"]
              and all(p["palco_ok"] and p["focos"] == 1 for p in passos))
        return {"viewport": prefixo, "ok": ok, "erros": erros, "passos": passos}

    def _registrar(self, pagina, inspetor, nome, capturas) -> dict:
        arquivo = self.saida / f"{nome}.png"
        pagina.screenshot(path=str(arquivo))
        capturas.append(str(arquivo))
        return {"passo": nome, "palco_ok": inspetor.palco_dentro_da_tela(), "focos": inspetor.focos()}


class Cli:
    """Lê os argumentos, roda o teste e imprime o relatório em JSON."""

    @staticmethod
    def executar(argv=None):
        p = argparse.ArgumentParser(description="Teste da interface de TV com Playwright")
        p.add_argument("--html", required=True)
        p.add_argument("--saida", required=True)
        p.add_argument("--roteiro", default="DOWN,RIGHT,SELECT,MENU,DOWN,BACK,BACK")
        a = p.parse_args(argv)
        config = ConfigTeste(html=Path(a.html), saida=Path(a.saida),
                             roteiro=[t.strip().upper() for t in a.roteiro.split(",") if t.strip()])
        relatorio = TesteInterface(config).executar()
        print(json.dumps(relatorio, indent=2, ensure_ascii=False))
        if not relatorio["success"]:
            sys.exit(1)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    Cli.executar()
