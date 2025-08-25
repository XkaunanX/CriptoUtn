# Implementacion shannon fano
def encode_shannon_fano(data: dict):
    # Asociar a cada simbolo su codigo binario
    data['Codes'] = assign_codes(data['SymbolList'])
    # Convertir texto original en su version codificada en bits
    data['EncodedText'] = ''.join(data['Codes'][char] for char in data['OriginalText'])
    
    # Acumuladores
    avg_length = 0
    total_bits = 0
    
    # Por cada simbolo
    for symbol in data['SymbolList']:
        code_length = len(symbol['Code'])
        symbol['CodeLength'] = code_length
        symbol['TotalBits'] = symbol['Count'] * code_length
        symbol['AvgCodeLength'] = code_length * symbol['Probability']
        
        avg_length += symbol['AvgCodeLength']
        total_bits += symbol['TotalBits']
    
    # Metricas
    data['AverageLength'] = avg_length
    data['TotalBits'] = total_bits
    data['Efficiency'] = data['TotalEntropy'] / avg_length if avg_length else 0
    
    return data

# Asignando codigo binario
def assign_codes(symbols, prefix='', codebook=None):
    # Inicializar diccionario
    if codebook is None:
        codebook = {}

    # Caso base
    if len(symbols) == 1:
        code = prefix or '0'
        symbol = symbols[0]
        codebook[symbol['Symbol']] = code
        symbol['Code'] = code
        return codebook

    # Recursion
    left, right = split_symbols(symbols) # Dividir la lista de simbolos
    assign_codes(left, prefix + '0', codebook) # Grupo izquierdo arranca en (0)
    assign_codes(right, prefix + '1', codebook) # Grupo derecho arranca con (1)
    # arbol binario
    return codebook

# Dividir la lista de simbolos
def split_symbols(symbols):
    # La mitad del total de probabilidades
    half = sum(s['Probability'] for s in symbols) / 2
    # Variables necesarias para encontrar el mejor punto donde dividir
    cumulative = 0
    best_index = 0
    min_diff = float('inf')

    # Determinar el lugar a dividir
    for i in range(len(symbols) - 1): # Hasta el penultimo simbolo, se evita el final, dejaria un lado vacio y romperia la recursion
        cumulative += symbols[i]['Probability'] # Peso del grupo left
        diff = abs(half - cumulative) # Que tan equilibrada esta la division en el punto
        
        if diff < min_diff: # Mas cercana a la mitad
            min_diff = diff # Mejor encontrada
            best_index = i # Punto optimo

    return symbols[:best_index + 1], symbols[best_index + 1:]