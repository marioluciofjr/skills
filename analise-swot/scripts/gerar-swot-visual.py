"""
gerar-swot-visual.py
Script para gerar uma interface visual animada da Análise SWOT em quadrantes.

Uso:
    python gerar-swot-visual.py [caminho_para_analise_swot.md]

Se nenhum arquivo for fornecido, abre a interface com dados de exemplo.
O resultado é salvo como 'swot_visual.html' na pasta atual.
"""

import sys
import re
import os
import json
import webbrowser
from pathlib import Path
from datetime import datetime


# ──────────────────────────────────────────────
# Parser do arquivo de análise SWOT em markdown
# ──────────────────────────────────────────────

def parse_swot_markdown(filepath: str) -> dict:
    """Lê o arquivo analise-swot.md e extrai os dados por quadrante."""
    data = {
        "title": "Análise SWOT",
        "date": datetime.now().strftime("%d/%m/%Y"),
        "strengths": [],
        "weaknesses": [],
        "opportunities": [],
        "threats": [],
        "next_steps": []
    }

    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"⚠️  Arquivo não encontrado: {filepath}. Usando dados de exemplo.")
        return get_example_data()

    # Detecta nome do projeto no título (linha # ...)
    title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
    if title_match:
        data["title"] = title_match.group(1).strip()

    # Função auxiliar para extrair itens de uma seção
    def extract_section(section_pattern: str) -> list:
        match = re.search(section_pattern, content, re.IGNORECASE | re.DOTALL)
        if not match:
            return []
        section_text = match.group(1)
        items = []
        for line in section_text.split('\n'):
            line = line.strip()
            # Aceita linhas que comecem com número, -, *, ou marcação de lista
            if re.match(r'^[\d\-\*•]\.*\s+', line) or re.match(r'^\d+\.', line):
                # Remove numeração e marcadores
                clean = re.sub(r'^[\d\-\*•\[\]x \.]+', '', line).strip()
                # Remove marcação de checkbox [ ] ou [x]
                clean = re.sub(r'^\[[ x]\]\s*', '', clean).strip()
                if clean and not clean.startswith('*') and len(clean) > 3:
                    # Extrai título e descrição separados por " — " ou " - "
                    parts = re.split(r'\s+[—–-]\s+', clean, maxsplit=1)
                    if len(parts) == 2:
                        items.append({"title": parts[0].strip(), "desc": parts[1].strip()})
                    else:
                        items.append({"title": clean, "desc": ""})
        return items

    # Padroniza seções aceitando emojis e variações
    sections = {
        "strengths":     r'##\s*[🔵💪]?\s*[Ff]or[çc]as?.*?\n(.*?)(?=\n##|\Z)',
        "weaknesses":    r'##\s*[🔴⚠️]?\s*[Ff]raquezas?.*?\n(.*?)(?=\n##|\Z)',
        "opportunities": r'##\s*[🟢🚀]?\s*[Oo]portunidades?.*?\n(.*?)(?=\n##|\Z)',
        "threats":       r'##\s*[🟠⚡]?\s*[Aa]mea[çc]as?.*?\n(.*?)(?=\n##|\Z)',
        "next_steps":    r'##\s*[✅]?\s*[Pp]r[oó]ximos?\s+[Pp]assos?.*?\n(.*?)(?=\n##|\Z)',
    }

    for key, pattern in sections.items():
        extracted = extract_section(pattern)
        if extracted:
            data[key] = extracted

    # Se os quadrantes estão vazios, usa dados de exemplo
    total = sum(len(data[k]) for k in ["strengths", "weaknesses", "opportunities", "threats"])
    if total == 0:
        print("⚠️  Nenhum dado encontrado no arquivo. Usando dados de exemplo.")
        return get_example_data()

    return data


def get_example_data() -> dict:
    """Retorna dados de exemplo para demonstração da interface."""
    return {
        "title": "Exemplo de Análise SWOT — Startup de Tecnologia",
        "date": datetime.now().strftime("%d/%m/%Y"),
        "strengths": [
            {"title": "Equipe técnica especializada", "desc": "Time com expertise em IA e desenvolvimento ágil"},
            {"title": "Produto inovador com IP próprio", "desc": "Tecnologia patenteada que diferencia no mercado"},
            {"title": "Cultura organizacional forte", "desc": "Baixa rotatividade e alta satisfação interna"},
            {"title": "Base de clientes fidelizados", "desc": "NPS acima de 70 com contratos de longo prazo"},
        ],
        "weaknesses": [
            {"title": "Capital de giro limitado", "desc": "Runway de apenas 8 meses sem novo aporte"},
            {"title": "Dependência de um cliente chave", "desc": "40% da receita concentrada em um único contrato"},
            {"title": "Ausência de time de vendas estruturado", "desc": "Crescimento limitado pela capacidade de aquisição"},
            {"title": "Processos manuais na operação", "desc": "Escalabilidade comprometida sem automação"},
        ],
        "opportunities": [
            {"title": "Mercado de IA em expansão acelerada", "desc": "Crescimento projetado de 38% ao ano até 2027"},
            {"title": "Editais de fomento à inovação abertos", "desc": "BNDES e Finep com chamadas para o setor"},
            {"title": "Lacuna de concorrentes especializados", "desc": "Principais players são generalistas sem foco no nicho"},
            {"title": "Adoção crescente B2B no setor", "desc": "Empresas do segmento aumentando budget de tecnologia"},
        ],
        "threats": [
            {"title": "Grandes players entrando no nicho", "desc": "Google e Microsoft com produtos adjacentes em beta"},
            {"title": "Escassez e guerra por talentos tech", "desc": "Salários aquecidos aumentando custo de contratação"},
            {"title": "Incerteza regulatória em IA", "desc": "LGPD e regulamentações de IA em discussão no Congresso"},
            {"title": "Volatilidade cambial", "desc": "Custos de infraestrutura em USD pressionando margens"},
        ],
        "next_steps": [
            {"title": "Iniciar rodada de investimento Série A", "desc": "Meta: Q2/2025"},
            {"title": "Contratar head de vendas", "desc": "Prioridade máxima para Q1/2025"},
            {"title": "Diversificar base de clientes", "desc": "Reduzir concentração para abaixo de 25% em 12 meses"},
            {"title": "Mapear editais de fomento", "desc": "BNDES e Finep — prazo: fim do mês"},
            {"title": "Iniciar automação dos processos operacionais", "desc": "Reduzir trabalho manual em 60% até Q3"},
        ]
    }


# ──────────────────────────────────────────────
# Gerador de HTML Animado
# ──────────────────────────────────────────────

def generate_html(data: dict) -> str:
    """Gera o HTML completo com a interface animada de quadrantes SWOT."""

    def items_to_json(items):
        return json.dumps(items, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{data['title']}</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    :root {{
      --bg: #0d1117;
      --bg-card: #161b22;
      --bg-card-hover: #1c2128;
      --border: #30363d;
      --text: #e6edf3;
      --text-muted: #7d8590;
      --text-dim: #484f58;

      --blue:   #388bfd;
      --blue-bg: rgba(56, 139, 253, 0.08);
      --blue-border: rgba(56, 139, 253, 0.3);

      --red:    #f85149;
      --red-bg: rgba(248, 81, 73, 0.08);
      --red-border: rgba(248, 81, 73, 0.3);

      --green:  #3fb950;
      --green-bg: rgba(63, 185, 80, 0.08);
      --green-border: rgba(63, 185, 80, 0.3);

      --orange: #e3b341;
      --orange-bg: rgba(227, 179, 65, 0.08);
      --orange-border: rgba(227, 179, 65, 0.3);

      --purple: #bc8cff;
      --purple-bg: rgba(188, 140, 255, 0.08);
    }}

    body {{
      font-family: 'Inter', system-ui, sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      padding: 2rem 1.5rem 4rem;
    }}

    /* ── Header ── */
    .header {{
      text-align: center;
      margin-bottom: 3rem;
      animation: fadeDown 0.8s ease both;
    }}
    .header-badge {{
      display: inline-block;
      background: var(--purple-bg);
      border: 1px solid var(--purple);
      color: var(--purple);
      font-size: 0.72rem;
      font-weight: 600;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      padding: 0.3rem 0.9rem;
      border-radius: 100px;
      margin-bottom: 1rem;
    }}
    .header h1 {{
      font-size: clamp(1.6rem, 4vw, 2.5rem);
      font-weight: 800;
      letter-spacing: -0.03em;
      color: var(--text);
      line-height: 1.2;
      margin-bottom: 0.5rem;
    }}
    .header .date {{
      color: var(--text-muted);
      font-size: 0.85rem;
    }}

    /* ── SWOT Grid ── */
    .swot-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.25rem;
      max-width: 1100px;
      margin: 0 auto 2rem;
    }}

    @media (max-width: 700px) {{
      .swot-grid {{ grid-template-columns: 1fr; }}
    }}

    /* ── Quadrant Card ── */
    .quadrant {{
      background: var(--bg-card);
      border-radius: 16px;
      border: 1px solid var(--border);
      padding: 1.5rem;
      position: relative;
      overflow: hidden;
      transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
      animation: fadeUp 0.7s ease both;
    }}
    .quadrant:hover {{
      transform: translateY(-4px);
      box-shadow: 0 12px 40px rgba(0,0,0,0.4);
    }}
    .quadrant::before {{
      content: '';
      position: absolute;
      top: 0; left: 0;
      width: 100%; height: 3px;
      border-radius: 16px 16px 0 0;
    }}

    .quadrant.strengths     {{ animation-delay: 0.1s; }}
    .quadrant.weaknesses    {{ animation-delay: 0.2s; }}
    .quadrant.opportunities {{ animation-delay: 0.3s; }}
    .quadrant.threats       {{ animation-delay: 0.4s; }}

    .quadrant.strengths::before     {{ background: linear-gradient(90deg, var(--blue), #58a6ff); }}
    .quadrant.weaknesses::before    {{ background: linear-gradient(90deg, var(--red), #ff6b6b); }}
    .quadrant.opportunities::before {{ background: linear-gradient(90deg, var(--green), #56d364); }}
    .quadrant.threats::before       {{ background: linear-gradient(90deg, var(--orange), #ffb74d); }}

    .quadrant.strengths:hover     {{ border-color: var(--blue-border); box-shadow: 0 12px 40px rgba(56,139,253,0.12); }}
    .quadrant.weaknesses:hover    {{ border-color: var(--red-border); box-shadow: 0 12px 40px rgba(248,81,73,0.12); }}
    .quadrant.opportunities:hover {{ border-color: var(--green-border); box-shadow: 0 12px 40px rgba(63,185,80,0.12); }}
    .quadrant.threats:hover       {{ border-color: var(--orange-border); box-shadow: 0 12px 40px rgba(227,179,65,0.12); }}

    .quadrant-header {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
      margin-bottom: 1.25rem;
    }}
    .quadrant-icon {{
      width: 40px; height: 40px;
      border-radius: 10px;
      display: flex; align-items: center; justify-content: center;
      font-size: 1.2rem;
      flex-shrink: 0;
    }}
    .strengths     .quadrant-icon {{ background: var(--blue-bg); }}
    .weaknesses    .quadrant-icon {{ background: var(--red-bg); }}
    .opportunities .quadrant-icon {{ background: var(--green-bg); }}
    .threats       .quadrant-icon {{ background: var(--orange-bg); }}

    .quadrant-label {{
      flex: 1;
    }}
    .quadrant-label h2 {{
      font-size: 1rem;
      font-weight: 700;
      letter-spacing: -0.02em;
    }}
    .strengths     .quadrant-label h2 {{ color: var(--blue); }}
    .weaknesses    .quadrant-label h2 {{ color: var(--red); }}
    .opportunities .quadrant-label h2 {{ color: var(--green); }}
    .threats       .quadrant-label h2 {{ color: var(--orange); }}

    .quadrant-label .subtitle {{
      font-size: 0.72rem;
      color: var(--text-muted);
      font-weight: 400;
      margin-top: 1px;
    }}

    .item-count {{
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 100px;
      font-size: 0.72rem;
      font-weight: 600;
      color: var(--text-muted);
      padding: 0.2rem 0.6rem;
    }}

    /* ── Items ── */
    .items-list {{ list-style: none; display: flex; flex-direction: column; gap: 0.6rem; }}

    .item {{
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 0.75rem 1rem;
      cursor: pointer;
      transition: all 0.25s ease;
      position: relative;
      overflow: hidden;
    }}
    .item::before {{
      content: '';
      position: absolute;
      left: 0; top: 0; bottom: 0;
      width: 3px;
      opacity: 0;
      transition: opacity 0.25s ease;
    }}
    .strengths     .item::before {{ background: var(--blue); }}
    .weaknesses    .item::before {{ background: var(--red); }}
    .opportunities .item::before {{ background: var(--green); }}
    .threats       .item::before {{ background: var(--orange); }}

    .item:hover {{ background: var(--bg-card-hover); border-color: transparent; }}
    .item:hover::before {{ opacity: 1; }}

    .item-title {{
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text);
      display: flex;
      align-items: flex-start;
      gap: 0.5rem;
    }}
    .item-title .dot {{
      width: 6px; height: 6px;
      border-radius: 50%;
      margin-top: 5px;
      flex-shrink: 0;
    }}
    .strengths     .dot {{ background: var(--blue); }}
    .weaknesses    .dot {{ background: var(--red); }}
    .opportunities .dot {{ background: var(--green); }}
    .threats       .dot {{ background: var(--orange); }}

    .item-desc {{
      font-size: 0.78rem;
      color: var(--text-muted);
      margin-top: 0.3rem;
      padding-left: 1.1rem;
      line-height: 1.5;
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.35s ease, opacity 0.25s ease;
      opacity: 0;
    }}
    .item.expanded .item-desc {{ max-height: 120px; opacity: 1; }}

    /* ── Next Steps ── */
    .next-steps-section {{
      max-width: 1100px;
      margin: 0 auto 2rem;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 1.5rem;
      animation: fadeUp 0.7s ease 0.5s both;
    }}
    .next-steps-section::before {{
      content: '';
      display: block;
      height: 3px;
      border-radius: 16px;
      background: linear-gradient(90deg, var(--purple), #58a6ff, var(--green));
      margin: -1.5rem -1.5rem 1.25rem;
      border-radius: 16px 16px 0 0;
    }}
    .next-steps-header {{
      display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.25rem;
    }}
    .next-steps-header h2 {{
      font-size: 1rem; font-weight: 700; color: var(--purple);
    }}
    .next-steps-header .subtitle {{
      font-size: 0.72rem; color: var(--text-muted);
    }}
    .steps-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 0.6rem;
    }}
    .step-item {{
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 0.75rem 1rem;
      display: flex;
      gap: 0.75rem;
      align-items: flex-start;
      transition: all 0.25s ease;
    }}
    .step-item:hover {{ background: var(--bg-card-hover); border-color: var(--purple); }}
    .step-checkbox {{
      width: 18px; height: 18px;
      border: 2px solid var(--border);
      border-radius: 5px;
      flex-shrink: 0;
      margin-top: 1px;
      cursor: pointer;
      transition: all 0.2s ease;
      position: relative;
    }}
    .step-checkbox.checked {{
      background: var(--green);
      border-color: var(--green);
    }}
    .step-checkbox.checked::after {{
      content: '✓';
      position: absolute;
      color: white;
      font-size: 12px;
      font-weight: 700;
      top: -1px; left: 2px;
    }}
    .step-text {{ flex: 1; }}
    .step-title {{ font-size: 0.83rem; font-weight: 600; color: var(--text); }}
    .step-desc {{ font-size: 0.75rem; color: var(--text-muted); margin-top: 2px; line-height: 1.4; }}

    /* ── Footer ── */
    .footer {{
      text-align: center;
      color: var(--text-dim);
      font-size: 0.75rem;
      margin-top: 1rem;
      animation: fadeUp 0.7s ease 0.6s both;
    }}

    /* ── Progress Bar ── */
    .progress-bar-wrapper {{
      max-width: 1100px;
      margin: 0 auto 1.5rem;
      animation: fadeUp 0.7s ease 0.45s both;
    }}
    .progress-label {{
      display: flex; justify-content: space-between;
      font-size: 0.75rem; color: var(--text-muted);
      margin-bottom: 0.4rem;
    }}
    .progress-track {{
      height: 6px;
      background: var(--bg-card);
      border-radius: 100px;
      overflow: hidden;
      border: 1px solid var(--border);
    }}
    .progress-fill {{
      height: 100%;
      background: linear-gradient(90deg, var(--blue), var(--green));
      border-radius: 100px;
      width: 0%;
      transition: width 0.5s ease;
    }}

    /* ── Animations ── */
    @keyframes fadeDown {{
      from {{ opacity: 0; transform: translateY(-20px); }}
      to   {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes fadeUp {{
      from {{ opacity: 0; transform: translateY(24px); }}
      to   {{ opacity: 1; transform: translateY(0); }}
    }}

    /* ── Pulse dot (live indicator) ── */
    .live-indicator {{
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      font-size: 0.7rem;
      color: var(--green);
      font-weight: 500;
    }}
    .pulse {{
      width: 7px; height: 7px;
      background: var(--green);
      border-radius: 50%;
      animation: pulse 2s infinite;
    }}
    @keyframes pulse {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50%       {{ opacity: 0.4; transform: scale(0.7); }}
    }}
  </style>
</head>
<body>

<header class="header">
  <div class="header-badge">Análise Estratégica</div>
  <h1>{data['title']}</h1>
  <p class="date">Gerado em {data['date']} &nbsp;·&nbsp;
    <span class="live-indicator">
      <span class="pulse"></span>
      Interativo
    </span>
  </p>
</header>

<div class="swot-grid" id="swot-grid">

  <!-- FORÇAS -->
  <div class="quadrant strengths">
    <div class="quadrant-header">
      <div class="quadrant-icon">🔵</div>
      <div class="quadrant-label">
        <h2>Forças</h2>
        <div class="subtitle">Fatores internos positivos</div>
      </div>
      <span class="item-count" id="count-s"></span>
    </div>
    <ul class="items-list" id="list-strengths"></ul>
  </div>

  <!-- FRAQUEZAS -->
  <div class="quadrant weaknesses">
    <div class="quadrant-header">
      <div class="quadrant-icon">🔴</div>
      <div class="quadrant-label">
        <h2>Fraquezas</h2>
        <div class="subtitle">Fatores internos negativos</div>
      </div>
      <span class="item-count" id="count-w"></span>
    </div>
    <ul class="items-list" id="list-weaknesses"></ul>
  </div>

  <!-- OPORTUNIDADES -->
  <div class="quadrant opportunities">
    <div class="quadrant-header">
      <div class="quadrant-icon">🟢</div>
      <div class="quadrant-label">
        <h2>Oportunidades</h2>
        <div class="subtitle">Fatores externos favoráveis</div>
      </div>
      <span class="item-count" id="count-o"></span>
    </div>
    <ul class="items-list" id="list-opportunities"></ul>
  </div>

  <!-- AMEAÇAS -->
  <div class="quadrant threats">
    <div class="quadrant-header">
      <div class="quadrant-icon">🟠</div>
      <div class="quadrant-label">
        <h2>Ameaças</h2>
        <div class="subtitle">Fatores externos desfavoráveis</div>
      </div>
      <span class="item-count" id="count-t"></span>
    </div>
    <ul class="items-list" id="list-threats"></ul>
  </div>

</div>

<!-- PRÓXIMOS PASSOS -->
<section class="next-steps-section" id="next-steps-section" style="display:none">
  <div class="next-steps-header">
    <div class="quadrant-icon" style="background:var(--purple-bg)">✅</div>
    <div>
      <h2>Próximos Passos Estratégicos</h2>
      <div class="subtitle">Clique nos checkboxes para marcar como concluído</div>
    </div>
    <span class="item-count" id="count-ns"></span>
  </div>
  <div class="steps-grid" id="list-next-steps"></div>
</section>

<!-- PROGRESS BAR DOS PRÓXIMOS PASSOS -->
<div class="progress-bar-wrapper" id="progress-wrapper" style="display:none">
  <div class="progress-label">
    <span>Progresso dos próximos passos</span>
    <span id="progress-text">0%</span>
  </div>
  <div class="progress-track">
    <div class="progress-fill" id="progress-fill"></div>
  </div>
</div>

<footer class="footer">
  Gerado pela Skill de Análise SWOT · Clique em qualquer item para expandir
</footer>

<script>
  const swotData = {{
    strengths:     {items_to_json(data['strengths'])},
    weaknesses:    {items_to_json(data['weaknesses'])},
    opportunities: {items_to_json(data['opportunities'])},
    threats:       {items_to_json(data['threats'])},
    next_steps:    {items_to_json(data['next_steps'])}
  }};

  function renderItems(listId, items, quadrantClass) {{
    const list = document.getElementById(listId);
    list.innerHTML = '';
    items.forEach((item, i) => {{
      const li = document.createElement('li');
      li.className = 'item';
      li.style.animationDelay = (i * 0.07) + 's';
      li.innerHTML = `
        <div class="item-title">
          <span class="dot"></span>
          <span>${{item.title}}</span>
        </div>
        ${{item.desc ? `<div class="item-desc">${{item.desc}}</div>` : ''}}
      `;
      if (item.desc) {{
        li.addEventListener('click', () => li.classList.toggle('expanded'));
      }}
      list.appendChild(li);
    }});
  }}

  function renderNextSteps(items) {{
    const container = document.getElementById('list-next-steps');
    const section = document.getElementById('next-steps-section');
    const wrapper = document.getElementById('progress-wrapper');

    if (!items || items.length === 0) return;
    section.style.display = 'block';
    wrapper.style.display = 'block';

    container.innerHTML = '';
    let checked = 0;

    items.forEach((item, i) => {{
      const div = document.createElement('div');
      div.className = 'step-item';
      div.innerHTML = `
        <div class="step-checkbox" id="cb-${{i}}"></div>
        <div class="step-text">
          <div class="step-title">${{item.title}}</div>
          ${{item.desc ? `<div class="step-desc">${{item.desc}}</div>` : ''}}
        </div>
      `;
      const cb = div.querySelector('.step-checkbox');
      cb.addEventListener('click', () => {{
        cb.classList.toggle('checked');
        updateProgress(items.length);
      }});
      container.appendChild(div);
    }});

    document.getElementById('count-ns').textContent = items.length;
    updateProgress(items.length);
  }}

  function updateProgress(total) {{
    const checked = document.querySelectorAll('.step-checkbox.checked').length;
    const pct = total > 0 ? Math.round((checked / total) * 100) : 0;
    document.getElementById('progress-fill').style.width = pct + '%';
    document.getElementById('progress-text').textContent = pct + '% (' + checked + '/' + total + ')';
  }}

  // Renderiza quadrantes
  renderItems('list-strengths',     swotData.strengths,     'strengths');
  renderItems('list-weaknesses',    swotData.weaknesses,    'weaknesses');
  renderItems('list-opportunities', swotData.opportunities, 'opportunities');
  renderItems('list-threats',       swotData.threats,       'threats');

  // Contagens
  document.getElementById('count-s').textContent = swotData.strengths.length;
  document.getElementById('count-w').textContent = swotData.weaknesses.length;
  document.getElementById('count-o').textContent = swotData.opportunities.length;
  document.getElementById('count-t').textContent = swotData.threats.length;

  // Próximos passos
  renderNextSteps(swotData.next_steps);
</script>
</body>
</html>
"""


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main():
    # Determina o caminho do arquivo de análise
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    else:
        # Tenta encontrar o arquivo padrão
        default_paths = [
            Path(__file__).parent.parent / "assets" / "analise-swot.md",
            Path("analise-swot.md"),
        ]
        input_path = None
        for p in default_paths:
            if p.exists():
                input_path = str(p)
                break
        if not input_path:
            print("ℹ️  Nenhum arquivo fornecido. Usando dados de exemplo.")
            input_path = "__example__"

    # Parse dos dados
    if input_path == "__example__":
        data = get_example_data()
    else:
        data = parse_swot_markdown(input_path)

    # Gera HTML
    html = generate_html(data)

    # Salva o arquivo
    output_path = Path(__file__).parent / "swot_visual.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Interface visual gerada com sucesso!")
    print(f"📄 Arquivo: {output_path.resolve()}")

    # Tenta abrir no browser
    try:
        webbrowser.open(output_path.resolve().as_uri())
        print("🌐 Abrindo no navegador...")
    except Exception:
        print("⚠️  Não foi possível abrir o navegador automaticamente.")
        print(f"    Abra manualmente: {output_path.resolve()}")


if __name__ == "__main__":
    main()
