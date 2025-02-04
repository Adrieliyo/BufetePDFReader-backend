# Reemplaza sólo una aparición de la etiqueta en los párrafos pero mantiene el formato original.
def reemplazar_texto(paragraph, etiqueta, valor):
    if etiqueta in paragraph.text:
        # Iterar sobre cada "run" (segmento de texto con mismo formato)
        for run in paragraph.runs:
            if etiqueta in run.text:
                run.text = run.text.replace(etiqueta, valor)

# Reemplaza todas las apariciones de las etiquetas. Sin embargo, quita el formato del texto original.
# def reemplazar_texto(paragraph, etiqueta, valor):
#     if etiqueta in paragraph.text:
#         # Concatenar todo el texto del párrafo para verificar si la etiqueta está presente
#         full_text = ''.join(run.text for run in paragraph.runs)
        
#         if etiqueta in full_text:
#             # Dividir el texto en partes antes, durante y después de la etiqueta
#             parts = full_text.split(etiqueta)
            
#             # Limpiar todos los runs del párrafo
#             for run in paragraph.runs:
#                 run.text = ""
            
#             # Agregar las partes del texto con el valor reemplazado
#             for i, part in enumerate(parts):
#                 if i > 0:
#                     # Agregar el valor reemplazado
#                     paragraph.add_run(valor)
#                 # Agregar la parte del texto
#                 paragraph.add_run(part)


# Reemplaza todas las apariciones de la etiqueta pero borra el formato original y borra texto.
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