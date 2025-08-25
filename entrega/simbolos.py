from collections import Counter
import math

def informacion_simbolos(texto):
    total_simbolos = len(texto)
    lista_simbolos = []
    
    conteos = Counter(texto)
    
    for simbolo, cantidad in conteos.items():
        probabilidad = cantidad / total_simbolos
        probabilidad_inversa = 1 / probabilidad
        info_mutua = -math.log2(probabilidad)
        entropia = probabilidad * info_mutua
        
        lista_simbolos.append({
            "Simbolo": simbolo,
            "Cantidad": cantidad,
            "Probabilidad": probabilidad,
            "ProbabilidadInversa": probabilidad_inversa,
            "InformacionMutua": info_mutua,
            "Entropia": entropia
        })
    
    # Ordenar por cantidad descendente
    lista_simbolos.sort(key=lambda x: x["Cantidad"], reverse=True)
    
    probabilidad_total = sum(s["Probabilidad"] for s in lista_simbolos) # Verificar que sea 1 sino hay error
    
    if probabilidad_total !=1:
        raise ValueError("symbols.py - La probabilidad total es distinta de 1")
    
    entropia_total = sum(s["Entropia"] for s in lista_simbolos)
    
    diccionario = {
        "TotalSimbolos": total_simbolos,
        "ProbabilidadTotal": probabilidad_total,
        "EntropiaTotal": entropia_total,
        "ListaSimbolos": lista_simbolos
    }
    
    return diccionario