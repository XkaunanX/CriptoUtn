import os
import json
import pandas as pd

# Exportar a excel
def export_to_excel(results, averages, encoding, output_dir="excel", filename="analysis.xlsx"):
    os.makedirs(output_dir, exist_ok=True)

    name, ext = os.path.splitext(filename)
    filename_with_encoding = f"{name}_{encoding}{ext}"
    output_path = os.path.join(output_dir, filename_with_encoding)

    with pd.ExcelWriter(output_path) as writer:
        for result in results:
            df = pd.DataFrame(result["SymbolList"])
            sheet_name = os.path.splitext(result["Filename"])[0][:31]
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        df_general = pd.DataFrame([averages["general_averages"]])
        df_general.to_excel(writer, sheet_name="General_Averages", index=False)

        df_symbols = pd.DataFrame(averages["averaged_symbols"])
        df_symbols.to_excel(writer, sheet_name="Symbol_Averages", index=False)

    print(f"Exportado todo a Excel: {output_path}")


# Exportar a csv 
def export_to_csv(results, averages, output_dir="csv", encoding=None):
    os.makedirs(output_dir, exist_ok=True)

    for result in results:
        df = pd.DataFrame(result["SymbolList"])
        filename = os.path.splitext(result["Filename"])[0]
        if encoding:
            filename = f"{filename}_{encoding}"
        output_path = os.path.join(output_dir, f"{filename}_detalle.csv")
        df.to_csv(output_path, index=False)

    general_avg = averages["general_averages"]
    general_filename = "promedio_general"
    if encoding:
        general_filename += f"_{encoding}"
    df_general = pd.DataFrame([general_avg])
    df_general.to_csv(os.path.join(output_dir, f"{general_filename}.csv"), index=False)

    symbols_filename = "promedio_por_simbolo"
    if encoding:
        symbols_filename += f"_{encoding}"
    df_symbols = pd.DataFrame(averages["averaged_symbols"])
    df_symbols.to_csv(os.path.join(output_dir, f"{symbols_filename}.csv"), index=False)

    print(f"Exportado todo a CSV en carpeta: {output_dir}")

# Exportar a json
def export_to_json(results, averages, output_dir="json", encoding=None):
    os.makedirs(output_dir, exist_ok=True)

    for result in results:
        filename = os.path.splitext(result["Filename"])[0]
        if encoding:
            filename = f"{filename}_{encoding}"
        output_path = os.path.join(output_dir, f"{filename}_detalle.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result["SymbolList"], f, ensure_ascii=False, indent=4)

    general_filename = "promedio_general"
    if encoding:
        general_filename += f"_{encoding}"
    general_path = os.path.join(output_dir, f"{general_filename}.json")
    with open(general_path, "w", encoding="utf-8") as f:
        json.dump(averages["general_averages"], f, ensure_ascii=False, indent=4)

    symbols_filename = "promedio_por_simbolo"
    if encoding:
        symbols_filename += f"_{encoding}"
    symbols_path = os.path.join(output_dir, f"{symbols_filename}.json")
    with open(symbols_path, "w", encoding="utf-8") as f:
        json.dump(averages["averaged_symbols"], f, ensure_ascii=False, indent=4)

    print(f"Exportado todo a JSON en carpeta: {output_dir}")
