from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time


driver = webdriver.Chrome()

wait = WebDriverWait(driver, 10)
startups = []
page = 1
cookies_aceitos = False
nomes_pagina_anterior = set()  # ✅ detecta quando o site para de mudar


while True:
    url = f'https://vitrine.sebraestartups.com.br/?hasTag=true&page={page}'
    driver.get(url)

    # Injeta override do clipboard após cada get()
    driver.execute_script("""
        window.captured_email = "";
        if (navigator.clipboard) {
            navigator.clipboard.writeText = (text) => {
                window.captured_email = text;
                return Promise.resolve();
            };
        }
    """)

    print(f'\n📄 Página {page}: {url}')

    # Aceitar cookies apenas na primeira página
    if not cookies_aceitos:
        try:
            cookie_button = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
            driver.execute_script("arguments[0].click();", cookie_button)
            print("Banner de cookies aceito.")
            cookies_aceitos = True
            time.sleep(1)
        except TimeoutException:
            cookies_aceitos = True

    # Aguarda os cards carregarem
    try:
        cards = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'article')))
    except TimeoutException:
        print(f"⚠️ Nenhum card encontrado na página {page}. Encerrando.")
        break

    if not cards:
        print("Sem cards. Encerrando.")
        break

    # ✅ CONDIÇÃO DE PARADA: compara nomes com a página anterior
    nomes_pagina_atual = set()
    for c in cards:
        try:
            nomes_pagina_atual.add(c.find_element(By.CSS_SELECTOR, 'h3').text)
        except:
            pass

    if nomes_pagina_atual and nomes_pagina_atual == nomes_pagina_anterior:
        print(f"📌 Página {page} igual à anterior. Última página atingida. Encerrando.")
        break

    nomes_pagina_anterior = nomes_pagina_atual
    print(f"   {len(cards)} cards encontrados.")

    for card in cards:
        name = ""
        try:
            name = card.find_element(By.CSS_SELECTOR, 'h3').text
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
            time.sleep(0.5)

            # imageUrl
            try:
                imageUrl = card.find_element(By.CSS_SELECTOR, 'img').get_attribute('src') or ""
            except:
                imageUrl = ""

            # description_pt
            try:
                paragraphs = card.find_elements(By.CSS_SELECTOR, 'p')
                description_pt = max((p.text.strip() for p in paragraphs), key=len, default="")
            except:
                description_pt = ""

            # local
            try:
                pin = card.find_element(By.XPATH, './/*[contains(@class,"lucide-map-pin")]')
                local = driver.execute_script(
                    "return arguments[0].parentElement.nextElementSibling.textContent;", pin
                ).strip()
            except:
                local = ""

            # siteUrl
            try:
                links = card.find_elements(By.CSS_SELECTOR, "a[href^='http']")
                siteUrl = next(
                    (l.get_attribute('href') for l in links if 'sebrae' not in (l.get_attribute('href') or '')),
                    ""
                )
            except:
                siteUrl = ""

            # badges
            try:
                badges = card.find_elements(By.CSS_SELECTOR,
                    "span[class*='rounded-full'], div[class*='rounded-full'], "
                    "span[class*='rounded-md'][class*='bg-'], div[class*='rounded-md'][class*='bg-']"
                )
                badge_texts = [b.text.strip() for b in badges if b.text.strip()]
                badge_texts = [b for b in badge_texts if b not in ['Ver detalhes', 'Acessar']]
                startup_type = badge_texts[0] if len(badge_texts) > 0 else ""
                segment_pt   = badge_texts[1] if len(badge_texts) > 1 else ""
                maturity_pt  = badge_texts[2] if len(badge_texts) > 2 else ""
            except:
                startup_type = segment_pt = maturity_pt = ""

            # Email via clipboard
            driver.execute_script("window.captured_email = '';")
            try:
                email_button = card.find_element(By.CSS_SELECTOR, 'button:has(svg.lucide-mail)')
                email = (
                    email_button.get_attribute('data-email') or
                    email_button.get_attribute('aria-label') or
                    ""
                )
                if not email:
                    driver.execute_script("arguments[0].click();", email_button)
                    time.sleep(0.5)
                    email = driver.execute_script("return window.captured_email;") or ""
            except:
                email = ""
            driver.execute_script("window.captured_email = '';")

            # Phone via clipboard
            driver.execute_script("window.captured_email = '';")
            try:
                phone_button = card.find_element(By.CSS_SELECTOR, 'button:has(svg.lucide-phone)')
                phone = (
                    phone_button.get_attribute('data-phone') or
                    phone_button.get_attribute('aria-label') or
                    ""
                )
                if not phone:
                    driver.execute_script("arguments[0].click();", phone_button)
                    time.sleep(0.5)
                    phone = driver.execute_script("return window.captured_email;") or ""
            except:
                phone = ""
            driver.execute_script("window.captured_email = '';")

            print(f'  ✔ {name} | {local} | {email} | {phone}')

            startups.append({
                'type': startup_type, 'name': name, 'local': local,
                'segment_pt': segment_pt, 'maturity_pt': maturity_pt,
                'siteUrl': siteUrl, 'email': email, 'phone': phone,
                'description_pt': description_pt, 'imageUrl': imageUrl,
            })

        except Exception as e:
            print(f'  Erro: {name} - {e}')

    page += 1
    time.sleep(1)


driver.quit()

df = pd.DataFrame(startups, columns=[
    'type', 'name', 'local', 'segment_pt', 'maturity_pt',
    'siteUrl', 'email', 'phone', 'description_pt', 'imageUrl'
])
df.to_csv('startups_completo.csv', index=False, encoding='utf-8-sig')
print(f'\n✅ Arquivo salvo com {len(startups)} startups!')

