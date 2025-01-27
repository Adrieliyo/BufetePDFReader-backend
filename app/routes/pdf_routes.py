from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from io import BytesIO
from docx import Document
from app.services.pdf_service import leer_pdf, extraer_datos_del_pdf
import os

router = APIRouter(prefix="/pdf", tags=["PDF"])

@router.post("/read")
async def read_pdf(file: UploadFile = File(...)):
    return await leer_pdf(file)

@router.post("/extraer-datos")
async def extraer_datos_pdf(file: UploadFile = File(...)):
    return await extraer_datos_del_pdf(file)

@router.post("/extract-data-and-modify-docx")
async def extract_data_and_modify_docx(
    pdf_file: UploadFile = File(...),
):
    try:
        if not pdf_file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")

        # Extraer datos del PDF
        datos_extraidos = await extraer_datos_del_pdf(pdf_file)
        lugar_y_fecha = datos_extraidos["datos"]["lugar_fecha"]

        docx_path = os.path.join("app/docx_files", "ConvenioRemunerado.docx")

        # Cargar el documento Word desde el sistema de archivos
        document = Document(docx_path)

        # Insertar lugar y fecha al inicio del documento
        first_paragraph = document.paragraphs[0]
        first_paragraph.insert_paragraph_before(lugar_y_fecha)

        # Guardar el documento modificado en memoria
        output_stream = BytesIO()
        document.save(output_stream)
        output_stream.seek(0)

        # Devolver el documento modificado como respuesta
        return StreamingResponse(
            output_stream,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": "attachment; filename=Convenio_modificado.docx"}
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar los archivos: {str(e)}")