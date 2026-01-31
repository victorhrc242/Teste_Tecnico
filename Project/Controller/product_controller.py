from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import List
import os
from Service.product_service import ProductService
from Repositore.product_repository import ProductRepository, OUTPUT_FILE
from schemas.product_schema import ProductSchema, productout, ProductUpdateSchema

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[productout])
def list_products():
    """Lista todos os produtos salvos no Excel final."""
    return ProductRepository.get_all_products()

@router.post("/import-local")
def import_from_spreadsheet():
    """Lê worten.xlsx e processa apenas produtos que ainda não estão no sistema."""
    success = ProductService.process_initial_spreadsheet()
    if not success:
        raise HTTPException(status_code=404, detail="Planilha de entrada 'data/worten.xlsx' não encontrada.")
    return {"message": "Processamento concluído com sucesso. Itens duplicados foram ignorados."}

@router.get("/download")
def download_excel():
    """Gera o download do arquivo Excel atualizado."""
    if not OUTPUT_FILE.exists():
        raise HTTPException(status_code=404, detail="O arquivo de resultados ainda não foi gerado.")
    
    return FileResponse(
        path=OUTPUT_FILE,
        filename="resultados_worten_final.xlsx",
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@router.post("/", response_model=productout)
def create_manual_product(payload: ProductSchema):
    """Busca e adiciona um produto específico pelo nome enviado no JSON."""
    product = ProductService.add_single_product(payload.Name)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado na Worten.")
    return product

@router.put("/{product_id}", response_model=bool)
def update_product(product_id: str, payload: ProductUpdateSchema):
    """Atualiza dados de um produto existente no Excel."""
    success = ProductRepository.update_product(product_id, payload.dict(exclude_unset=True))
    if not success:
        raise HTTPException(status_code=404, detail="ID de produto não encontrado para atualização.")
    return success

@router.delete("/{product_id}")
def delete_product(product_id: str):
    """Remove um produto do Excel."""
    success = ProductRepository.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="ID de produto não encontrado para remoção.")
    return {"message": f"Produto {product_id} removido com sucesso."}