import os
import argparse
import text_data
import shannon
import huffman
import average
import export
import time

# Recibir archivos por parametro
parser = argparse.ArgumentParser(description="Analiza archivos de texto y genera estadisticas por algoritmo")
parser.add_argument("paths", nargs='+', help="Archivos o carpetas a analizar")
parser.add_argument("-e", "--excel", action="store_true", help="Exportar el resultado en formato Excel (.xlsx)")
parser.add_argument("-c", "--csv", action="store_true", help="Exportar el resultado en formato CSV (.csv)")
parser.add_argument("-j", "--json", action="store_true", help="Exportar el resultado en formato JSON (.json)")
parser.add_argument("-a", "--algorithm", choices=["shannon", "huffman"], default="shannon",
                    help="Algoritmo a usar: shannon o huffman (default: shannon)")
args = parser.parse_args()

start = time.time()

queue = []
results  = []

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

while queue:
    file = queue.pop(0)
    if os.path.isfile(file):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
        
        data = text_data.generate_text_data(content)
        
        # Seleccionar algoritmo
        if args.algorithm == "shannon":
            encoded = shannon.encode_shannon_fano(data)
        elif args.algorithm == "huffman":
            encoded = huffman.encode_huffman(data)

        encoded["Filename"] = os.path.basename(file)
        encoded["Algorithm"] = args.algorithm
        results.append(encoded)

    else:
        print(f"Error: {file} not found")

averages = average.calculate_averages(results)

if args.excel:
    export.export_to_excel(results, averages, encoding=args.algorithm)
    
if args.csv:
    export.export_to_csv(results, averages, encoding=args.algorithm)
    
if args.json:
    export.export_to_json(results, averages, encoding=args.algorithm)

end = time.time()

print(f"Tiempo transcurrido: {end - start:.4f} segundos")