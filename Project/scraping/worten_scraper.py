from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from difflib import SequenceMatcher
import time
import os

STOP_WORDS = {"com", "de", "para", "o", "a", "os", "as", "e", "em"}

class WortenScraper:
    def __init__(self):
        user_data = os.path.join(os.getcwd(), "chrome_profile")
        self.driver = Driver(
            browser="chrome",
            uc=True,
            headless=False,
            user_data_dir=user_data
        )

    def _calculate_similarity_score(self, searched: str, found: str) -> float:
        """Calcula um score de 0 a 1 da similaridade entre nomes"""
        searched_words = [w for w in searched.lower().split() if w not in STOP_WORDS]
        found_text = found.lower()

        if not searched_words:
            return 0.0

        # 1️⃣ Similaridade por palavras importantes
        word_matches = sum(1 for word in searched_words if word in found_text)
        word_similarity = word_matches / len(searched_words)

        # 2️⃣ Similaridade global da string
        seq_similarity = SequenceMatcher(None, searched.lower(), found.lower()).ratio()

        # Combina os dois (peso igual)
        score = (word_similarity + seq_similarity) / 2
        return score

    def get_product_data(self, product_name: str):
        try:
            url = f"https://www.worten.pt/search?query={product_name.replace(' ', '+')}"
            self.driver.uc_open_with_reconnect(url, reconnect_time=4)
            wait = WebDriverWait(self.driver, 12)

            # Aceitar cookies se aparecer
            try:
                btn = "#onetrust-accept-btn-handler"
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, btn)))
                self.driver.execute_script(
                    "document.querySelector(arguments[0]).click();", btn
                )
                time.sleep(1)
            except:
                pass

            # Verifica se há resultados
            page_text = self.driver.page_source.lower()
            if "0 resultados" in page_text or "não encontrámos o que procura" in page_text:
                return self._indisponivel(product_name)

            cards = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-card"))
            )

            best_product = None
            highest_score = 0.0

            for card in cards:
                try:
                    name = card.find_element(
                        By.CSS_SELECTOR, "h3.product-card__name"
                    ).text.strip()

                    score = self._calculate_similarity_score(product_name, name)

                    # Ignora produtos com score muito baixo
                    if score < 0.6:
                        continue

                    # Pega preço
                    try:
                        p = card.find_element(By.CSS_SELECTOR, "[itemprop='price']")
                        price = float(p.get_attribute("content"))
                    except:
                        continue

                    # Pega vendedor
                    try:
                        seller = card.find_element(
                            By.CSS_SELECTOR, ".product-card__seller b"
                        ).text.strip()
                    except:
                        seller = "Worten"

                    link = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

                    # Escolhe o produto com maior score de similaridade
                    if score > highest_score or (score == highest_score and price < best_product.get("Score", float('inf'))):
                        highest_score = score
                        best_product = {
                            "Name": name,
                            "Link": link,
                            "Score": price,
                            "Seller": seller,
                            "Status": "Disponível",
                            "MatchScore": round(score, 2)  # mostra score para verificação
                        }

                except:
                    continue

            return best_product if best_product else self._indisponivel(product_name)

        except Exception as e:
            print(f"Erro scraper: {e}")
            return self._indisponivel(product_name)

    def _indisponivel(self, name):
        return {
            "Name": name,
            "Link": "",
            "Score": 0.0,
            "Seller": "Worten",
            "Status": "Indisponível",
            "MatchScore": 0.0
        }

    def stop(self):
        self.driver.quit()
