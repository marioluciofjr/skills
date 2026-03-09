"""
Módulo scraper para a tabela de 'Participantes' do Big Brother Brasil.
Responsabilidade: Extrair exclusivamente as tabelas cujos subtítulos
indicam a listagem oficial dos participantes da edição.

Uso:
  python bbb-participantes.py <numero_da_edicao>
"""
import sys
import requests
from bs4 import BeautifulSoup
import time

def get_participantes(edition_number: str) -> str:
    """Busca a página do BBB especificada e extrai apenas tabelas que contêm 'Participantes' nos cabeçalhos adjacentes."""
    url = f"https://pt.wikipedia.org/wiki/Big_Brother_Brasil_{edition_number}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        time.sleep(10)
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        return f"Erro ao acessar {url}: {e}"

    soup = BeautifulSoup(response.text, 'html.parser')
    content = [f"# Participantes do Big Brother Brasil {edition_number}\n"]
    
    # Filtro focado nas tabelas de Participantes
    tables = soup.find_all('table', class_=['sortable', 'wikitable'])
    found = False
    
    for idx, table in enumerate(tables):
        prev = table.find_previous(['h2', 'h3'])
        if prev:
            title = prev.get_text(strip=True).upper()
            if 'PARTICIPANTE' in title:
                found = True
                content.append(f"## {title} (Tabela {idx+1})\n")
                content.append("| " + " | ".join(th.get_text(strip=True) for th in table.find('tr').find_all(['th', 'td'])) + " |")
                content.append("|" + "---|"*len(table.find('tr').find_all(['th', 'td'])))
                
                rows = table.find_all('tr')[1:]
                for row in rows:
                    cols = row.find_all(['th', 'td'])
                    col_texts = [col.get_text(strip=True).replace('\n', ' ') for col in cols]
                    if col_texts:
                        content.append("| " + " | ".join(col_texts) + " |")
                content.append("\n")
                
    if not found:
        return f"Não foi possível localizar a tabela de Participantes para o BBB {edition_number} de forma estruturada. Considere a tool search_web caso precise."
    
    content.append("\n**ATENÇÃO LLM (GUARDRAIL DE HOMÔNIMOS):** Ao ler a tabela acima, verifique sempre o NOME e SOBRENOME completos do participante. Não confunda homônimos (ex: Ana Paula Costa vs Ana Paula Renault). Seja absolutamente cético e objetivo.")
        
    return "\n".join(content)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(get_participantes(sys.argv[1]))
    else:
        print("Uso: python bbb-participantes.py <numero_da_edicao>")
