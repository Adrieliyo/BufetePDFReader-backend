# Función para reemplazar el texto dentro de un párrafo de un documento Word.
def reemplazar_texto(paragraph, etiqueta, valor):
    if etiqueta in paragraph.text:
        # Iterar sobre cada "run" (segmento de texto con mismo formato)
        for run in paragraph.runs:
            if etiqueta in run.text:
                run.text = run.text.replace(etiqueta, valor)

# Función más cercana
# def reemplazar_texto(paragraph, etiqueta, valor):
#     if etiqueta not in paragraph.text:
#         return  # Si la etiqueta no está en el párrafo, no hacer nada
    
#     # Unir el texto completo del párrafo con sus runs
#     full_text = "".join(run.text for run in paragraph.runs)
    
#     # Reemplazar todas las apariciones de la etiqueta en el texto completo
#     new_text = full_text.replace(etiqueta, valor)

#     # Inicializar índice para reconstruir los runs
#     index = 0
#     for run in paragraph.runs:
#         run_length = len(run.text)
#         if index < len(new_text):  # Asegurar que no exceda el texto modificado
#             run.text = new_text[index:index + run_length]
#         else:
#             run.text = ""  # Vaciar runs sobrantes si el nuevo texto es más corto
#         index += run_length
