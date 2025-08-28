import os
from docx import Document
from PyPDF2 import PdfReader

def leer_archivo(path):
    extension = os.path.splitext(path)[1].lower()
    if extension == ".docx":
        doc = Document(path)
        texto = ""
        for p in doc.paragraphs:
            texto += p.text + "\n"
        return texto
    elif extension == ".pdf":
        reader = PdfReader(path)
        texto = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                texto += page_text
        return texto
    elif extension == ".txt":
        return open(path, 'r', encoding='utf-8').read()
    else:
        raise ValueError("reader.py - Formato no soportado: " + extension)