import os
import json
import pandas as pd

# Exportar a excel
def export_to_excel(results, averages, output_dir="excel", filename="shannon_fano_analysis.xlsx"):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    with pd.ExcelWriter(output_path) as writer:
        # 1. Exportar detalle de cada archivo a hojas separadas
        for result in results:
            df = pd.DataFrame(result["SymbolList"])
            sheet_name = os.path.splitext(result["Filename"])[0][:31]  # Excel limita nombre hoja a 31 chars
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        # 2. Exportar promedio general (general_averages) a hoja 'General_Averages'
        general_avg = averages["general_averages"]
        df_general = pd.DataFrame([general_avg])  # Pasar dict a dataframe de una fila
        df_general.to_excel(writer, sheet_name="General_Averages", index=False)

        # 3. Exportar promedio por simbolo a hoja 'Symbol_Averages'
        df_symbols = pd.DataFrame(averages["averaged_symbols"])
        df_symbols.to_excel(writer, sheet_name="Symbol_Averages", index=False)

    print(f"Exportado todo a Excel: {output_path}")

# Exportar a csv 
def export_to_csv(results, averages, output_dir="csv"):
    os.makedirs(output_dir, exist_ok=True)

    for result in results:
        df = pd.DataFrame(result["SymbolList"])
        filename = os.path.splitext(result["Filename"])[0]
        output_path = os.path.join(output_dir, f"{filename}_detalle.csv")
        df.to_csv(output_path, index=False)

    general_avg = averages["general_averages"]
    df_general = pd.DataFrame([general_avg])
    df_general.to_csv(os.path.join(output_dir, "promedio_general.csv"), index=False)

    df_symbols = pd.DataFrame(averages["averaged_symbols"])
    df_symbols.to_csv(os.path.join(output_dir, "promedio_por_simbolo.csv"), index=False)

    print(f"Exportado todo a CSV en carpeta: {output_dir}")

# Exportar a json
def export_to_json(results, averages, output_dir="json"):
    os.makedirs(output_dir, exist_ok=True)

    for result in results:
        filename = os.path.splitext(result["Filename"])[0]
        output_path = os.path.join(output_dir, f"{filename}_detalle.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result["SymbolList"], f, ensure_ascii=False, indent=4)

    general_path = os.path.join(output_dir, "promedio_general.json")
    with open(general_path, "w", encoding="utf-8") as f:
        json.dump(averages["general_averages"], f, ensure_ascii=False, indent=4)

    symbols_path = os.path.join(output_dir, "promedio_por_simbolo.json")
    with open(symbols_path, "w", encoding="utf-8") as f:
        json.dump(averages["averaged_symbols"], f, ensure_ascii=False, indent=4)

    print(f"Exportado todo a JSON en carpeta: {output_dir}")