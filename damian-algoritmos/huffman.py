import heapq

# Implementacion Huffman
class HuffmanNode:
    def __init__(self, symbol=None, freq=0):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None

    # Permite ordenar nodos en el heap por frecuencia
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(symbols):
    heap = []

    # Crear nodos hoja para cada simbolo y meter en heap
    for s in symbols:
        heapq.heappush(heap, HuffmanNode(symbol=s['Symbol'], freq=s['Count']))

    # Construir el arbol uniendo nodos de menor frecuencia
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = HuffmanNode(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(heap, merged)

    return heap[0]

def assign_huffman_codes(node, prefix='', codebook=None):
    if codebook is None:
        codebook = {}

    if node.symbol is not None:
        codebook[node.symbol] = prefix or '0'
    else:
        assign_huffman_codes(node.left, prefix + '0', codebook)
        assign_huffman_codes(node.right, prefix + '1', codebook)

    return codebook

def encode_huffman(data: dict):
    # Construir arbol Huffman a partir de la lista de simbolos y sus frecuencias
    tree = build_huffman_tree(data['SymbolList'])

    # Asignar codigos binarios a cada simbolo
    codes = assign_huffman_codes(tree)
    data['Codes'] = codes

    # Codificar el texto original usando los codigos asignados
    data['EncodedText'] = ''.join(codes[char] for char in data['OriginalText'])

    # Inicializar metricas
    avg_length = 0
    total_bits = 0

    # Calcular metricas por simbolo y agregar al diccionario
    for symbol in data['SymbolList']:
        code = codes[symbol['Symbol']]
        code_length = len(code)
        symbol['Code'] = code
        symbol['CodeLength'] = code_length
        symbol['TotalBits'] = symbol['Count'] * code_length
        symbol['AvgCodeLength'] = code_length * symbol['Probability']

        avg_length += symbol['AvgCodeLength']
        total_bits += symbol['TotalBits']

    # Guardar métricas generales en el diccionario
    data['AverageLength'] = avg_length
    data['TotalBits'] = total_bits
    data['Efficiency'] = data['TotalEntropy'] / avg_length if avg_length > 0 else 0

    return data
