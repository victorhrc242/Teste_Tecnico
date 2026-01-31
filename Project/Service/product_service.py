import pandas as pd
from models.product import Product
from Repositore.product_repository import ProductRepository
from scraping.worten_scraper import get_product_data

class ProductService:
    @staticmethod
    def process_initial_spreadsheet(file_path: str):
        """Lê a planilha e garante que está pegando o NOME para pesquisar."""
        try:
            df = pd.read_excel(file_path)
            
            # Lógica para encontrar a coluna do Nome do Produto
            # 1. Tenta encontrar por nomes comuns de colunas
            possiveis_colunas = ['Name', 'Nome', 'Produto', 'Product', 'Designação']
            col_alvo = None
            
            for col in df.columns:
                if str(col).strip() in possiveis_colunas:
                    col_alvo = col
                    break
            
            # 2. Se não achar pelo nome, e a primeira for ID (numérica), tenta a segunda
            if col_alvo is None:
                col_alvo = df.columns[1] if len(df.columns) > 1 else df.columns[0]

            print(f"[INFO] Usando a coluna '{col_alvo}' para pesquisa.")

            for valor in df[col_alvo]:
                nome_produto = str(valor).strip()
                # Evita pesquisar células vazias ou apenas números de ID acidentais
                if pd.notna(valor) and len(nome_produto) > 2:
                    print(f"[BUSCA] Iniciando scraping para: {nome_produto}")
                    ProductService.add_product_by_name(nome_produto)
            
            return True
        except Exception as e:
            print(f"Erro ao processar planilha: {e}")
            return False

    @staticmethod
    def add_product_by_name(product_name: str):
        """Usa o NOME recebido para fazer o scraping."""
        data = get_product_data(product_name)
        if not data:
            return None

        all_products = ProductRepository.get_all_products()
        numeric_ids = [int(p.ID) for p in all_products if str(p.ID).isdigit()]
        next_id = max(numeric_ids, default=0) + 1

        product = Product(
            ID=str(next_id),
            EAN="N/A",
            Name=data.get("Name"), # Nome extraído do site
            Status=data.get("Status"),
            Score=data.get("Score"),
            Seller=data.get("Seller"),
            Link=data.get("Link")
        )

        ProductRepository.add_product(product)
        return product