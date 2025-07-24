import json

def comparar_codificaciones(datos_codificacion: dict, imprimir=True, encoding='utf-8'):
    """
    Compara codificaciones aplicadas y guarda métricas en el diccionario.
    También identifica el mejor algoritmo por eficiencia y por compresión.
    """

    texto_original = datos_codificacion['TextoOriginal']
    try:
        bits_originales = len(texto_original.encode(encoding)) * 8
    except UnicodeEncodeError:
        raise ValueError(f"El texto contiene caracteres que no se pueden representar en '{encoding}'.")

    comparaciones = {}
    mejor_eficiencia = -1
    mejor_eficiencia_alg = None

    menor_bits = float('inf')
    mejor_compresion_alg = None

    for nombre_alg, info in datos_codificacion["Codificaciones"].items():
        longitud_cod = info["LongitudPromedio"]
        eficiencia = info["Eficiencia"]
        bits_totales = info["CantidadBits"]
        tasa_compresion = bits_totales / bits_originales if bits_originales else 0

        comparaciones[nombre_alg] = {
            "LongitudPromedio": longitud_cod,
            "Eficiencia": eficiencia,
            "BitsTotales": bits_totales,
            "TasaCompresion": tasa_compresion,
            "BitsOriginales": bits_originales
        }

        if eficiencia > mejor_eficiencia:
            mejor_eficiencia = eficiencia
            mejor_eficiencia_alg = nombre_alg

        if bits_totales < menor_bits:
            menor_bits = bits_totales
            mejor_compresion_alg = nombre_alg

        if imprimir:
            print(f"\nAlgoritmo: {nombre_alg}")
            print(f"  Longitud promedio de código: {longitud_cod:.4f}")
            print(f"  Eficiencia: {eficiencia:.4f}")
            print(f"  Bits totales codificados: {bits_totales}")
            print(f"  Tasa de compresión: {tasa_compresion:.4f} ({tasa_compresion * 100:.2f}%)")
            print(f"  Bits originales ({encoding}): {bits_originales}")

    datos_codificacion['Comparaciones'] = comparaciones
    datos_codificacion['ResumenComparacion'] = {
        "MejorEficiencia": mejor_eficiencia_alg,
        "MejorCompresion": mejor_compresion_alg
    }

    if imprimir:
        print("\n===== MEJORES RESULTADOS =====")
        print(f"  Mejor eficiencia: {mejor_eficiencia_alg}")
        print(f"  Mejor compresión (menos bits): {mejor_compresion_alg}")

    return datos_codificacion


def obtener_codigos_ordenados(datos_codificacion: dict, algoritmo: str) -> dict:
    """
    Devuelve los códigos de un algoritmo ordenados por frecuencia descendente.
    Ideal para mostrarlos en una tabla de interfaz gráfica.
    
    Parámetros:
        datos_codificacion: dict con resultados de codificación
        algoritmo: 'Huffman' o 'Shannon-Fano'

    Retorna:
        dict {caracter: codigo}, ordenado por frecuencia descendente
    """
    if algoritmo not in datos_codificacion["Codificaciones"]:
        raise ValueError(f"Algoritmo '{algoritmo}' no encontrado en los resultados.")

    codigos = datos_codificacion["Codificaciones"][algoritmo]["Codigos"]
    simbolos_ordenados = sorted(
        datos_codificacion["ListaSimbolos"],
        key=lambda s: s["Cantidad"],
        reverse=True
    )

    codigos_ordenados = {}
    for simbolo in simbolos_ordenados:
        char = simbolo["Caracter"]
        if char in codigos:
            codigos_ordenados[char] = codigos[char]

    return codigos_ordenados


def guardar_codigos_codificacion(datos_codificacion: dict, algoritmo: str, ruta_salida: str):
    """
    Guarda únicamente los códigos de un algoritmo específico en un archivo JSON.

    Parámetros:
        - datos_codificacion: dict generado por cargar_datos_simbolos + codificación
        - algoritmo: str, por ejemplo "Huffman" o "Shannon-Fano"
        - ruta_salida: str, nombre del archivo a crear (ej: "huffman.json")
    """
    if algoritmo not in datos_codificacion["Codificaciones"]:
        raise ValueError(f"No se encontró la codificación '{algoritmo}' en los datos.")

    codificacion = datos_codificacion["Codificaciones"][algoritmo]

    datos_a_guardar = {
        "Algoritmo": codificacion["Algoritmo"],
        "Códigos": codificacion["Códigos"]
    }

    with open(ruta_salida, 'w', encoding='utf-8') as archivo:
        json.dump(datos_a_guardar, archivo, ensure_ascii=False, indent=4)

    print(f"Códigos guardados en: {ruta_salida}")



def guardar_codigos_codificacion_texto_codificado(datos_codificacion: dict, algoritmo: str, ruta_salida: str):
    """
    Guarda los códigos y el texto codificaco de un algoritmo específico en un archivo JSON.

    Parámetros:
        - datos_codificacion: dict general generado por cargar_datos_simbolos + codificación
        - algoritmo: str, por ejemplo "Huffman" o "Shannon-Fano"
        - ruta_salida: str, nombre del archivo a crear (ej: "huffman.json")
    """
    if algoritmo not in datos_codificacion["Codificaciones"]:
        raise ValueError(f"No se encontró la codificación '{algoritmo}' en los datos.")

    codificacion = datos_codificacion["Codificaciones"][algoritmo]

    datos_a_guardar = {
        "Algoritmo": codificacion["Algoritmo"],
        "Codigos": codificacion["Codigos"],
        "TextoCodificado": codificacion["TextoCodificado"]
    }

    with open(ruta_salida, 'w', encoding='utf-8') as archivo:
        json.dump(datos_a_guardar, archivo, ensure_ascii=False, indent=4)

    print(f"Códigos guardados en: {ruta_salida}")


def cargar_codigos_codificacion(ruta_archivo: str) -> dict:
    """
    Carga los códigos binarios de un archivo JSON para decodificación.

    El archivo debe contener al menos:
    {
        "Algoritmo": "Huffman" o "Shannon-Fano",
        "Codigos": { "A": "111", "B": "10", ... }
    }

    Retorna un diccionario con las claves:
    - 'Algoritmo': nombre del algoritmo
    - 'Codigos': diccionario de codificación
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)

        if "Algoritmo" not in datos or "Códigos" not in datos:
            raise ValueError("Faltan claves requeridas: 'Algoritmo' y/o 'Códigos'")

        return {
            "Algoritmo": datos["Algoritmo"],
            "Códigos": datos["Códigos"]
        }

    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_archivo}")
    except json.JSONDecodeError:
        raise ValueError(f"El archivo no tiene formato JSON válido: {ruta_archivo}")
