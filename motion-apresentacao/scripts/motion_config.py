"""motion_config.py — carrega, completa com padrões e valida o config.json de um projeto de motion.

Única fonte de verdade do esquema de configuração. Usado por build_motion.py e prepare_deps.py.

Uso em código:
  cfg = MotionConfig.load("pasta-do-projeto")     # dicionário completo e validado
  MotionConfig.font_families(cfg)                 # [(família, pesos)] para baixar ou pedir ao Google Fonts
"""
from __future__ import annotations

import copy
import json
import struct
from pathlib import Path


class ConfigError(ValueError):
    """Erro de configuração com mensagem pronta para o usuário."""


class PngHeader:
    """Lê largura e altura direto do cabeçalho de um PNG, sem depender do Pillow.

    O PNG guarda o tamanho nos bytes 16 a 24 (bloco IHDR); ler só isso é rápido e não exige bibliotecas.
    """

    SIGNATURE = b"\x89PNG\r\n\x1a\n"

    @classmethod
    def size(cls, path: Path) -> tuple[int, int]:
        with open(path, "rb") as fh:
            head = fh.read(24)
        if head[:8] != cls.SIGNATURE:
            raise ConfigError(f"O logo precisa ser PNG (gere com extract_logo.py): {path}")
        return struct.unpack(">II", head[16:24])


class MotionConfig:
    """Esquema do config.json: padrões, mescla com o arquivo do projeto e validação.

    Todos os métodos são de classe porque o esquema é único; não há estado por instância a guardar.
    """

    DEFAULTS: dict = {
        "title": "Apresentação em motion",
        "lang": "pt-BR",
        "locale": "pt-BR",
        "width": 1920,
        "height": 1080,
        "loop": True,
        "gsap_version": "3.12.5",
        "theme": {
            "bg": "#000000", "fg": "#ffffff",
            "g1": "#9a9a9a", "g2": "#5c5c5c", "g3": "#262626", "g4": "#141414", "g5": "#0a0a0a",
        },
        "fonts": {
            "display": {"family": "Inter Tight", "weights": [400, 500, 600, 700, 800]},
            "mono": {"family": "JetBrains Mono", "weights": [400, 500]},
        },
        "brand": {},
        "chrome": None,
    }
    REQUIRED_PROJECT_FILES = ("config.json", "scenes.html", "scenes.js")
    LOGO_META_KEYS = ("aspect", "mark_end", "word_start")

    @classmethod
    def load(cls, project_dir: str | Path) -> dict:
        """Devolve o config completo; caminhos do logo resolvidos e metadados do logo.json mesclados."""
        root = Path(project_dir)
        cls._require_files(root)
        cfg = cls._merge(cls.DEFAULTS, json.loads((root / "config.json").read_text(encoding="utf-8")))
        cfg["brand"] = cls._resolve_brand(root, cfg.get("brand") or {})
        cls._validate_chrome(cfg.get("chrome"))
        return cfg

    @staticmethod
    def font_families(cfg: dict) -> list[tuple[str, list[int]]]:
        """[(família, pesos)] sem duplicatas, na ordem display -> mono -> demais."""
        seen, out = set(), []
        for spec in cfg.get("fonts", {}).values():
            fam = spec.get("family")
            if fam and fam not in seen:
                seen.add(fam)
                out.append((fam, sorted(set(spec.get("weights", [400])))))
        return out

    # ------------------------------------------------------------ etapas internas do carregamento
    @classmethod
    def _require_files(cls, root: Path) -> None:
        missing = [f for f in cls.REQUIRED_PROJECT_FILES if not (root / f).exists()]
        if missing:
            raise ConfigError(f"Arquivos ausentes em {root}: {', '.join(missing)}")

    @classmethod
    def _merge(cls, base: dict, override: dict) -> dict:
        """Mescla recursiva: o que o projeto define vence; o que ele omite vem dos padrões."""
        out = copy.deepcopy(base)
        for key, value in (override or {}).items():
            if isinstance(value, dict) and isinstance(out.get(key), dict):
                out[key] = cls._merge(out[key], value)
            else:
                out[key] = value
        return out

    @classmethod
    def _resolve_brand(cls, root: Path, brand: dict) -> dict:
        """Completa a marca com os metadados do logo.json (ou com valores seguros, se ele faltar)."""
        logo = brand.get("logo")
        if not logo:
            return brand
        logo_path = (root / logo).resolve()
        if not logo_path.exists():
            raise ConfigError(f"Logo não encontrado: {logo_path}")
        meta_path = logo_path.with_suffix(".json")
        meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
        for key in cls.LOGO_META_KEYS:
            if brand.get(key) is None:
                brand[key] = meta.get(key)
        if not brand.get("aspect"):
            w, h = PngHeader.size(logo_path)
            brand["aspect"] = round(w / h, 4)
        for key in ("mark_end", "word_start"):
            if brand.get(key) is None:
                brand[key] = 1  # sem vão detectado: o logo inteiro é tratado como símbolo
        brand["_logo_path"] = str(logo_path)
        return brand

    @staticmethod
    def _validate_chrome(chrome: dict | None) -> None:
        if chrome is not None and not isinstance(chrome.get("sections", []), list):
            raise ConfigError("chrome.sections deve ser uma lista de rótulos das seções")
