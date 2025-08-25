from .monticulo_minimo import MonticuloMinimo, Nodo

def construir_arbol_huffman(frecuencias_simbolos):
    monticulo = MonticuloMinimo()

    for caracter, frecuencia in frecuencias_simbolos.items():
        monticulo.insertar(Nodo(caracter, frecuencia))

    while len(monticulo) > 1:
        nodo1 = monticulo.extraer_minimo()
        nodo2 = monticulo.extraer_minimo()
        nodo_combinado = Nodo(frecuencia=nodo1.frecuencia + nodo2.frecuencia)
        nodo_combinado.izquierda = nodo1
        nodo_combinado.derecha = nodo2
        monticulo.insertar(nodo_combinado)

    return monticulo.extraer_minimo() if len(monticulo) == 1 else None

def construir_codigos(raiz):
    codigos = {}
    def _construir(nodo, codigo_actual):
        if nodo is None:
            return
        if nodo.caracter is not None:
            codigos[nodo.caracter] = codigo_actual
        _construir(nodo.izquierda, codigo_actual + '0')
        _construir(nodo.derecha, codigo_actual + '1')
    _construir(raiz, '')
    return codigos

def codificar_huffman(datos_codificacion):
    lista_simbolos = datos_codificacion["ListaSimbolos"]
    frecuencias = {s['Caracter']: s['Cantidad'] for s in lista_simbolos}

    raiz = construir_arbol_huffman(frecuencias)
    codigos = construir_codigos(raiz)

    texto_codificado = ''.join(codigos[c] for c in datos_codificacion["TextoOriginal"])

    longitud_prom_total = 0
    bits_totales = 0

    for simbolo in lista_simbolos:
        char = simbolo['Caracter']
        codigo = codigos[char]
        longitud = len(codigo)

        simbolo['Codigo'] = codigo
        simbolo['LongitudCodigo'] = longitud
        simbolo['BitsTotales'] = simbolo['Cantidad'] * longitud
        simbolo['LongitudPromedioSimbolo'] = longitud * simbolo['Probabilidad']

        longitud_prom_total += simbolo['LongitudPromedioSimbolo']
        bits_totales += simbolo['BitsTotales']

    cod_resultado = {
        "Algoritmo": "Huffman",
        "Codigos": codigos,
        "TextoCodificado": texto_codificado,
        "LongitudPromedio": longitud_prom_total,
        "CantidadBits": bits_totales,
        "Eficiencia": datos_codificacion['EntropiaTotal'] / longitud_prom_total if longitud_prom_total else 0
    }

    datos_codificacion["Codificaciones"]["Huffman"] = cod_resultado
    return datos_codificacion

def decodificar_huffman(texto_codificado, codigos):
    codigos_invertidos = {v: k for k, v in codigos.items()}
    codigo_actual = ''
    texto_decodificado = ''
    for bit in texto_codificado:
        codigo_actual += bit
        if codigo_actual in codigos_invertidos:
            texto_decodificado += codigos_invertidos[codigo_actual]
            codigo_actual = ''
    return texto_decodificado
