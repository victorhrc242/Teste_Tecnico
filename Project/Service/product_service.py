import pandas as pd
from models.product import Product
from Repositore.product_repository import ProductRepository
from scraping.worten_scraper import WortenScraper

class ProductService:
    @staticmethod
    def process_initial_spreadsheet():
        """Lógica principal: lê a entrada, verifica o que já existe e processa apenas o novo."""
        # 1. Carrega a planilha original (worten.xlsx)
        df_input = ProductRepository.load_input_spreadsheet()
        if df_input is None:
            return False

        # 2. Carrega produtos já processados para evitar duplicados (Idempotência)
        existing_products = ProductRepository.get_all_products()
        # Criamos um set de nomes já processados para busca rápida
        processed_names = {p.Name.lower() for p in existing_products}

        # Identifica a coluna de pesquisa (Name, Produto, etc)
        col_alvo = next((c for c in df_input.columns if str(c).lower() in ['name', 'nome', 'produto']), df_input.columns[0])

        bot = WortenScraper()
        
        try:
            for index, row in df_input.iterrows():
                nome_pesquisa = str(row[col_alvo]).strip()

                # Pula se estiver vazio ou se já tiver sido processado
                if not nome_pesquisa or nome_pesquisa.lower() == "nan":
                    continue
                
                if nome_pesquisa.lower() in processed_names:
                    print(f"[SKIP] Produto já processado anteriormente: {nome_pesquisa}")
                    continue

                print(f"[*] Iniciando busca para: {nome_pesquisa}")
                
                try:
                    data = bot.get_product_data(nome_pesquisa)
                    if data:
                        # Criar novo objeto com ID sequencial baseado no total atual
                        new_id = str(len(ProductRepository.get_all_products()) + 1)
                        
                        product = Product(
                            ID=new_id,
                            EAN="N/A",
                            Name=data["Name"],
                            Status=data["Status"],
                            Score=data["Score"],
                            Seller=data["Seller"],
                            Link=data["Link"]
                        )
                        # Salva imediatamente no Excel para não perder progresso
                        ProductRepository.add_product(product)
                        processed_names.add(data["Name"].lower())
                    else:
                        print(f"[!] Produto não encontrado no site: {nome_pesquisa}")
                except Exception as e:
                    print(f"[ERRO] Falha ao processar item {nome_pesquisa}: {e}")
                    # Continua para o próximo item mesmo se um falhar
                    continue
        finally:
            bot.stop()
            
        return True

    @staticmethod
    def add_single_product(name: str):
        """Adiciona um único produto via API."""
        bot = WortenScraper()
        try:
            data = bot.get_product_data(name)
            if not data: return None
            
            new_id = str(len(ProductRepository.get_all_products()) + 1)
            product = Product(
                ID=new_id, EAN="N/A", Name=data["Name"],
                Status=data["Status"], Score=data["Score"],
                Seller=data["Seller"], Link=data["Link"]
            )
            ProductRepository.add_product(product)
            return product
        finally:
            bot.stop()