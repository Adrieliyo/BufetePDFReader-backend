import re
from fastapi import HTTPException

def extraer_datos(texto: str) -> dict:
    try:
        patrones = {
            "lugar_fecha": r"(?<!\w)(Los Mochis, Sinaloa, \d{1,2} de \w+ del \d{4})(?!\w)",
            "nombre_empresa": r"Nombre de la empresa, dependencia pública o institución social:\s*(.*?)\s*(?=Actividad Económica:)",
            "actividad_economica": r"Actividad Económica:\s*(.*?)\s*(?=Fecha de inicio de operaciones:)",
            "fecha_inicio": r"Fecha de inicio de operaciones:\s*\d{2} de (\w+) de (\d{4})",
            "domicilio": r"Domicilio:\s*(.*?)\s*(?=RFC:)",
            "rfc": r"RFC:\s*([A-Z0-9]+)",
            "representante_legal": r"Representante legal:\s*(.*?)\s*(?=Correo:)",
            "correo": r"[Cc]orreo:\s+([\w\.-]+@[\w\.-]+)",
            "telefono": r"[Tt]eléfono:\s+(\d{3}\s*\d{3}\s*\d{4})",
            "cargo": r"[Cc]argo:\s*(.*?)\s*(?=\d|$)",
            "vigencia": r"3\.-\s*Vigencia del convenio solicitado:\s*(.*?)\s*(?:\n|$)",
            "apoyo_economico": r"Apoyo económico mensual propuesto:\s*([^\n]+?)(?:\n|1-2|$)",          "responsable_practicas": r"Jefe inmediato:\s*(.*?)\s*(?=Correo:)",
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

            # if match:
            #     datos[campo] = match.group(1).strip()
            # else:
            #     datos[campo] = ""

            if match:
                valor = match.group(1).strip()
                valor = re.sub(r'\s+', ' ', valor)  # Reemplaza múltiples espacios y saltos de línea con un solo espacio
                if campo == "fecha_inicio":
                    datos[campo] = f"{match.group(1)} {match.group(2)}"
                else:
                    datos[campo] = valor
            else:
                datos[campo] = ""
        
        # Datos extra estáticos a agregar
        datos["nombre_escuela"] = "Facultad de Ingeniería Los Mochis"
        datos["domicilio_escuela"] = "Fuente de Poseidón y Ángel Flores, Col. Jiquilpan Módulo B2 C.P. 81220."
        datos["unidad_regional"] = "Unidad Regional Norte"
        datos["nombre_director"] = "Dr. Rody Abraham Soto Rojo"

        return datos

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")