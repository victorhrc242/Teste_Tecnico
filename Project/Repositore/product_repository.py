import pandas as pd
from pathlib import Path
from models.product import Product

INPUT_FILE = Path("data/worten.xlsx")
OUTPUT_FILE = Path("data/worten_final.xlsx")

class ProductRepository:
    @staticmethod
    def _load_file() -> pd.DataFrame:
        if OUTPUT_FILE.exists():
            return pd.read_excel(OUTPUT_FILE, dtype={'ID': str}).fillna("")
        # Estrutura completa exigida pelo desafio
        return pd.DataFrame(columns=["ID", "EAN", "Name", "Status", "Score", "Seller", "Link"])

    @staticmethod
    def get_all_products() -> list[Product]:
        df = ProductRepository._load_file()
        products = []
        for _, row in df.iterrows():
            products.append(Product(
                ID=str(row['ID']),
                EAN=str(row.get('EAN', 'N/A')),
                Name=str(row['Name']),
                Status=str(row['Status']),
                Score=float(row['Score']) if row['Score'] else 0.0,
                Seller=str(row.get('Seller', 'Worten')),
                Link=str(row.get('Link', ''))
            ))
        return products

    @staticmethod
    def add_product(product: Product):
        df = ProductRepository._load_file()
        new_row = pd.DataFrame([product.__dict__])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_excel(OUTPUT_FILE, index=False)

    @staticmethod
    def update_product(product_id: str, updated_data: dict):
        df = ProductRepository._load_file()
        if product_id in df['ID'].values:
            for key, value in updated_data.items():
                if value is not None and key in df.columns:
                    df.loc[df['ID'] == product_id, key] = value
            df.to_excel(OUTPUT_FILE, index=False)
            return True
        return False

    @staticmethod
    def delete_product(product_id: str):
        df = ProductRepository._load_file()
        if product_id in df['ID'].values:
            df = df[df['ID'] != product_id]
            df.to_excel(OUTPUT_FILE, index=False)
            return True
        return False

    @staticmethod
    def load_input_spreadsheet():
        if INPUT_FILE.exists():
            return pd.read_excel(INPUT_FILE)
        return None