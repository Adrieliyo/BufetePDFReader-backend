def numero_a_letras(numero):
    unidades = ['', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve']
    decenas = ['', 'diez', 'veinte', 'treinta', 'cuarenta', 'cincuenta', 'sesenta', 'setenta', 'ochenta', 'noventa']
    especiales = {
        11: 'once', 12: 'doce', 13: 'trece', 14: 'catorce', 15: 'quince',
        16: 'dieciséis', 17: 'diecisiete', 18: 'dieciocho', 19: 'diecinueve',
        21: 'veintiuno', 22: 'veintidós', 23: 'veintitrés', 24: 'veinticuatro',
        25: 'veinticinco', 26: 'veintiséis', 27: 'veintisiete', 28: 'veintiocho',
        29: 'veintinueve',
    }
    
    if numero in especiales:
        return especiales[numero]
    
    if numero < 10:
        return unidades[numero]
    
    if numero < 100:
        if numero % 10 == 0:
            return decenas[numero // 10]
        return f"{decenas[numero // 10]} y {unidades[numero % 10]}"
    
    return str(numero)

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