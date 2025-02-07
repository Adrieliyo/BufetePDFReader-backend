def numero_a_letras(numero):
    unidades = ['', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve']
    decenas = ['', 'diez', 'veinte', 'treinta', 'cuarenta', 'cincuenta', 'sesenta', 'setenta', 'ochenta', 'noventa']
    centenas = ['', 'ciento', 'doscientos', 'trescientos', 'cuatrocientos', 'quinientos', 
                'seiscientos', 'setecientos', 'ochocientos', 'novecientos']
    especiales = {
        11: 'once', 12: 'doce', 13: 'trece', 14: 'catorce', 15: 'quince',
        16: 'dieciséis', 17: 'diecisiete', 18: 'dieciocho', 19: 'diecinueve',
        21: 'veintiuno', 22: 'veintidós', 23: 'veintitrés', 24: 'veinticuatro',
        25: 'veinticinco', 26: 'veintiséis', 27: 'veintisiete', 28: 'veintiocho',
        29: 'veintinueve',
    }

    def convertir_grupo(n):
        if n == 0:
            return ''
        
        if n in especiales:
            return especiales[n]
        
        if n < 10:
            return unidades[n]
        
        if n < 100:
            if n % 10 == 0:
                return decenas[n // 10]
            return f"{decenas[n // 10]} y {unidades[n % 10]}"
        
        if n == 100:
            return "cien"
            
        if n < 1000:
            resto = n % 100
            if resto == 0:
                return centenas[n // 100]
            return f"{centenas[n // 100]} {convertir_grupo(resto)}"
        
        return str(n)

    if numero < 1000:
        return convertir_grupo(numero)
        
    if numero < 1000000:
        miles = numero // 1000
        resto = numero % 1000
        if miles == 1:
            texto_miles = "mil"
        else:
            texto_miles = f"{convertir_grupo(miles)} mil"
            
        if resto == 0:
            return texto_miles
        return f"{texto_miles} {convertir_grupo(resto)}"
        
    if numero < 1000000000:
        millones = numero // 1000000
        resto = numero % 1000000
        if millones == 1:
            texto_millones = "un millón"
        else:
            texto_millones = f"{convertir_grupo(millones)} millones"
            
        if resto == 0:
            return texto_millones
        return f"{texto_millones} {numero_a_letras(resto)}"
    
    return str(numero)
    
    # if numero in especiales:
    #     return especiales[numero]
    
    # if numero < 10:
    #     return unidades[numero]
    
    # if numero < 100:
    #     if numero % 10 == 0:
    #         return decenas[numero // 10]
    #     return f"{decenas[numero // 10]} y {unidades[numero % 10]}"
    
    # return str(numero)

def mes_a_letras(mes):
    meses = {
        1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril', 
        5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
        9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
    }
    return meses.get(mes, '')

def anio_a_letras(anio):
    # Obtener los últimos dos dígitos
    ultimos_dos_digitos = anio % 100
    return numero_a_letras(ultimos_dos_digitos)