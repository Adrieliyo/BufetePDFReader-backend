from fastapi import HTTPException
from fastapi.responses import JSONResponse
from PyPDF2 import PdfReader
import pdfplumber
from app.utils.regex_utils import extraer_datos

async def leer_pdf(file):
    try:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")

        pdf_reader = PdfReader(file.file)
        text_content = [page.extract_text() for page in pdf_reader.pages]

        return JSONResponse(content={
            "total_pages": len(pdf_reader.pages),
            "content": text_content
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el PDF: {str(e)}")

async def extraer_datos_del_pdf(file):
    try:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")

        texto_completo = ""
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                texto_completo += page.extract_text() + "\n"

        datos_extraidos = extraer_datos(texto_completo)

        # return JSONResponse(content={
        #     "status": "success",
        #     "datos": datos_extraidos
        # })

         # Verificar que se haya podido extraer al menos algunos datos importantes
        datos_importantes = ["nombre_empresa", "representante_legal"]
        datos_encontrados = [campo for campo in datos_importantes if datos_extraidos.get(campo)]
        
        if not datos_encontrados:
            raise HTTPException(
                status_code=400, 
                detail="El PDF no parece contener el formato esperado para la extracción de datos"
            )
        
        return {
            "status": "success",
            "datos": datos_extraidos
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")