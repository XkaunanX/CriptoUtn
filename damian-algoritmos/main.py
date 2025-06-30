import os
import argparse
from operator import itemgetter
from collections import Counter
import math
import pandas as pd

# Recibir archivos por parametro
parser = argparse.ArgumentParser(description="")
parser.add_argument("paths", nargs='+', help="Archivos o carpetas a analizar")
args = parser.parse_args()

# Cola de procesamiento
queue = []

# Encolar archivos a procesar
for path in args.paths:
    if os.path.isfile(path):
        queue.append(path)
    elif os.path.isdir(path):
        for entry in os.listdir(path):
            absolute_path = os.path.join(path, entry)
            if os.path.isfile(absolute_path):
                queue.append(absolute_path)
    else:
        print(f"Error in {path}")

# Procesar 
while queue:
    file = queue.pop(0)
    if os.path.isfile(file):
        print(f"file: {file}")
    else:
        print("Error")

# Generar datos del texto contenido en cada archivo  
def generate_text_data(string: str):
    result = {} # Diccionario de salida
    symbol_data = [] # Lista de informacion por simbolo
    total_symbols = len(string)
    symbol_counts = Counter(string)
    
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
    result["TotalSymbols"] = total_symbols
    result["total_probability"] = total_probability
    result["TotalEntropy"] = total_entropy
    result["SymbolList"] = symbol_data
    
    return result