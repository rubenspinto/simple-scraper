from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

driver = webdriver.Chrome()
driver.get('https://vitrine.sebraestartups.com.br/?hasTag=true&page=1')

# Injeta o interceptor de clipboard (igual ao original)
driver.execute_script("""
    window.captured_email = "";
    navigator.clipboard.writeText = (text) => {
        window.captured_email = text;
        return Promise.resolve();
    };
""")

wait = WebDriverWait(driver, 10)

try:
    cookie_button = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
    cookie_button.click()
    print("Banner de cookies aceito.")
except:
    pass

cards = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'article')))

startups = []

for card in cards:
    name = ""
    try:
        name = card.find_element(By.CSS_SELECTOR, 'h3').text
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
        time.sleep(0.5)

        # ── Campos que NÃO precisam de clique ──────────────────────
        # imageUrl
        try:
            imageUrl = card.find_element(By.CSS_SELECTOR, 'img').get_attribute('src') or ""
        except:
            imageUrl = ""

        # description_pt (parágrafo mais longo do card)
        try:
            paragraphs = card.find_elements(By.CSS_SELECTOR, 'p')
            description_pt = max((p.text.strip() for p in paragraphs), key=len, default="")
        except:
            description_pt = ""

        # local (elemento após ícone de mapa)
        try:
            pin = card.find_element(By.CSS_SELECTOR, 'svg.lucide-map-pin')
            local = driver.execute_script(
                "return arguments[0].parentElement.textContent;", pin
            ).strip()
        except:
            local = ""

        # siteUrl (link externo, excluindo domínios sebrae)
        try:
            links = card.find_elements(By.CSS_SELECTOR, "a[href^='http']")
            siteUrl = next(
                (l.get_attribute('href') for l in links if 'sebrae' not in (l.get_attribute('href') or '')),
                ""
            )
        except:
            siteUrl = ""

       # badges: type / segment_pt / maturity_pt
        try:
            # Mudamos a busca para classes características de "badges" no Tailwind CSS
            badges = card.find_elements(By.CSS_SELECTOR,
                "span[class*='rounded-full'], div[class*='rounded-full'], "
                "span[class*='rounded-md'][class*='bg-'], div[class*='rounded-md'][class*='bg-']"
            )
            
            # Extrai o texto e ignora os que vierem vazios
            badge_texts = [b.text.strip() for b in badges if b.text.strip()]
            
            # Remove palavras indesejadas que podem vir no meio das tags (opcional, mas recomendado)
            badge_texts = [b for b in badge_texts if b not in ['Ver detalhes', 'Acessar']]

            # Atribui os valores baseados na ordem em que aparecem
            startup_type  = badge_texts[0] if len(badge_texts) > 0 else ""
            segment_pt    = badge_texts[1] if len(badge_texts) > 1 else ""
            maturity_pt   = badge_texts[2] if len(badge_texts) > 2 else ""
            
        except Exception as e:
            # Imprimir o erro ajuda a debugar caso algo mude no site futuramente
            print(f"Aviso: Erro ao extrair badges - {e}")
            startup_type = segment_pt = maturity_pt = ""

        # ── Email via clipboard (lógica ORIGINAL intacta) ──────────
        driver.execute_script("window.captured_email = '';")
        try:
            email_button = card.find_element(By.CSS_SELECTOR, 'button:has(svg.lucide-mail)')
            driver.execute_script("arguments[0].click();", email_button)
            time.sleep(0.5)
        except:
            pass
        email = driver.execute_script("return window.captured_email;") or ""
        driver.execute_script("window.captured_email = '';")

        # ── Phone via clipboard (mesma lógica do email) ────────────
        try:
            phone_button = card.find_element(By.CSS_SELECTOR, 'button:has(svg.lucide-phone)')
            driver.execute_script("arguments[0].click();", phone_button)
            time.sleep(0.5)
        except:
            pass
        phone = driver.execute_script("return window.captured_email;") or ""
        driver.execute_script("window.captured_email = '';")

        print(f'✔ {name} | {email} | {phone}')

        startups.append({
            'type':           startup_type,
            'name':           name,
            'local':          local,
            'segment_pt':     segment_pt,
            'maturity_pt':    maturity_pt,
            'siteUrl':        siteUrl,
            'email':          email,
            'phone':          phone,
            'description_pt': description_pt,
            'imageUrl':       imageUrl,
        })

    except Exception as e:
        print(f'Erro ao processar card: {name} - {e}')

driver.quit()

df = pd.DataFrame(startups, columns=[
    'type','name','local','segment_pt','maturity_pt',
    'siteUrl','email','phone','description_pt','imageUrl'
])
df.to_csv('startups_completo.csv', index=False, encoding='utf-8-sig')
print(f'Arquivo salvo com {len(startups)} startups!')
