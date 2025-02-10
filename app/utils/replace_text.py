# Reemplaza sólo una aparición de la etiqueta en los párrafos pero mantiene el formato original.
def reemplazar_texto(paragraph, etiqueta, valor):
    if etiqueta in paragraph.text:
        # Iterar sobre cada "run" (segmento de texto con mismo formato)
        for run in paragraph.runs:
            if etiqueta in run.text:
                run.text = run.text.replace(etiqueta, valor)

def reemplazar_en_tablas(document, reemplazos):
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for etiqueta, valor in reemplazos.items():
                        # Convierte el valor a mayúsculas antes de reemplazar
                        reemplazar_texto(paragraph, etiqueta, valor.upper())