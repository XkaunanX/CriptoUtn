def generar_archivo_codificado(datos: dict, archivo_original: bytes):
    codigos = datos['Codigos']
    bits = ''.join(codigos[s] for s in archivo_original)
    bits_validos = len(bits) % 8
    if bits_validos == 0:
        bits_validos = 8  #último byte completo

    byteArray = bytearray()
    
    for i in range(0, len(bits), 8):
        byte_segmento = bits[i:i+8] #tomo 8 bits
        if len(byte_segmento) < 8:
            byte_segmento = byte_segmento.ljust(8, "0") #si el byte no esta completo, lo completo con ceros
        byteArray.append(int(byte_segmento, 2)) #agrego el byte al final del array
    
    return bytes(byteArray), bits_validos