def calcular_promedios(resultados):
    total_archivos = len(resultados)
    
    # Promedios generales
    promedio_total_simbolos = sum(r["TotalSimbolos"] for r in resultados) / total_archivos if total_archivos else 0
    promedio_entropia_total = sum(r["EntropiaTotal"] for r in resultados) / total_archivos if total_archivos else 0
    promedio_probabilidad_total = sum(r["ProbabilidadTotal"] for r in resultados) / total_archivos if total_archivos else 0

    promedios_generales = {
        "PromedioTotalSimbolos": promedio_total_simbolos,
        "PromedioEntropiaTotal": promedio_entropia_total,
        "PromedioProbabilidadTotal": promedio_probabilidad_total
    }

    # Promedio por simbolo
    estadisticas_simbolos = {}

    for r in resultados:
        for s in r["ListaSimbolos"]:
            simbolo = s["Simbolo"]
            if simbolo not in estadisticas_simbolos:
                estadisticas_simbolos[simbolo] = {
                    "Cantidad": 0,
                    "Probabilidad": 0,
                    "ProbabilidadInversa": 0,
                    "InformacionMutua": 0,
                    "Entropia": 0,
                    "Apariciones": 0
                }
            estadisticas_simbolos[simbolo]["Cantidad"] += s["Cantidad"]
            estadisticas_simbolos[simbolo]["Probabilidad"] += s["Probabilidad"]
            estadisticas_simbolos[simbolo]["ProbabilidadInversa"] += s["ProbabilidadInversa"]
            estadisticas_simbolos[simbolo]["InformacionMutua"] += s["InformacionMutua"]
            estadisticas_simbolos[simbolo]["Entropia"] += s["Entropia"]
            estadisticas_simbolos[simbolo]["Apariciones"] += 1

    simbolos_promediados = []
    for simbolo, stats in estadisticas_simbolos.items():
        apariciones = stats["Apariciones"]
        simbolos_promediados.append({
            "Simbolo": simbolo,
            "PromedioCantidad": stats["Cantidad"] / apariciones,
            "PromedioProbabilidad": stats["Probabilidad"] / apariciones,
            "PromedioProbabilidadInversa": stats["ProbabilidadInversa"] / apariciones,
            "PromedioInformacionMutua": stats["InformacionMutua"] / apariciones,
            "PromedioEntropia": stats["Entropia"] / apariciones
        })

    return {
        "PromediosGenerales": promedios_generales,
        "SimbolosPromediados": simbolos_promediados
    }