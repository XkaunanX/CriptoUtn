def leer_archivo(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return data
    except FileNotFoundError:
        print(f"Error: el archivo '{path}' no existe.")
    except PermissionError:
        print(f"Error: no tenés permisos para leer '{path}'.")
    except Exception as e:
        print(f"Error inesperado al leer '{path}': {e}")
    return None