import argparse
import os
import reader
import simbolos
import excel
import shannon
import huffman
import lempel
import promedio

# Crear directorio para los archivos
os.makedirs("./planillas", exist_ok=True)
os.makedirs("./codificado", exist_ok=True)
os.makedirs("./decodificado", exist_ok=True)

parser = argparse.ArgumentParser(description="Procesa un directorio")
parser.add_argument("directorio", help="Directorio a procesar")
args = parser.parse_args()

cola = []

# Reemplazar args.paths por args.directorio
if os.path.isdir(args.directorio):
    for entry in os.listdir(args.directorio):
        absolute_path = os.path.join(args.directorio, entry)
        if os.path.isfile(absolute_path):
            cola.append(absolute_path)
else:
    print(f"main.py - Error en {args.directorio}")
    
resultados_simbolos = []
    
while cola:
    archivo = cola.pop(0)
    contenido = reader.leer_archivo(archivo)
    nombre_base = os.path.splitext(os.path.basename(archivo))[0]
    ruta_simbolos = f"planillas/{nombre_base}_simbolo.xlsx"
    info_simbolos = simbolos.informacion_simbolos(contenido)
    resultados_simbolos.append(info_simbolos)
    excel.persistir_simbolos(info_simbolos, ruta_simbolos)
    shan = shannon.codificar_shannon_fano(excel.recuperar_simbolos(ruta_simbolos))
    huff = huffman.codificar_huffman(excel.recuperar_simbolos(ruta_simbolos))
    lemp = lempel.lz77_compress_con_metrica(contenido)
    with open(f"codificado/{nombre_base}_shannon.txt", "w", encoding="utf-8") as f:
        f.write(shannon.generar_texto_codificado(shan, contenido))
    with open(f"decodificado/{nombre_base}_shannon.txt", "w", encoding="utf-8") as f:
        f.write(shannon.decodificar_shannon_fano(shan, shannon.generar_texto_codificado(shan, contenido)))
    with open(f"codificado/{nombre_base}_huffman.txt", "w", encoding="utf-8") as f:
        f.write(huffman.generar_texto_codificado(huff, contenido))
    with open(f"decodificado/{nombre_base}_huffman.txt", "w", encoding="utf-8") as f:
        f.write(huffman.decodificar_huffman(huff, huffman.generar_texto_codificado(huff, contenido)))
    with open(f"codificado/{nombre_base}_lempel-ziv.txt", "w", encoding="utf-8") as f:
        f.write(str(lempel.lz77_compress(contenido)))
    with open(f"decodificado/{nombre_base}_lempel-ziv.txt", "w", encoding="utf-8") as f:
        f.write(lempel.lz77_decompress(lempel.lz77_compress(contenido)))
    excel.persistir_shannon_fano(shan, f"./planillas/{nombre_base}_shannon.xlsx")
    excel.persistir_huffman(huff, f"./planillas/{nombre_base}_huffman.xlsx")
    excel.persistir_lz77(lemp, f"./planillas/{nombre_base}_lempel-ziv.xlsx")
    
promedios = promedio.calcular_promedios(resultados_simbolos)

excel.persistir_promedios(promedios, f"./planillas/promedio_simbolos.xlsx")
