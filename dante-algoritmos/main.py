import argparse
import os
import reader
import simbolos
import excel
import huffman
import promedio
import shannon
import generar_archivo
import decodificar

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
    extension = os.path.splitext(archivo)[1].lower()
    contenido = reader.leer_archivo(archivo)
    nombre_base = os.path.splitext(os.path.basename(archivo))[0]
    ruta_simbolos = f"planillas/{nombre_base}_simbolo.xlsx"
    info_simbolos = simbolos.informacion_simbolos(contenido)
    resultados_simbolos.append(info_simbolos)
    excel.persistir_simbolos(info_simbolos, ruta_simbolos)
    shan = shannon.codificar_shannon_fano(excel.recuperar_simbolos(ruta_simbolos))
    huff = huffman.codificar_huffman(excel.recuperar_simbolos(ruta_simbolos))
    codificado_huffman, bits_validos_huffman = generar_archivo.generar_archivo_codificado(huff, contenido)
    codificado_shannon, bits_validos_shannon = generar_archivo.generar_archivo_codificado(shan, contenido)
    
    with open(f"codificado/{nombre_base}_shannon.bin", "wb") as f:
        f.write(bytes([bits_validos_shannon]))
        f.write(codificado_shannon)
    with open(f"decodificado/{nombre_base}_shannon{extension}", "wb") as f:
        f.write(decodificar.decodificar(shan, codificado_shannon, bits_validos_shannon))
        
    with open(f"codificado/{nombre_base}_huffman.bin", "wb") as f: # uso .bin ya que el archivo codificado esta en bytes y no en caracteres
        f.write(bytes([bits_validos_huffman])) #uso los bits validos para indicar la longitud del ultimo byte a la hora de descomprimir
        f.write(codificado_huffman)
    with open(f"decodificado/{nombre_base}_huffman{extension}", "wb") as f:
        f.write(decodificar.decodificar(huff, codificado_huffman, bits_validos_huffman))

    excel.persistir_huffman(huff, f"./planillas/{nombre_base}_huffman.xlsx")
    excel.persistir_shannon_fano(shan, f"./planillas/{nombre_base}_shannon.xlsx")
    
promedios = promedio.calcular_promedios(resultados_simbolos)
excel.persistir_promedios(promedios, f"./planillas/promedio_simbolos.xlsx")