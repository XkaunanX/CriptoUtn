from collections import Counter
import math

texto01 = "EL CENTRO DE ESTUDIOS DESARROLLO Y TERRITORIO Y LA FACULTAD REGIONAL LA PLATA - UNIVERSIDAD TECNOLÓGICA NACIONAL, DE COMÚN ACUERDO, SUSCRIBEN ESTA CARTA DE INTENCIÓN, SOBRE LA BASE DE LAS CONSIDERACIONES Y PROPÓSITOS QUE SE EXPONEN A CONTINUACIÓN:"

def cargar_datos_simbolos(texto: str):
    conteo_simbolos = Counter(texto)
    total = sum(conteo_simbolos.values())
    cod = {}
    lista_simbolos = sorted([
                    {
                        'Caracter': simb,
                        'Cantidad': frec,
                        'Probabilidad': (prob := frec / total),
                        'IMutua':  (imutua := -math.log2(prob)),
                        'Entropia': imutua * prob,
                    }
                    for simb, frec in conteo_simbolos.items()
                ], key=lambda x: x['Cantidad'], reverse=True)


    cod["CantSimbolos"] = total
    # TODO: Sacar la list comprehesion a bucle for para no tener que usar dos
    cod["EntropiaTotal"] = sum(simbolo['Entropia'] for simbolo in lista_simbolos)
    cod["ListaSimbolos"] = lista_simbolos
    return cod

a=cargar_datos_simbolos(texto01)
print(a)
print("fin")