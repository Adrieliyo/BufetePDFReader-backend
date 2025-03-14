from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.middlewares.auth_required import authRequired
from app.config.database import SessionLocal
from app.routes.pdf_routes import router as pdf_router
from app.routes.register_routes import router as register_router
from app.routes.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.mail_test_routes import router as mail_test_router
from app.routes.password_reset_routes import router as password_reset_router

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Configurar según necesidades
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

# Dependencia para obtener la sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Registrar rutas

# Rutas públicas (no requieren autenticación)
app.include_router(register_router)
app.include_router(auth_router)
app.include_router(password_reset_router)

app.include_router(mail_test_router)

# Rutas protegidas (requieren autenticación)
app.include_router(
    pdf_router,
    dependencies=[Depends(authRequired)]
)

app.include_router(
    user_router,
    dependencies=[Depends(authRequired)]
)

app.include_router(
    user_router,
    dependencies=[Depends(authRequired)]
)

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de lectura de PDFs"}