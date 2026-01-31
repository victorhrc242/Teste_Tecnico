from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def get_product_data(product_name: str):
    print(f"\n[PASSO 1] Abrindo Chrome com Perfil Persistente para: {product_name}")
    
    # Criamos uma pasta para salvar os cookies e evitar CAPTCHA infinito
    # Isso faz com que o site te reconheça como um humano que já passou por lá
    user_data = os.path.join(os.getcwd(), "chrome_profile")

    # Inicializa o Driver com Modo UC e Perfil de Usuário
    driver = Driver(
        browser="chrome", 
        uc=True, 
        headless=False,
        user_data_dir=user_data, # Salva cookies e sessões
        incognito=False          # Não usar anônimo (ajuda a passar no bot detection)
    )

    try:
        url = f"https://www.worten.pt/search?query={product_name.replace(' ', '+')}"
        
        # Abre a URL e tenta lidar com o Cloudflare automaticamente
        driver.uc_open_with_reconnect(url, reconnect_time=6)
        
        print("[PASSO 2] Verificando CAPTCHA...")
        
        # Tenta clicar no botão de "Sou Humano" automaticamente se ele aparecer
        time.sleep(2)
        try:
            driver.uc_gui_click_captcha()
            print("  -> Tentativa de clique automático no CAPTCHA realizada.")
        except:
            pass

        # Se o CAPTCHA travar, damos 15 segundos para você clicar manualmente
        # Uma vez resolvido com o 'user_data_dir', ele dificilmente pedirá de novo
        time.sleep(5)

        # --- LOCALIZAR O CARD PRINCIPAL ---
        print("[PASSO 3] Localizando container do produto...")
        wait = WebDriverWait(driver, 20)
        
        # Espera o card carregar (se o CAPTCHA passar, o h3 aparece)
        card = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card__text-container")))

        # --- EXTRAIR NOME ---
        print("[PASSO 4] Extraindo nome...")
        name = card.find_element(By.CSS_SELECTOR, "h3.product-card__name").text.strip()
        print(f"  -> Nome: {name}")

        # --- EXTRAIR PREÇO (META DATA) ---
        print("[PASSO 5] Extraindo preço...")
        try:
            # Busca o preço direto na meta tag (conforme o seu HTML)
            price_meta = card.find_element(By.CSS_SELECTOR, "meta[itemprop='price']")
            final_price = float(price_meta.get_attribute("content"))
        except:
            val = card.find_element(By.CSS_SELECTOR, ".value").text
            dec = card.find_element(By.CSS_SELECTOR, ".decimal").text
            final_price = float(f"{val.replace('.', '')}.{dec}")
        
        print(f"  -> Preço: {final_price}")

        # --- EXTRAIR LINK ---
        print("[PASSO 6] Extraindo link...")
        try:
            path = card.find_element(By.CSS_SELECTOR, "[itemprop='offers']").get_attribute("itemid")
            product_link = f"https://www.worten.pt{path}"
        except:
            product_link = card.find_element(By.TAG_NAME, "a").get_attribute("href")

        # --- EXTRAIR VENDEDOR ---
        print("[PASSO 7] Extraindo vendedor...")
        try:
            seller = card.find_element(By.CSS_SELECTOR, "b[itemprop='seller']").text.strip()
        except:
            seller = "Worten"

        return {
            "Name": name,
            "Score": final_price,
            "Status": "Disponível",
            "Seller": seller,
            "Link": product_link,
            "EAN": "N/A",
            "Mirakl_Image": "",
            "BB_Image_Url": ""
        }

    except Exception as e:
        print(f"\n[ERRO] O loop do CAPTCHA ou erro de elemento impediu a extração: {e}")
        return None

    finally:
        print("[FINAL] Fechando navegador.")
        time.sleep(2)
        driver.quit()