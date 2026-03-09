"""
Módulo scraper Geral para captar fatos avulsos do Big Brother Brasil.
Responsabilidade: Capturar resumos, parágrafos introdutórios e tabelas extras
(Big Fone, Casa de Vidro, Castigo do Monstro) que fogem ao modelo Participante/Histórico padrão.

Uso:
  python bbb-geral.py <numero_da_edicao>
"""
import sys
import requests
from bs4 import BeautifulSoup
import time

def get_fatos_gerais(edition_number: str) -> str:
    """Busca tópicos como Big Fone, Punições, Provas de Resistência, etc."""
    url = f"https://pt.wikipedia.org/wiki/Big_Brother_Brasil_{edition_number}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        time.sleep(10)
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        return f"Erro ao acessar {url}: {e}"

    soup = BeautifulSoup(response.text, 'html.parser')
    content = [f"# Fatos Gerais: Big Brother Brasil {edition_number}\n"]
    
    # Busca por elementos de curiosidades ou fatos extras no corpo e tabelas menores
    headings = soup.find_all(['h2', 'h3'])
    for h in headings:
        title = h.get_text(strip=True).upper()
        # Ignorar as que já estão no bbb-participantes.py e bbb-historico.py
        if 'PARTICIPANTE' not in title and 'HISTÓRICO' not in title and 'VOTAÇÃO' not in title:
            # Seleciona as temáticas comuns de curiosidade
            if any(key in title for key in ['BIG FONE', 'MONSTRO', 'ANJO', 'CASA DE VIDRO', 'XEPA']):
                content.append(f"## {title}")
                # Pegar p ou ul que sucede o heading
                nxt = h.find_next_sibling()
                while nxt and nxt.name not in ['h2', 'h3']:
                    if nxt.name in ['p', 'ul', 'ol', 'table']:
                        text = nxt.get_text(strip=True, separator=" ")
                        # Evitar imprimir HTML vazio
                        if text:
                            content.append(text)
                    nxt = nxt.find_next_sibling()
                content.append("\n")

    result = "\n".join(content)
    if len(result.strip()) < 50:
        return "Nada encontrado sobre Big Fones, Casa de Vidro ou dinâmicas específicas na página Wiki. Utilize 'search_web' em portais jornalísticos e Gshow."
    return result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(get_fatos_gerais(sys.argv[1]))
    else:
        print("Uso: python bbb-geral.py <numero_da_edicao>")
