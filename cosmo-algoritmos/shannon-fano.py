from collections import Counter
import math

texto01 = "EL CENTRO DE ESTUDIOS DESARROLLO Y TERRITORIO Y LA FACULTAD REGIONAL LA PLATA - UNIVERSIDAD TECNOLÓGICA NACIONAL, DE COMÚN ACUERDO, SUSCRIBEN ESTA CARTA DE INTENCIÓN, SOBRE LA BASE DE LAS CONSIDERACIONES Y PROPÓSITOS QUE SE EXPONEN A CONTINUACIÓN:"

def cargar_datos_simbolos(texto: str):
    conteo_simbolos = Counter(texto)
    total = sum(conteo_simbolos.values())
    cod = {"TextoOriginal": texto}
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

def dividir_simbolos(lista_simbolos):
    """Divide la lista de símbolos en dos partes con suma de probabilidades más equilibrada"""
    total = sum(s['Probabilidad'] for s in lista_simbolos)
    mitad = total / 2
    mejor_id = 0
    mejor_diferencia = float('inf')
    acumulado = 0

    for i in range(len(lista_simbolos) - 1):  # No tiene sentido dividir en len - 1 y vacío
        acumulado += lista_simbolos[i]['Probabilidad']
        diferencia = abs(mitad - acumulado)
        if diferencia < mejor_diferencia:
            mejor_diferencia = diferencia
            mejor_idx = i

    return lista_simbolos[:mejor_id + 1], lista_simbolos[mejor_id + 1:]


# TODO: Quitar codigos que esta dentro de ListaSimbolos
# ahora lo dejo que es mas facil codificar despues.
def asignar_codigos(simbolos, prefijo='', codigos=None):
    """Asigna códigos binarios a cada símbolo usando Shannon-Fano"""
    if codigos is None:
        codigos = {}
    if len(simbolos) == 1:
        codigo_final = prefijo or '0'
        codigos[simbolos[0]['Caracter']] = codigo_final
        simbolos[0]['Codigo'] = codigo_final
        return codigos
    izquierda, derecha = dividir_simbolos(simbolos)
    asignar_codigos(izquierda, prefijo + '0', codigos)
    asignar_codigos(derecha, prefijo + '1', codigos)
    return codigos



def codificar_shannon_fano(cod: list):
    """Agrega al diccionario 'cod' los códigos Shannon-Fano y el texto codificado"""
    cod['Algoritmo']='Shannon-Fano'
    lista_simbolos = cod['ListaSimbolos']
    codigos = asignar_codigos(lista_simbolos) # TODO: quitar codigos
    cod['Codigos'] = codigos
    cod['TextoCodificado'] = ''.join(codigos[char] for char in cod['TextoOriginal'])

    long_prom_total = 0
    bits_totales = 0

    # Calcular por símbolo: longitud y bits totales
    for s in lista_simbolos:
        longitud = len(s['Codigo'])
        s['LongitudCodigo'] = longitud
        s['BitsTotales'] = s['Cantidad'] * longitud
        s['LongitudPromedioSimbolo'] = longitud * s['Probabilidad']

        long_prom_total += s['LongitudPromedioSimbolo']
        bits_totales += s['BitsTotales']

    cod['LongitudPromedio'] = long_prom_total
    cod['CantidadBits'] = bits_totales
    # cod['EntropiaH'] = long_prom_total

    cod['Eficiencia'] = cod['EntropiaTotal'] / cod['LongitudPromedio'] if cod['LongitudPromedio'] else 0

    return cod


b=codificar_shannon_fano(a)
print(b)
print("fin2")