"""
Módulo scraper para a tabela 'Histórico' / 'Paredões' do Big Brother Brasil.
Responsabilidade: Extrair a matriz que contabiliza as dinâmicas de votos
da casa, indicações de líderes e imunidade.

Uso:
  python bbb-historico.py <numero_da_edicao>
"""
import sys
import requests
from bs4 import BeautifulSoup
import time

def get_historico(edition_number: str) -> str:
    """Busca a página e capta exclusivamente as tabelas do Histórico de Votação / Paredões."""
    url = f"https://pt.wikipedia.org/wiki/Big_Brother_Brasil_{edition_number}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        time.sleep(10)
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        return f"Erro ao acessar {url}: {e}"

    soup = BeautifulSoup(response.text, 'html.parser')
    content = [f"# Histórico de Votações do Big Brother Brasil {edition_number}\n"]
    
    tables = soup.find_all('table', class_=['sortable', 'wikitable', 'hlist'])
    found = False
    
    for idx, table in enumerate(tables):
        prev = table.find_previous(['h2', 'h3'])
        if prev:
            title = prev.get_text(strip=True).upper()
            if 'HISTÓRICO' in title or 'PAREDÕES' in title or 'VOTAÇÃO' in title:
                found = True
                content.append(f"## {title} (Tabela {idx+1})\n")
                
                # As tabelas de histórico do BBB na Wiki costumam usar colspans pesados.
                # Retornamos em formato de log para evitar quebra do Markdown parser
                for row in table.find_all('tr'):
                    cols = row.find_all(['th', 'td'])
                    col_texts = [c.get_text(strip=True).replace('\n', ' ') for c in cols if c.get_text(strip=True)]
                    if col_texts:
                        content.append(" | ".join(col_texts))
                content.append("\n")
                
    if not found:
        return f"Não foi possível encontrar a tabela 'Histórico' no BBB {edition_number}. Faça 'search_web' diretamente."
        
    content.append("\n**ATENÇÃO LLM (GUARDRAIL DE HOMÔNIMOS):** Ao ler a tabela acima, verifique sempre o NOME completo do participante. Cuidado com homônimos de edições diferentes.")

    return "\n".join(content)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(get_historico(sys.argv[1]))
    else:
        print("Uso: python bbb-historico.py <numero_da_edicao>")
