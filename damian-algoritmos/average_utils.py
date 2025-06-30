def calculate_averages(results):
    total_files = len(results)
    # Promedio general
    avg_entropy = sum(r["TotalEntropy"] for r in results) / total_files if total_files else 0
    avg_length = sum(r["AverageLength"] for r in results) / total_files if total_files else 0
    avg_bits = sum(r["TotalBits"] for r in results) / total_files if total_files else 0
    avg_efficiency = sum(r["Efficiency"] for r in results) / total_files if total_files else 0

    general_averages = {
        "AverageEntropy": avg_entropy,
        "AverageLength": avg_length,
        "AverageBits": avg_bits,
        "AverageEfficiency": avg_efficiency
    }

    # Promedio por simbolo
    symbol_stats = {}

    for r in results:
        for sym in r["SymbolList"]:
            char = sym["Symbol"]
            if char not in symbol_stats:
                symbol_stats[char] = {
                    "Count": 0,
                    "Probability": 0,
                    "CodeLength": 0,
                    "TotalBits": 0,
                    "Entropy": 0,
                    "Appearances": 0
                }
            symbol_stats[char]["Count"] += sym["Count"]
            symbol_stats[char]["Probability"] += sym["Probability"]
            symbol_stats[char]["CodeLength"] += sym.get("CodeLength", 0)
            symbol_stats[char]["TotalBits"] += sym.get("TotalBits", 0)
            symbol_stats[char]["Entropy"] += sym["Entropy"]
            symbol_stats[char]["Appearances"] += 1

    averaged_symbols = []
    for char, stats in symbol_stats.items():
        appearances = stats["Appearances"]
        averaged_symbols.append({
            "Symbol": char,
            "AvgCount": stats["Count"] / appearances,
            "AvgProbability": stats["Probability"] / appearances,
            "AvgCodeLength": stats["CodeLength"] / appearances,
            "AvgTotalBits": stats["TotalBits"] / appearances,
            "AvgEntropy": stats["Entropy"] / appearances
        })

    return {
        "general_averages": general_averages,
        "averaged_symbols": averaged_symbols
    }
