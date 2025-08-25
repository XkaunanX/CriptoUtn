import math
from operator import itemgetter
from collections import Counter

# Generar datos del texto contenido en cada archivo  
def generate_text_data(string: str):
    data = {} # Diccionario de salida
    symbol_data = [] # Lista de informacion por simbolo
    total_symbols = len(string)
    symbol_counts = Counter(string)
    data = {"OriginalText": string}
    
    for symbol, count in symbol_counts.items():
        probability = count / total_symbols
        inverse_probability = 1/probability
        mutual_info = -math.log2(probability)
        entropy = mutual_info * probability
        
        symbol_data.append({
            "Symbol": symbol,
            "Count": count,
            "Probability": probability,
            "InverseProbability": inverse_probability,
            "MutualInformation": mutual_info,
            "Entropy": entropy
        })
    
    # Ordenar (mayor a menor)
    symbol_data.sort(key=itemgetter("Count"), reverse=True)
    
    # Totales
    total_probability = sum(s["Probability"] for s in symbol_data)
    total_entropy = sum(s["Entropy"] for s in symbol_data)
    
    # Rellenar diccionario
    data["TotalSymbols"] = total_symbols
    data["total_probability"] = total_probability
    data["TotalEntropy"] = total_entropy
    data["SymbolList"] = symbol_data
    
    return data