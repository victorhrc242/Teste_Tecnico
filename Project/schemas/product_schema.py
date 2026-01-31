from pydantic import BaseModel
from typing import Optional

class ProductSchema(BaseModel):
    """Schema para criação manual via API"""
    Name: str

class ProductUpdateSchema(BaseModel):
    """Schema para atualização do produto"""
    EAN: Optional[str] = None
    Name: Optional[str] = None
    Status: Optional[str] = None
    Score: Optional[float] = None
    Seller: Optional[str] = None
    Link: Optional[str] = None

class productout(BaseModel):
    ID: str
    EAN: str
    Name: str
    Status: str
    Score: float
    Seller: str    # <--- Certifique-se que estas linhas existem
    Link: str      # <--- Certifique-se que estas linhas existem
    Mirakl_Image: Optional[str] = ""
    BB_Image_Url: Optional[str] = ""

    class Config:
        from_attributes = True