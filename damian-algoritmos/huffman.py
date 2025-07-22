import heapq

class HuffmanNode:
    def __init__(self, symbol=None, freq=0):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None

    # Esto permite que los nodos se ordenen por frecuencia en el heap
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(symbols):
    heap = []

    # Crear un nodo por simbolo
    for s in symbols:
        heapq.heappush(heap, HuffmanNode(symbol=s['Symbol'], freq=s['Count']))

    # Construccion del arbol de Huffman
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

    if node.symbol is not None:  # Es una hoja
        codebook[node.symbol] = prefix or '0'
    else:
        assign_huffman_codes(node.left, prefix + '0', codebook)
        assign_huffman_codes(node.right, prefix + '1', codebook)

    return codebook

def encode_huffman(data: dict):
    # Árbol y asignación de códigos
    tree = build_huffman_tree(data['SymbolList'])
    codes = assign_huffman_codes(tree)
    data['Codes'] = codes
    data['EncodedText'] = ''.join(codes[char] for char in data['OriginalText'])

    # Metricas por simbolo
    avg_length = 0
    total_bits = 0

    for symbol in data['SymbolList']:
        code = codes[symbol['Symbol']]
        code_length = len(code)
        symbol['Code'] = code
        symbol['CodeLength'] = code_length
        symbol['TotalBits'] = symbol['Count'] * code_length
        symbol['AvgCodeLength'] = code_length * symbol['Probability']

        avg_length += symbol['AvgCodeLength']
        total_bits += symbol['TotalBits']

    # Metricas generales
    data['AverageLength'] = avg_length
    data['TotalBits'] = total_bits
    data['Efficiency'] = data['TotalEntropy'] / avg_length if avg_length else 0

    return data
