from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.routes.pdf_routes import router as pdf_router
from app.routes.register_routes import router as register_router
from app.routes.auth_routes import router as auth_router

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configurar según necesidades
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para obtener la sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Registrar rutas
app.include_router(pdf_router)
app.include_router(register_router)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de lectura de PDFs"}