# Importa la clase principal de FastAPI para crear la aplicación.
from fastapi import FastAPI
# Importa el middleware de CORS para permitir la comunicación con el frontend.
from fastapi.middleware.cors import CORSMiddleware
# Importa nuestro módulo de rutas del chat como un alias para mayor claridad.
from api import chat as chat_router

# --- Aplicación Principal ---
# Se crea la instancia de la aplicación. Los metadatos como 'title' y 'description'
# se usarán para generar la documentación automática.
app = FastAPI(
    title="Chatbot PDF",
    description="Un chatbot para viajes.",
    version="3.2.0"
)

# Habilita CORS para permitir la comunicación con el frontend.
# Esto es una medida de seguridad del navegador. Con esta configuración,
# le dice al navegador que es seguro el frontend (en localhost:5500)
# y se comunique con el backend (en localhost:8000).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite cualquier origen.
    allow_credentials=True, # Permite el envío de cookies.
    allow_methods=["*"], # Permite todos los métodos HTTP.
    allow_headers=["*"], # Permite todas las cabeceras HTTP.
)

# Incluye las rutas del chat (/chat, /reset) en la aplicación.
app.include_router(chat_router.router)

# Endpoint de verificación de estado.
# Define una ruta GET en la raíz de la API.
@app.get("/health", tags=["Health Check"])
async def health_check():
    """Confirma que la aplicación está en funcionamiento."""
    # Devuelve una respuesta JSON simple.
    return {"status": "ok"}