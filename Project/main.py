from fastapi import FastAPI
from Controller.product_controller import router as product_router

app = FastAPI(
    title="API Produtos Worten",
    description="API para gerenciar produtos, buscar preços na Worten e salvar no Excel",
    version="1.0.0"
)

# Registrar router
app.include_router(product_router)

# Rota raiz opcional
@app.get("/")
def root():
    return {"message": "API Produtos Worten funcionando!"}

# Para rodar:
# uvicorn main:app --reload
