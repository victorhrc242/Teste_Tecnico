from pydantic import BaseModel
from typing import Optional


class ProductSchema(BaseModel):
    """Schema para criação do produto"""
    EAN: str
    Name: str
    Status: str
    Score: float
    Mirakl_Image: str
    BB_Image_Url: str


class ProductUpdateSchema(BaseModel):
    """Schema para atualização do produto"""
    ID: str               # agora string
    EAN: Optional[str] = None
    Name: Optional[str] = None
    Status: Optional[str] = None
    Score: Optional[float] = None
    Mirakl_Image: Optional[str] = None
    BB_Image_Url: Optional[str] = None


class productout(BaseModel):
    """Schema para retorno do produto via API"""
    ID: str
    EAN: str
    Name: str
    Status: str
    Score: float
    Mirakl_Image: str
    BB_Image_Url: str
