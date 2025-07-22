import os
import argparse
import shannon_fano
import huffman
import average_utils
import export_utils
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
        
        # Seleccionar algoritmo
        if args.algorithm == "shannon":
            data = shannon_fano.generate_text_data(content)
            encoded = shannon_fano.encode_shannon_fano(data)
        elif args.algorithm == "huffman":
            data = huffman.generate_text_data(content)
            encoded = huffman.encode_huffman(data)

        encoded["Filename"] = os.path.basename(file)
        encoded["Algorithm"] = args.algorithm
        results.append(encoded)

    else:
        print(f"Error: {file} not found")

averages = average_utils.calculate_averages(results)

if args.excel:
    export_utils.export_to_excel(results, averages)
    
if args.csv:
    export_utils.export_to_csv(results, averages)
    
if args.json:
    export_utils.export_to_json(results, averages)

end = time.time()

print(f"Tiempo transcurrido: {end - start:.4f} segundos")