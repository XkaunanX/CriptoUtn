import time

def codificar_shannon_fano(datos: dict):
    inicio = time.time()
    datos['Codigos'] = asignar_codigos(datos['ListaSimbolos'])
    
    longitud_promedio = 0
    total_bits = 0
    
    for simbolo in datos['ListaSimbolos']:
        largo_codigo = len(simbolo['Code'])
        simbolo['LongitudCodigo'] = largo_codigo
        simbolo['TotalBits'] = simbolo['Cantidad'] * largo_codigo
        simbolo['LongitudPromedio'] = largo_codigo * simbolo['Probabilidad']
        
        longitud_promedio += simbolo['LongitudPromedio']
        total_bits += simbolo['TotalBits']
    
    datos['LongitudPromedio'] = longitud_promedio
    datos['TotalBits'] = total_bits
    datos['Eficiencia'] = datos['EntropiaTotal'] / longitud_promedio if longitud_promedio else 0
    
    fin = time.time()
    datos['TiempoCodificacion'] = round(fin - inicio, 3)
    return datos

def decodificar_shannon_fano(datos: dict, texto_codificado: str):
    inicio = time.time()
    codigo_a_simbolo = {v: k for k, v in datos['Codigos'].items()}
    resultado = []
    buffer = ''
    
    for bit in texto_codificado:
        buffer += bit
        if buffer in codigo_a_simbolo:
            resultado.append(codigo_a_simbolo[buffer])
            buffer = ''
    
    fin = time.time()
    datos['TiempoDecodificacion'] = round(fin - inicio, 3)
    return ''.join(resultado)

def asignar_codigos(simbolos, prefijo='', diccionario_codigos=None):
    if diccionario_codigos is None:
        diccionario_codigos = {}
    if len(simbolos) == 1:
        codigo = prefijo or '0'
        simbolo = simbolos[0]
        diccionario_codigos[simbolo['Simbolo']] = codigo
        simbolo['Code'] = codigo
        return diccionario_codigos

    izquierdo, derecho = dividir_simbolos(simbolos)
    asignar_codigos(izquierdo, prefijo + '0', diccionario_codigos)
    asignar_codigos(derecho, prefijo + '1', diccionario_codigos)
    return diccionario_codigos

def dividir_simbolos(simbolos):
    mitad = sum(s['Probabilidad'] for s in simbolos) / 2
    acumulado = 0
    indice_mejor = 0
    min_diff = float('inf')

    for i in range(len(simbolos) - 1):
        acumulado += simbolos[i]['Probabilidad']
        diff = abs(mitad - acumulado)
        if diff < min_diff:
            min_diff = diff
            indice_mejor = i

    return simbolos[:indice_mejor + 1], simbolos[indice_mejor + 1:]

def generar_texto_codificado(datos: dict, texto: str) -> str:
    codigos = datos['Codigos']
    return ''.join(codigos[s] for s in texto)