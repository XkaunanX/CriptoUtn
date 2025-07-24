from collections import Counter
import math

def cargar_datos_simbolos(texto: str):
    """Genera estructura base con conteo, probabilidades e información de los símbolos"""
    conteo_simbolos = Counter(texto)
    total = sum(conteo_simbolos.values())

    lista_simbolos = []
    entropia_total = 0

    for simb, frec in conteo_simbolos.items():
        prob = frec / total
        imutua = -math.log2(prob)
        entropia = imutua * prob

        lista_simbolos.append({
            'Caracter': simb,
            'Cantidad': frec,
            'Probabilidad': prob,
            'IMutua': imutua,
            'Entropia': entropia,
        })

        entropia_total += entropia

    lista_simbolos.sort(key=lambda x: x['Cantidad'], reverse=True)

    return {
        "TextoOriginal": texto,
        "CantSimbolos": total,
        "EntropiaTotal": entropia_total,
        "ListaSimbolos": lista_simbolos,
        "Codificaciones": {},
        "Comparaciones": {}  # agregado para guardar comparaciones
    }