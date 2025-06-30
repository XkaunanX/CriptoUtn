import os
import pandas as pd

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
