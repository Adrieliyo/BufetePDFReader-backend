import re
from fastapi import HTTPException

def extraer_datos(texto: str) -> dict:
    try:
        patrones = {
            "representante_legal": r"2\.-\s*Nombre del representante legal de la empresa:\s*(.*?)\s*(?=Correo:|$)",
            "correo": r"[Cc]orreo:\s+([\w\.-]+@[\w\.-]+)",
            "telefono": r"[Tt]eléfono:\s+(\d{3}\s*\d{3}\s*\d{4})",
            "cargo": r"[Cc]argo:\s*(.*?)\s*(?=\d|$)",
            "vigencia": r"3\.-\s*Vigencia del convenio solicitado:\s*(.*?)\s*(?:\n|$)",
            "apoyo_economico": r"4\.-\s*Apoyo económico mensual propuesto:\s*(.*?)\s*(?:\n|$)"
        }

        datos = {}
        for campo, patron in patrones.items():
            match = re.search(patron, texto, re.IGNORECASE | re.DOTALL)
            if not match:
                raise ValueError(f"No se encontró el campo: {campo}")
            datos[campo] = match.group(1).strip()

        return datos

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")