from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.services.pdf_service import leer_pdf, extraer_datos_del_pdf

router = APIRouter(prefix="/pdf", tags=["PDF"])

@router.post("/read")
async def read_pdf(file: UploadFile = File(...)):
    return await leer_pdf(file)

@router.post("/extraer-datos")
async def extraer_datos_pdf(file: UploadFile = File(...)):
    return await extraer_datos_del_pdf(file)