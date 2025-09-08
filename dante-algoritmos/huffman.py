import heapq
import time

class NodoHuffman:
    def __init__(self, simbolo=None, frecuencia=0):
        self.simbolo = simbolo
        self.frecuencia = frecuencia
        self.izquierdo = None
        self.derecho = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

def construir_arbol_huffman(lista_simbolos):
    heap = []
    for s in lista_simbolos:
        heapq.heappush(heap, NodoHuffman(simbolo=s['Simbolo'], frecuencia=s['Cantidad']))

    while len(heap) > 1:
        izquierdo = heapq.heappop(heap)
        derecho = heapq.heappop(heap)
        combinado = NodoHuffman(frecuencia=izquierdo.frecuencia + derecho.frecuencia)
        combinado.izquierdo = izquierdo
        combinado.derecho = derecho
        heapq.heappush(heap, combinado)

    return heap[0]

def asignar_codigos_huffman(nodo, prefijo='', diccionario_codigos=None):
    if diccionario_codigos is None:
        diccionario_codigos = {}

    if nodo.simbolo is not None:
        diccionario_codigos[nodo.simbolo] = prefijo or '0'
    else:
        asignar_codigos_huffman(nodo.izquierdo, prefijo + '0', diccionario_codigos)
        asignar_codigos_huffman(nodo.derecho, prefijo + '1', diccionario_codigos)

    return diccionario_codigos

def codificar_huffman(datos: dict):
    inicio = time.time()

    arbol = construir_arbol_huffman(datos['ListaSimbolos'])
    codigos = asignar_codigos_huffman(arbol)
    datos['Codigos'] = codigos

    longitud_promedio = 0
    total_bits = 0

    for simbolo in datos['ListaSimbolos']:
        codigo = codigos[simbolo['Simbolo']]
        largo = len(codigo)
        simbolo['Codigo'] = codigo
        simbolo['LongitudCodigo'] = largo
        simbolo['TotalBits'] = simbolo['Cantidad'] * largo
        simbolo['LongitudPromedio'] = largo * simbolo['Probabilidad']

        longitud_promedio += simbolo['LongitudPromedio']
        total_bits += simbolo['TotalBits']

    datos['LongitudPromedio'] = longitud_promedio
    datos['TotalBits'] = total_bits
    datos['Eficiencia'] = datos['EntropiaTotal'] / longitud_promedio if longitud_promedio > 0 else 0

    fin = time.time()
    datos['TiempoCodificacion'] = round(fin - inicio, 3)

    return datos