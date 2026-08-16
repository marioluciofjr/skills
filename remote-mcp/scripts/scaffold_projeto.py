#!/usr/bin/env python3
"""Gera a estrutura de base de um MCP remoto (FastMCP + Streamable HTTP + Vercel).

Uso:
    python scaffold_projeto.py especificacao.json /caminho/destino

O arquivo de especificação é um JSON com este formato:
{
    "nome_pasta": "mcp-exemplo",
    "nome_servidor": "Exemplo-Tema",
    "usa_httpx": true,
    "autor": "Nome da pessoa usuária",
    "ano": 2026,
    "tools": [
        {"nome": "exemplo_listar_algo", "descricao": "Lista algo do tema.", "somente_leitura": true, "destrutiva": false}
    ]
}

Este script só gera o esqueleto (pastas, requirements.txt, LICENSE, .gitignore,
server.py com as tools em branco). A lógica de cada tool é escrita depois,
por quem estiver conduzindo o pipeline da skill — o script não tenta adivinhar
como buscar o dado de cada tema.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class EspecificacaoTool:
    """Descreve uma tool do MCP: nome, o que faz, e as anotações de comportamento."""

    nome: str
    descricao: str
    somente_leitura: bool = True
    destrutiva: bool = False

    @property
    def idempotente(self) -> bool:
        """Uma tool só de leitura é sempre idempotente: repetir a chamada não muda nada."""
        return self.somente_leitura or not self.destrutiva


@dataclass
class EspecificacaoProjeto:
    """Reúne tudo que o scaffold precisa saber sobre o projeto a gerar."""

    nome_pasta: str
    nome_servidor: str
    autor: str
    ano: int
    usa_httpx: bool = False
    tools: list[EspecificacaoTool] = field(default_factory=list)

    @staticmethod
    def a_partir_de_json(caminho: Path) -> "EspecificacaoProjeto":
        """Lê o arquivo de especificação em JSON e monta o objeto correspondente."""
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        tools = [EspecificacaoTool(**item) for item in dados.get("tools", [])]
        return EspecificacaoProjeto(
            nome_pasta=dados["nome_pasta"],
            nome_servidor=dados["nome_servidor"],
            autor=dados.get("autor", "[a preencher]"),
            ano=dados.get("ano", 2026),
            usa_httpx=dados.get("usa_httpx", False),
            tools=tools,
        )


class GeradorRequirements:
    """Gera o conteúdo de requirements.txt, com teto de versão maior em cada lib."""

    def gerar(self, spec: EspecificacaoProjeto) -> str:
        linhas = [
            "fastmcp>=3.4.0,<4.0.0",
            "starlette>=0.37.0",
            "uvicorn>=0.29.0",
        ]
        if spec.usa_httpx:
            linhas.append("httpx>=0.27.0")
        return "\n".join(linhas) + "\n"


class GeradorLicenca:
    """Gera o texto da licença MIT, com o autor e o ano informados na especificação."""

    def gerar(self, spec: EspecificacaoProjeto) -> str:
        return (
            "MIT License\n\n"
            f"Copyright (c) {spec.ano} {spec.autor}\n\n"
            'Permission is hereby granted, free of charge, to any person obtaining a copy\n'
            'of this software and associated documentation files (the "Software"), to deal\n'
            "in the Software without restriction, including without limitation the rights\n"
            "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
            "copies of the Software, and to permit persons to whom the Software is\n"
            "furnished to do so, subject to the following conditions:\n\n"
            "The above copyright notice and this permission notice shall be included in all\n"
            "copies or substantial portions of the Software.\n\n"
            'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n'
            "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
            "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
            "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
            "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
            "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
            "SOFTWARE.\n"
        )


class GeradorGitignore:
    """Gera o .gitignore padrão de um projeto Python simples."""

    def gerar(self, spec: EspecificacaoProjeto) -> str:
        return "__pycache__/\n*.pyc\n.venv/\nvenv/\n.env\n"


class GeradorServidor:
    """Gera o esqueleto de server.py: FastMCP, Streamable HTTP, CORS e um stub por tool.

    A lógica de cada tool fica marcada com um TODO — este gerador não sabe buscar
    dado de nenhuma fonte específica, só monta a estrutura obrigatória do arquivo.
    """

    def gerar(self, spec: EspecificacaoProjeto) -> str:
        imports = self._montar_imports(spec)
        tools = "\n\n".join(self._montar_tool(tool) for tool in spec.tools) or self._montar_tool_exemplo()
        return (
            f"{imports}\n\n"
            f'# Cria o servidor MCP\n'
            f'mcp = FastMCP("{spec.nome_servidor}")\n\n'
            f"{tools}\n\n"
            f"{self._montar_app()}\n\n"
            f"{self._montar_main()}\n"
        )

    def _montar_imports(self, spec: EspecificacaoProjeto) -> str:
        linhas = ["from fastmcp import FastMCP", "from mcp.types import ToolAnnotations"]
        if spec.usa_httpx:
            linhas.append("import httpx")
        linhas.extend(
            [
                "from starlette.middleware import Middleware",
                "from starlette.middleware.cors import CORSMiddleware",
            ]
        )
        return "\n".join(linhas)

    def _montar_tool(self, tool: EspecificacaoTool) -> str:
        return (
            "@mcp.tool(\n"
            f'    name="{tool.nome}",\n'
            "    annotations=ToolAnnotations(\n"
            f'        title="{tool.descricao}",\n'
            f"        readOnlyHint={tool.somente_leitura},\n"
            f"        destructiveHint={tool.destrutiva},\n"
            f"        idempotentHint={tool.idempotente},\n"
            f"        openWorldHint={str(True)},\n"
            "    ),\n"
            ")\n"
            f"async def {tool.nome}() -> str:\n"
            f'    """{tool.descricao}\n\n'
            "    TODO: implementar a lógica desta tool — buscar o dado na fonte definida\n"
            "    na etapa 2 do pipeline, tratar erro e devolver o texto formatado.\n"
            '    """\n'
            '    raise NotImplementedError("Implemente esta tool antes de publicar.")'
        )

    def _montar_tool_exemplo(self) -> str:
        return (
            "@mcp.tool(\n"
            '    name="tema_exemplo",\n'
            "    annotations=ToolAnnotations(\n"
            '        title="Tool de exemplo",\n'
            "        readOnlyHint=True,\n"
            "        destructiveHint=False,\n"
            "        idempotentHint=True,\n"
            "        openWorldHint=True,\n"
            "    ),\n"
            ")\n"
            "async def tema_exemplo() -> str:\n"
            '    """TODO: substitua por uma tool real, definida na ficha de aprovação."""\n'
            '    raise NotImplementedError("Nenhuma tool foi definida na especificação.")'
        )

    def _montar_app(self) -> str:
        return (
            "# Cria a aplicação ASGI em Streamable HTTP, no caminho /mcp, com CORS\n"
            "# liberado para clientes remotos e modo stateless para rodar em serverless\n"
            "app = mcp.http_app(\n"
            '    path="/mcp",\n'
            "    stateless_http=True,\n"
            "    middleware=[\n"
            "        Middleware(\n"
            "            CORSMiddleware,\n"
            '            allow_origins=["*"],\n'
            '            allow_methods=["GET", "POST", "DELETE", "OPTIONS"],\n'
            '            allow_headers=["*"],\n'
            '            expose_headers=["mcp-session-id"],\n'
            "        )\n"
            "    ],\n"
            ")"
        )

    def _montar_main(self) -> str:
        return (
            'if __name__ == "__main__":\n'
            "    import os\n"
            "    import uvicorn\n\n"
            '    porta = int(os.environ.get("PORT", 8000))\n'
            '    uvicorn.run(app, host="0.0.0.0", port=porta)'
        )


class ScaffolderProjeto:
    """Orquestra os geradores para escrever a estrutura completa do projeto em disco."""

    def __init__(self) -> None:
        self._gerador_requirements = GeradorRequirements()
        self._gerador_licenca = GeradorLicenca()
        self._gerador_gitignore = GeradorGitignore()
        self._gerador_servidor = GeradorServidor()

    def gerar(self, spec: EspecificacaoProjeto, destino: Path) -> Path:
        """Cria a pasta do projeto e escreve os 4 arquivos de base. Devolve o caminho da pasta."""
        pasta_projeto = destino / spec.nome_pasta
        pasta_projeto.mkdir(parents=True, exist_ok=True)

        (pasta_projeto / "requirements.txt").write_text(
            self._gerador_requirements.gerar(spec), encoding="utf-8"
        )
        (pasta_projeto / "LICENSE").write_text(self._gerador_licenca.gerar(spec), encoding="utf-8")
        (pasta_projeto / ".gitignore").write_text(self._gerador_gitignore.gerar(spec), encoding="utf-8")
        (pasta_projeto / "server.py").write_text(self._gerador_servidor.gerar(spec), encoding="utf-8")

        return pasta_projeto


def main() -> None:
    if len(sys.argv) != 3:
        print("Uso: python scaffold_projeto.py especificacao.json /caminho/destino")
        raise SystemExit(1)

    caminho_especificacao = Path(sys.argv[1])
    destino = Path(sys.argv[2])

    spec = EspecificacaoProjeto.a_partir_de_json(caminho_especificacao)
    pasta_gerada = ScaffolderProjeto().gerar(spec, destino)

    print(f"Projeto gerado em: {pasta_gerada}")
    print("Próximo passo: implementar a lógica de cada tool em server.py (marcada com TODO).")


if __name__ == "__main__":
    main()
