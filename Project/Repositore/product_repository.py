import pandas as pd
from pathlib import Path
from models.product import Product

FILE_PATH = Path("data/worten_final.xlsx")

class ProductRepository:
    @staticmethod
    def _load_file() -> pd.DataFrame:
        if FILE_PATH.exists():
            # Forçamos o ID como string para não perdermos formatação
            return pd.read_excel(FILE_PATH, dtype={'ID': str}).fillna("")
        return pd.DataFrame(columns=["ID", "EAN", "Name", "Status", "Score", "Seller", "Link"])

    @staticmethod
    def add_product(product: Product):
        df = ProductRepository._load_file()
        # Converte o objeto para dicionário
        new_row = pd.DataFrame([product.__dict__])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_excel(FILE_PATH, index=False)

    @staticmethod
    def get_all_products() -> list[Product]:
        df = ProductRepository._load_file()
        products = []
        for _, row in df.iterrows():
            # Mapeamento explícito para garantir que o ID não seja tratado como float 1.0
            products.append(Product(
                ID=str(row['ID']),
                EAN=str(row['EAN']),
                Name=str(row['Name']),
                Status=str(row['Status']),
                Score=float(row['Score']) if row['Score'] else 0.0,
                Seller=str(row['Seller']),
                Link=str(row['Link'])
            ))
        return products