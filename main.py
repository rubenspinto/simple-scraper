# ============================================================================
# WEB SCRAPING - VITRINE SEBRAE STARTUPS (COM PLAYWRIGHT)
# ============================================================================
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import re

def scrape_sebrae_vitrine(max_paginas=100):
    """Extrai startups do Vitrine Sebrae interagindo com cliques usando Playwright"""

    todas_startups = []

    # Inicia a automação de navegador
    with sync_playwright() as p:
        # headless=True roda invisível. Mude para False se quiser ver ele clicando!
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for pag in range(1, max_paginas + 1):
            print(f"📄 Página {pag}...", end=" ", flush=True)

            url = f"https://vitrine.sebraestartups.com.br/?hasTag=true&page={pag}"
            page.goto(url, wait_until="networkidle")

            try:
                # Aguarda os cards carregarem na tela (timeout de 10s)
                page.wait_for_selector('article.flex', timeout=10000)
            except:
                print("❌ Sem mais dados ou fim das páginas")
                break

            # Localiza todos os cards renderizados pelo Playwright
            cards_locator = page.locator('article.flex').all()
            print(f"✅ {len(cards_locator)} startups")

            for card_loc in cards_locator:
                # 1. Pega o HTML do card para usar com seu BeautifulSoup atual
                html_card = card_loc.inner_html()
                card = BeautifulSoup(html_card, 'html.parser')

                h3 = card.find('h3', class_='font-bold')
                if not h3:
                    continue
                
                nome_startup = h3.text.strip()

                # Extrair dados estáticos (mantive sua lógica original)
                tipo_div = card.find('div', string=re.compile('Startup|Projeto'))
                local_p = card.find('p', string=re.compile(r'[A-Z]{2}$'))
                mat_p = card.find('p', string=re.compile('Crescimento|Validação|Tração|Escala|Ideação'))

                # 2. CAPTURA DE EMAIL (O Segredo do Clique + Regex)
                email = ''
                padrao_email = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
                
                # Procura o botão que tem o ícone da carta
                botao_email = card_loc.locator('button:has(svg.lucide-mail)')
                
                if botao_email.count() > 0:
                    try:
                        # Pega todos os emails na página ANTES de clicar
                        emails_antes = set(re.findall(padrao_email, page.content()))
                        
                        # Clica no botão do email
                        botao_email.first.click(timeout=3000)
                        page.wait_for_timeout(600) # Aguarda 0.6s para o pop-up renderizar
                        
                        # Pega todos os emails na página DEPOIS de clicar
                        emails_depois = set(re.findall(padrao_email, page.content()))
                        
                        # A diferença entre "depois" e "antes" é o email recém revelado!
                        novos_emails = list(emails_depois - emails_antes)
                        if novos_emails:
                            email = novos_emails[0]
                            
                        # Pressiona ESC para fechar o pop-up e não atrapalhar o próximo card
                        page.keyboard.press("Escape")
                        page.wait_for_timeout(200)
                    except Exception as e:
                        # Se der erro no clique, apenas ignora e segue para a próxima
                        pass

                # Telefone
                telefone = ''
                tel_link = card.find('a', href=re.compile(r'^tel:'))
                if tel_link:
                    telefone = tel_link.get('href', '').replace('tel:', '')

                # Website
                site_url = ''
                for link in card.find_all('a', href=True):
                    href = link.get('href', '')
                    if href.startswith('http') and 'sebraestartups' not in href and 'mailto' not in href and 'tel' not in href:
                        site_url = href
                        break

                # Descrição e Segmento
                desc_p = card.find('p', class_='text-justify')
                segmento = ''
                seg_divs = card.find_all('div', class_=lambda x: x and 'rounded-full' in str(x))
                for div in seg_divs:
                    text = div.text.strip()
                    if text and text not in ['Startup', 'Projeto Inovador', 'Participante']:
                        segmento = text
                        break

                # Imagem
                img = card.find('img', alt='Company logo')

                startup = {
                    'type': tipo_div.text.strip() if tipo_div else '',
                    'name': nome_startup,
                    'local': local_p.text.strip() if local_p else '',
                    'segment_pt': segmento,
                    'maturity_pt': mat_p.text.strip() if mat_p else '',
                    'siteUrl': site_url,
                    'email': email,
                    'phone': telefone,
                    'description_pt': desc_p.text.strip() if desc_p else '',
                    'imageUrl': img.get('src', '') if img else ''
                }

                todas_startups.append(startup)

            # Uma pequena pausa entre páginas para não sobrecarregar o site
            time.sleep(1)

        browser.close()

    return todas_startups


# ============================================================================
# EXECUTAR E SALVAR
# ============================================================================

if __name__ == "__main__":
    print("🚀 Iniciando scraping com Playwright...\n")
    print("="*60)

    startups = scrape_sebrae_vitrine(max_paginas=2) # Coloquei 2 páginas para você testar rápido

    print("="*60)

    if startups:
        df = pd.DataFrame(startups)
        df = df.drop_duplicates(subset=['name'], keep='first')

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'vitrine_startups_{timestamp}.csv'
        df.to_csv(filename, index=False, encoding='utf-8-sig')

        print(f"\n✅ CONCLUÍDO!")
        print("="*60)
        print(f"📁 Arquivo: {filename}")
        print(f"📊 Total: {len(df)} startups")
        print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("="*60)

        print(f"\n📧 Com email: {df['email'].astype(bool).sum()}")
        print(f"📞 Com telefone: {df['phone'].astype(bool).sum()}")
        print(f"🌐 Com website: {df['siteUrl'].astype(bool).sum()}")

        print(f"\n📋 PREVIEW:")
        print("="*60)
        print(df[['name', 'email']].head(10)) # Mostra apenas Nome e Email para checagem rápida

    else:
        print("\n❌ Nenhum dado coletado!")