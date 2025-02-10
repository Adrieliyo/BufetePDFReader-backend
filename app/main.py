from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.routes.pdf_routes import router as pdf_router

app = FastAPI()

# Dependencia para obtener la sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Registrar rutas
app.include_router(pdf_router)

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de lectura de PDFs"}