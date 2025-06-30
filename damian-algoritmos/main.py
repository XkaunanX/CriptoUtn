import os
import argparse
import shannon_fano
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

console = Console()

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

        console.rule(f"[bold green]Processed: {file}")

        console.print(f"[cyan]Total symbols:[/] {encoded['TotalSymbols']}")
        console.print(f"[cyan]Entropy:[/] {encoded['TotalEntropy']:.4f}")
        console.print(f"[cyan]Avg length:[/] {encoded['AverageLength']:.4f}")
        console.print(f"[cyan]Bits:[/] {encoded['TotalBits']}")
        console.print(f"[cyan]Efficiency:[/] {encoded['Efficiency']:.4f}")

        table = Table(title=f"Symbol Details: {os.path.basename(file)}")

        table.add_column("Symbol", justify="center")
        table.add_column("Count", justify="right")
        table.add_column("Prob", justify="right")
        table.add_column("Code", justify="center")
        table.add_column("Bits", justify="right")
        table.add_column("Entropy", justify="right")

        for sym in encoded["SymbolList"]:
            table.add_row(
                repr(sym["Symbol"]),
                str(sym["Count"]),
                f"{sym['Probability']:.4f}",
                sym["Code"],
                str(sym["TotalBits"]),
                f"{sym["Entropy"]:.4f}"
            )

        console.print(table)

    else:
        print(f"Error: {file} not found")

# Probando exportacion a excel
if args.excel:
    output_dir = "excel"
    os.makedirs(output_dir, exist_ok=True)

    for result in results:
        df = pd.DataFrame(result["SymbolList"])
        filename = os.path.splitext(result["Filename"])[0]
        output_path = os.path.join(output_dir, f"{filename}_shannon_fano.xlsx")
        df.to_excel(output_path, index=False)
        print(f"Exportado a Excel: {output_path}")
