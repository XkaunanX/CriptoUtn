def dividir_simbolos(lista_simbolos):
    """Divide la lista de símbolos en dos partes con suma de probabilidades más equilibrada"""
    total = sum(s['Probabilidad'] for s in lista_simbolos)
    mitad = total / 2
    mejor_id = 0
    mejor_diferencia = float('inf')
    acumulado = 0

    for i in range(len(lista_simbolos) - 1):
        acumulado += lista_simbolos[i]['Probabilidad']
        diferencia = abs(mitad - acumulado)
        if diferencia < mejor_diferencia:
            mejor_diferencia = diferencia
            mejor_id = i
        else:
            break  # optimización: si empeora, salir

    return lista_simbolos[:mejor_id + 1], lista_simbolos[mejor_id + 1:]


def asignar_codigos(simbolos, prefijo='', codigos=None):
    """Asigna códigos binarios a cada símbolo usando Shannon-Fano"""
    if codigos is None:
        codigos = {}
    if len(simbolos) == 1:
        codigo_final = prefijo or '0' # el or '0 es para cuando hay solo un caracter
        codigos[simbolos[0]['Caracter']] = codigo_final 
        simbolos[0]['Codigo'] = codigo_final
        return codigos
    izquierda, derecha = dividir_simbolos(simbolos)
    asignar_codigos(izquierda, prefijo + '0', codigos)
    asignar_codigos(derecha, prefijo + '1', codigos)
    return codigos


def codificar_shannon_fano(datos_codificacion: dict) -> dict:
    """Agrega al diccionario los resultados del algoritmo Shannon-Fano"""
    lista_simbolos = datos_codificacion['ListaSimbolos']
    codigos = asignar_codigos(lista_simbolos)

    texto_codificado = ''.join(codigos[char] for char in datos_codificacion['TextoOriginal'])

    longitud_prom_total = 0
    bits_totales = 0

    for s in lista_simbolos:
        longitud = len(s['Codigo'])
        s['LongitudCodigo'] = longitud
        s['BitsTotales'] = s['Cantidad'] * longitud
        s['LongitudPromedioSimbolo'] = longitud * s['Probabilidad']

        longitud_prom_total += s['LongitudPromedioSimbolo']
        bits_totales += s['BitsTotales']

    cod_resultado = {
        "Algoritmo": "Shannon-Fano",
        "Codigos": codigos,
        "TextoCodificado": texto_codificado,
        "LongitudPromedio": longitud_prom_total,
        "CantidadBits": bits_totales,
        "Eficiencia": datos_codificacion['EntropiaTotal'] / longitud_prom_total if longitud_prom_total else 0
    }

    datos_codificacion['Codificaciones']['Shannon-Fano'] = cod_resultado
    return datos_codificacion

def decodificar_shannon_fano(texto_codificado, codigos):
    """Decodifica el texto binario utilizando los códigos de Shannon-Fano"""
    codigos_invertidos = {v: k for k, v in codigos.items()}
    codigo_actual = ''
    texto_decodificado = ''
    for bit in texto_codificado:
        codigo_actual += bit
        if codigo_actual in codigos_invertidos:
            texto_decodificado += codigos_invertidos[codigo_actual]
            codigo_actual = ''
    return texto_decodificado

