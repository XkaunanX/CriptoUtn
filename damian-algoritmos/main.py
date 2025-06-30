import os
import argparse
import shannon_fano
import average_utils
import export_utils
from rich.console import Console
from rich.table import Table
import pandas as pd

# Recibir archivos por parametro
parser = argparse.ArgumentParser(description="Analiza archivos de texto y genera estadisticas Shannon-Fano")
parser.add_argument("paths", nargs='+', help="Archivos o carpetas a analizar")
parser.add_argument("-e", "--excel", action="store_true", help="Exportar el resultado en formato Excel (.xlsx)")
parser.add_argument("-c", "--csv", action="store_true", help="Exportar el resultado en formato CSV (.csv)")
parser.add_argument("-j", "--json", action="store_true", help="Exportar el resultado en formato JSON (.json)")
parser.add_argument("-ht", "--html", action="store_true", help="Exportar el resultado en formato HTML (.html)")
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

# Procesar (por archivo)
while queue:
    file = queue.pop(0)
    if os.path.isfile(file):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
        
        data = shannon_fano.generate_text_data(content)
        encoded = shannon_fano.encode_shannon_fano(data)
        encoded["Filename"] = os.path.basename(file)
        results.append(encoded)

    else:
        print(f"Error: {file} not found")

# Calcular promedios
averages = average_utils.calculate_averages(results)

# Probando exportacion a excel
if args.excel:
    export_utils.export_to_excel(results, averages)