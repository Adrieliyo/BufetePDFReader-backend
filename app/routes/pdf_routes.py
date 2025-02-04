from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from io import BytesIO
from docx import Document
from app.services.pdf_service import leer_pdf, extraer_datos_del_pdf
from app.utils.replace_text import reemplazar_texto
from app.utils.numbers_to_words import numero_a_letras, mes_a_letras, anio_a_letras
import os
from datetime import datetime
import random
import string
import re

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
        fecha_actual = datetime.now()
        dia_letra = numero_a_letras(fecha_actual.day)
        mes_letra = mes_a_letras(fecha_actual.month)
        anio_letra = anio_a_letras(fecha_actual.year)

        vigencia = datos_extraidos["datos"].get("vigencia", "")
        numero_match = re.search(r'(\d+)', vigencia)
        if numero_match:
            numero = int(numero_match.group(1))
            numero_vigencia = str(numero)
            letra_vigencia = numero_a_letras(numero).upper()
        else:
            numero_vigencia = ""
            letra_vigencia = ""

        # Preparar diccionario de reemplazos
        reemplazos = {
            "{{NOMBRE_ESCUELA}}": datos_extraidos["datos"].get("nombre_escuela", ""),
            "{{DOMICILIO_ESCUELA}}": datos_extraidos["datos"].get("domicilio_escuela", ""),
            "{{NOMBRE_DIRECTOR}}": datos_extraidos["datos"].get("nombre_director", ""),
            "{{UNIDAD_REGIONAL}}": datos_extraidos["datos"].get("unidad_regional", ""),
            "{{REPRESENTANTE_LEGAL}}": datos_extraidos["datos"].get("representante_legal", ""),
            "{{CARGO}}": datos_extraidos["datos"].get("cargo", ""),
            "{{LETRA_VIGENCIA}}": letra_vigencia,
            "{{NUMERO_VIGENCIA}}": numero_vigencia,
            "{{DIAS_LETRA}}": dia_letra.upper(),
            "{{MES_LETRA}}": mes_letra.upper(),
            "{{ANIO_LETRA}}": anio_letra.upper()
        }

        # lugar_y_fecha = datos_extraidos["datos"].get("lugar_fecha", "")
        apoyo_economico = datos_extraidos["datos"].get("apoyo_economico", "").strip()
        # representante_legal = datos_extraidos["datos"].get("representante_legal", "")

        # # Imprimir los datos extraídos para depuración
        print(f"Datos extraídos: {datos_extraidos}")
        print()
        print(f"Apoyo económico: {apoyo_economico}")
        print()
        print(f"Reemplazos:", reemplazos)

        # Determinar el archivo DOCX a usar
        if apoyo_economico:
            docx_path = os.path.join("app/docx_files", "ConvenioRemunerado.docx")
        else:
            docx_path = os.path.join("app/docx_files", "ConvenioNoRemunerado.docx")
            
        # Cargar el documento Word desde el sistema de archivos
        document = Document(docx_path)

        # Insertar la fecha donde está la etiqueta {{FECHA}}
        # fecha_formato = datetime.now().strftime("%d/%m/%Y")

        # Reemplazar en párrafos
        # for paragraph in document.paragraphs:
        #     reemplazar_texto(paragraph, "{{FECHA}}", fecha_formato)

        # Insertar lugar y fecha al inicio del documento
        # first_paragraph = document.paragraphs[0]
        # first_paragraph.insert_paragraph_before(texto_a_insertar)

        # Reemplazar en párrafos
        for paragraph in document.paragraphs:
            for etiqueta, valor in reemplazos.items():
                reemplazar_texto(paragraph, etiqueta, valor)

        # Guardar el documento modificado en memoria
        output_stream = BytesIO()
        document.save(output_stream)
        output_stream.seek(0)

        # Obtener la fecha actual y formatearla
        fecha_actual_formateada = datetime.now().strftime("%Y-%m-%d")

        # Generar 3 letras aleatorias
        letras_aleatorias = ''.join(random.choices(string.ascii_uppercase, k=3))

        # Nombre del archivo con la fecha actual
        nombre_archivo = f"{os.path.splitext(os.path.basename(docx_path))[0]}_{fecha_actual_formateada}_{letras_aleatorias}.docx"

        # Devolver el documento modificado como respuesta
        return StreamingResponse(
            output_stream,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={nombre_archivo}"}
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar los archivos: {str(e)}")