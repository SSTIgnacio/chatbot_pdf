import os
import PyPDF2
# lru_cache es un decorador que sirve para crear una caché simple.
from functools import lru_cache

# Se define la ruta al PDF de forma segura, sin importar desde dónde se ejecute el script.
PDF_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "Accessible_Travel_Guide_Partial.pdf")


# @lru_cache(maxsize=1) La primera vez que se llame a esta
# función, ejecuta su código y guarda el resultado en memoria. Las siguientes
# veces, no la ejecutes de nuevo, simplemente devuelve el resultado guardado".
# Esto asegura que el PDF, que es una operación pesada, se lea solo una vez.
@lru_cache(maxsize=1)
def get_pdf_context() -> str:
    """Lee y extrae el texto del PDF, usando una caché para eficiencia."""
    print(f"Cargando el contexto del PDF desde: {PDF_FILE_PATH}...")
    
    # Comprueba si el archivo existe antes de intentar abrirlo.
    if not os.path.exists(PDF_FILE_PATH):
        raise FileNotFoundError(f"No se encontró el archivo PDF en: {PDF_FILE_PATH}")
    
    # Abre el archivo PDF en modo de lectura binaria ('rb').
    with open(PDF_FILE_PATH, 'rb') as pdf_file:
        # Crea un objeto lector de PDF.
        reader = PyPDF2.PdfReader(pdf_file)
        # Une el texto de todas las páginas en una sola cadena.
        text = "".join(page.extract_text() for page in reader.pages if page.extract_text())

    print("Contexto del PDF cargado con éxito.")
    return text
