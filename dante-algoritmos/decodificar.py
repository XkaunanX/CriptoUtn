import time

def decodificar(datos: dict, archivo_codificado: bytes, bits_validos: bytes):
    inicio = time.time()
    codigo_a_simbolo = {v: k for k, v in datos['Codigos'].items()}
    resultado = bytearray()
    buffer = ''
    bits = ''
    
    for i, byte in enumerate(archivo_codificado):
        b = format(byte, "08b")  # convierto un byte a 8 bits
        if i == len(archivo_codificado) - 1:
            b = b[:bits_validos]  # último byte: solo los bits válidos
        bits += b
    
    for bit in bits:
        buffer += bit
        if buffer in codigo_a_simbolo:
            resultado.append(codigo_a_simbolo[buffer])
            buffer = ''
            
    fin = time.time()
    datos['TiempoDecodificacion'] = round(fin - inicio, 3)
    buffer = ''
    bits = ''
    return bytes(resultado)