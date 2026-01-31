from dataclasses import dataclass, field
# Usei dataclass para facilitar
# criação de objetos e evitar escrever __init__ manualmente.
@dataclass
class Product:
    """
        Representa um produto do sistema.
        Atributos:
        id (int): Identificador único do produto.
        name (str): Nome do produto.
        link (str): URL do produto na Worten.
        price (float): Menor preço encontrado.
        seller (str): Nome do vendedor que oferece o menor preço.
        available (bool): Disponibilidade do produto (True se disponível).
    """ 
    # Todos os atributos estão tipados ( str, float, bool) 
    # isso ajuda a validar e manter o código limpo
    ID: str
    EAN: str
    Name: str
    Status: str
    Score: float
    Seller: str  # Requisito do desafio
    Link: str    
    Mirakl_Image: str = ""
    BB_Image_Url: str = ""