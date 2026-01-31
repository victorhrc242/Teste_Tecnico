from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from typing import List
import shutil
import os
from Service.product_service import ProductService
from schemas.product_schema import ProductSchema, productout
from pathlib import Path

router = APIRouter(prefix="/products", tags=["Products"])
TEMP_UPLOAD = "data/original_upload.xlsx"

@router.get("/", response_model=List[productout])
def list_products():
    return ProductService.get_all_products()

@router.post("/", response_model=productout)
def create_from_name(product_in: ProductSchema):
    product = ProductService.add_product_by_name(product_in.Name)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

@router.post("/import")
async def import_spreadsheet(file: UploadFile = File(...)):
    """Faz o upload da planilha do desafio e processa tudo."""
    with open(TEMP_UPLOAD, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    success = ProductService.process_initial_spreadsheet(TEMP_UPLOAD)
    if not success:
        raise HTTPException(status_code=500, detail="Erro ao processar arquivo")
    
    return {"message": "Processamento em lote iniciado/concluído com sucesso"}

@router.get("/download")
def download_results():
    file_path = Path("data/worten_final.xlsx")
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Arquivo final ainda não gerado")
    return FileResponse(file_path, filename="resultados_worten.xlsx")