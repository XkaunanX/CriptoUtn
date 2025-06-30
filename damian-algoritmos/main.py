import os
import argparse
import shannon_fano
import pandas as pd

# Recibir archivos por parametro
parser = argparse.ArgumentParser(description="")
parser.add_argument("paths", nargs='+', help="Archivos o carpetas a analizar")
args = parser.parse_args()

# Cola de procesamiento
queue = []

# Lista de resultados
results  = []

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
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
        
        data = shannon_fano.generate_text_data(content)
        encoded = shannon_fano.encode_shannon_fano(data)
        encoded["Filename"] = os.path.basename(file)
        results.append(encoded)

        print(f"\nProcessed: {file}")
        print(f"  Total symbols: {encoded['TotalSymbols']}")
        print(f"  Entropy: {encoded['TotalEntropy']:.4f}")
        print(f"  Avg length: {encoded['AverageLength']:.4f}")
        print(f"  Bits: {encoded['TotalBits']}")
        print(f"  Efficiency: {encoded['Efficiency']:.4f}")
        print(f"\n{'Symbol':^10} {'Count':^10} {'Prob':^10} {'Code':^10} {'Bits':^10} {'Entropy':^10}")

        for sym in encoded["SymbolList"]:
            print(f"{repr(sym['Symbol']):^10} {sym['Count']:^10} {sym['Probability']:^10.4f} "
                f"{sym['Code']:^10} {sym['TotalBits']:^10} {sym['Entropy']:^10.4f}")
    else:
        print(f"Error: {file} not found")