# Cripto UTN

## Instalar Dependencias

´´´bash
pip install -r requirements.txt
´´´

## Ejecutar

´´´bash
python main.py <directorio>
´´´

## Explicacion

<directorio> Tiene que contener los archivos .docx o pdf que se quiera procesar

- en ./planillas: se generara el analisis por cada archivo, de todos las codificaciones, se generara un archivo con el promedio de simbolos.

- en ./codificado: se generara los archivos .txt con su texto codificado.

- en ./decodificado: se generara los archivos .txt con su texto decodificado luego de ser codificado para verificar el correcto funcionamiento.