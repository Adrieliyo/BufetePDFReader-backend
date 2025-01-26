from fastapi import FastAPI
from app.routes.pdf_routes import router as pdf_router

app = FastAPI()

# Registrar rutas
app.include_router(pdf_router)

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de lectura de PDFs"}