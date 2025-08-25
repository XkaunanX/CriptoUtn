import pandas as pd

def persistir_simbolos(diccionario, ruta_excel):
    df_simbolos = pd.DataFrame(diccionario["ListaSimbolos"])
    df_totales = pd.DataFrame([{
        "TotalSimbolos": diccionario["TotalSimbolos"],
        "ProbabilidadTotal": diccionario["ProbabilidadTotal"],
        "EntropiaTotal": diccionario["EntropiaTotal"]
    }])
    with pd.ExcelWriter(ruta_excel, engine="openpyxl") as writer:
        df_simbolos.to_excel(writer, sheet_name="Simbolos", index=False)
        df_totales.to_excel(writer, sheet_name="Totales", index=False)
        
def recuperar_simbolos(ruta_excel):
    df_simbolos = pd.read_excel(ruta_excel, sheet_name="Simbolos")
    df_totales = pd.read_excel(ruta_excel, sheet_name="Totales")
    
    diccionario = {
        "ListaSimbolos": df_simbolos.to_dict(orient="records"),
        "TotalSimbolos": int(df_totales["TotalSimbolos"][0]),
        "ProbabilidadTotal": float(df_totales["ProbabilidadTotal"][0]),
        "EntropiaTotal": float(df_totales["EntropiaTotal"][0])
    }
    
    return diccionario

def persistir_shannon_fano(diccionario, ruta_excel):
    df_simbolos = pd.DataFrame(diccionario["ListaSimbolos"])
    
    df_totales = pd.DataFrame([{
        "TotalSimbolos": diccionario.get("TotalSimbolos", 0),
        "ProbabilidadTotal": diccionario.get("ProbabilidadTotal", 0),
        "EntropiaTotal": diccionario.get("EntropiaTotal", 0),
        "LongitudPromedio": diccionario.get("LongitudPromedio", 0),
        "TotalBits": diccionario.get("TotalBits", 0),
        "Eficiencia": diccionario.get("Eficiencia", 0),
        "TiempoCodificacion": diccionario.get("TiempoCodificacion", 0),
        "TiempoDecodificacion": diccionario.get("TiempoDecodificacion", 0)
    }])
    
    with pd.ExcelWriter(ruta_excel, engine="openpyxl") as writer:
        df_simbolos.to_excel(writer, sheet_name="Simbolos", index=False)
        df_totales.to_excel(writer, sheet_name="Totales", index=False)
        
def recuperar_shannon_fano(ruta_excel):
    df_simbolos = pd.read_excel(ruta_excel, sheet_name="Simbolos")
    df_totales = pd.read_excel(ruta_excel, sheet_name="Totales")
    
    diccionario = {
        "ListaSimbolos": df_simbolos.to_dict(orient="records"),
        "TotalSimbolos": int(df_totales["TotalSimbolos"][0]),
        "ProbabilidadTotal": float(df_totales["ProbabilidadTotal"][0]),
        "EntropiaTotal": float(df_totales["EntropiaTotal"][0]),
        "LongitudPromedio": float(df_totales["LongitudPromedio"][0]),
        "TotalBits": int(df_totales["TotalBits"][0]),
        "Eficiencia": float(df_totales["Eficiencia"][0]),
        "TiempoCodificacion": float(df_totales["TiempoCodificacion"][0]),
        "TiempoDecodificacion": float(df_totales["TiempoDecodificacion"][0])
    }
    
    if "Code" in df_simbolos.columns and "Simbolo" in df_simbolos.columns:
        diccionario["Codigos"] = {row["Simbolo"]: row["Code"] for row in diccionario["ListaSimbolos"]}
    
    return diccionario

def persistir_huffman(diccionario, ruta_excel):
    df_simbolos = pd.DataFrame(diccionario["ListaSimbolos"])
    df_totales = pd.DataFrame([{
        "TotalSimbolos": diccionario.get("TotalSimbolos", 0),
        "ProbabilidadTotal": diccionario.get("ProbabilidadTotal", 0),
        "EntropiaTotal": diccionario.get("EntropiaTotal", 0),
        "LongitudPromedio": diccionario.get("LongitudPromedio", 0),
        "TotalBits": diccionario.get("TotalBits", 0),
        "Eficiencia": diccionario.get("Eficiencia", 0),
        "TiempoCodificacion": diccionario.get("TiempoCodificacion", 0),
        "TiempoDecodificacion": diccionario.get("TiempoDecodificacion", 0)
    }])
    
    with pd.ExcelWriter(ruta_excel, engine="openpyxl") as writer:
        df_simbolos.to_excel(writer, sheet_name="Simbolos", index=False)
        df_totales.to_excel(writer, sheet_name="Totales", index=False)

def recuperar_huffman(ruta_excel):
    df_simbolos = pd.read_excel(ruta_excel, sheet_name="Simbolos")
    df_totales = pd.read_excel(ruta_excel, sheet_name="Totales")
    
    diccionario = {
        "ListaSimbolos": df_simbolos.to_dict(orient="records"),
        "TotalSimbolos": int(df_totales["TotalSimbolos"][0]),
        "ProbabilidadTotal": float(df_totales["ProbabilidadTotal"][0]),
        "EntropiaTotal": float(df_totales["EntropiaTotal"][0]),
        "LongitudPromedio": float(df_totales["LongitudPromedio"][0]),
        "TotalBits": int(df_totales["TotalBits"][0]),
        "Eficiencia": float(df_totales["Eficiencia"][0]),
        "TiempoCodificacion": float(df_totales["TiempoCodificacion"][0]),
        "TiempoDecodificacion": float(df_totales["TiempoDecodificacion"][0])
    }
    
    if "Codigo" in df_simbolos.columns and "Simbolo" in df_simbolos.columns:
        diccionario["Codigos"] = {row["Simbolo"]: row["Codigo"] for row in diccionario["ListaSimbolos"]}
    
    return diccionario

def persistir_lz77(diccionario, ruta_excel):
    df_comprimido = pd.DataFrame(diccionario["Comprimido"], columns=["Distancia", "Longitud", "Caracter"])
    df_totales = pd.DataFrame([{
        "LongitudOriginal": diccionario.get("LongitudOriginal", 0),
        "LongitudComprimida": diccionario.get("LongitudComprimida", 0),
        "Eficiencia": diccionario.get("Eficiencia", 0),
        "TiempoCodificacion": diccionario.get("TiempoCodificacion", 0),
        "TiempoDecodificacion": diccionario.get("TiempoDecodificacion", 0)
    }])
    with pd.ExcelWriter(ruta_excel, engine="openpyxl") as writer:
        df_comprimido.to_excel(writer, sheet_name="Comprimido", index=False)
        df_totales.to_excel(writer, sheet_name="Totales", index=False)

def recuperar_lz77(ruta_excel):
    df_comprimido = pd.read_excel(ruta_excel, sheet_name="Comprimido")
    df_totales = pd.read_excel(ruta_excel, sheet_name="Totales")
    diccionario = {
        "Comprimido": [tuple(row) for row in df_comprimido.to_numpy()],
        "LongitudOriginal": int(df_totales["LongitudOriginal"][0]),
        "LongitudComprimida": int(df_totales["LongitudComprimida"][0]),
        "Eficiencia": float(df_totales["Eficiencia"][0]),
        "TiempoCodificacion": float(df_totales["TiempoCodificacion"][0]),
        "TiempoDecodificacion": float(df_totales["TiempoDecodificacion"][0])
    }
    return diccionario

def persistir_promedios(diccionario_promedios, ruta_excel):
    df_generales = pd.DataFrame([diccionario_promedios["PromediosGenerales"]])
    df_simbolos = pd.DataFrame(diccionario_promedios["SimbolosPromediados"])
    with pd.ExcelWriter(ruta_excel, engine="openpyxl") as writer:
        df_generales.to_excel(writer, sheet_name="PromediosGenerales", index=False)
        df_simbolos.to_excel(writer, sheet_name="SimbolosPromediados", index=False)