import re
from fastapi import HTTPException

def extraer_datos(texto: str) -> dict:
    try:
        patrones = {
            "lugar_fecha": r"(?<!\w)(Los Mochis, Sinaloa, \d{1,2} de \w+ del \d{4})(?!\w)",
            "representante_legal": r"2\.-\s*Nombre del representante legal de la empresa:\s*(.*?)\s*(?=Correo:|$)",
            "correo": r"[Cc]orreo:\s+([\w\.-]+@[\w\.-]+)",
            "telefono": r"[Tt]eléfono:\s+(\d{3}\s*\d{3}\s*\d{4})",
            "cargo": r"[Cc]argo:\s*(.*?)\s*(?=\d|$)",
            "vigencia": r"3\.-\s*Vigencia del convenio solicitado:\s*(.*?)\s*(?:\n|$)",
            "apoyo_economico": r"4\.-\s*Apoyo económico mensual propuesto:\s*([^5].*?)(?=\s*5\.-|$)",
            "responsable_practicas": r"5\.-\s*Nombre del responsable de prácticas profesionales \(.*?\):\s*(.*?)\s*Correo:",
            "correo_responsable": r"Correo:\s*([\w\.-]+@[\w\.-]+)",
            "telefono_responsable": r"5\.-.*?Teléfono:\s*(\d{10})",
            "cargo_responsable": r"5\.-.*?Cargo:\s*(.*?)(?:\n|$)",
            "carrera_practicante": r"6\.-\s*Carrera del practicante:\s*(.*?)\s*(?:7\.-|$)",
            "nombre_practicante": r"7\.-\s*Nombre del Practicante:\s*(.*?)(?:\n|$)"
        }

        datos = {}
        for campo, patron in patrones.items():
            match = re.search(patron, texto, re.IGNORECASE | re.DOTALL)
            # if not match:
            #     raise ValueError(f"No se encontró el campo: {campo}")
            # datos[campo] = match.group(1).strip()
            if match:
                datos[campo] = match.group(1).strip()
            else:
                datos[campo] = ""
            
        return datos

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")