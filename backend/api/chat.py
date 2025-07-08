import json
import requests
# APIRouter permite agrupar rutas en un módulo separado.
# Depends se usa para la inyección de dependencias.
from fastapi import APIRouter, Depends
# StreamingResponse es una clase especial para enviar respuestas en tiempo real.
from fastapi.responses import StreamingResponse
# BaseModel se usa para definir la estructura de los datos de entrada.
from pydantic import BaseModel
from typing import Generator, List, Dict, Any

# Se importan los módulos necesarios del proyecto.
from core.config import settings
from services.pdf_service import get_pdf_context
from core.dependencies import conversation_histories

# --- Modelos de Datos ---
# Definen "contratos" para la API. FastAPI validará automáticamente
# que las peticiones entrantes tengan esta estructura.
class ChatRequest(BaseModel):
    message: str
    conversation_id: str

class ResetRequest(BaseModel):
    conversation_id: str

# --- Router ---
# Se crea una instancia del router.
router = APIRouter()

# --- Lógica de Negocio ---
def _stream_openai_response(messages: List[Dict[str, str]], history: List[Dict[str, str]]) -> Generator[str, Any, None]:
    """Función generadora para transmitir la respuesta de OpenAI como SSE."""
    # Prepara las cabeceras y el cuerpo de la petición a la API de OpenAI.
    headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "gpt-4o", "messages": messages, "stream": True}

    full_bot_response = ""
    try:
        # Realiza la petición POST.
        with requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, stream=True) as response:
            response.raise_for_status() # Lanza un error si la respuesta no es 200 OK.
            # Itera sobre cada línea que llega en la respuesta.
            for chunk in response.iter_lines():
                if not chunk or not chunk.startswith(b'data: '): continue
                
                json_str = chunk.decode('utf-8')[6:] # Extrae el JSON del evento.
                if json_str.strip() == '[DONE]': break # Señal de fin de OpenAI.
                
                try:
                    data = json.loads(json_str)
                    content_piece = data["choices"][0]["delta"].get("content", "")
                    if content_piece:
                        full_bot_response += content_piece
                        # Prepara el dato para ser enviado como un Server-Sent Event (SSE).
                        sse_data = json.dumps({"type": "content", "content": content_piece})
                        # 'yield' produce el dato y lo envía al cliente inmediatamente.
                        yield f"data: {sse_data}\\n\\n"
                except (json.JSONDecodeError, KeyError): continue
        
        # Al finalizar, guarda la respuesta completa en el historial.
        history.append({"role": "assistant", "content": full_bot_response})
    except requests.RequestException as e:
        yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\\n\\n"
    finally:
        # Envía un evento final para que el frontend sepa que la transmisión ha terminado.
        yield f"data: {json.dumps({'type': 'done'})}\\n\\n"

# --- Endpoints ---
# Define la ruta POST /chat.
@router.post("/chat", tags=["Chat"])
async def handle_chat(
    request: ChatRequest, 
    # Inyección de Dependencias: FastAPI llamará a get_pdf_context
    # y pasará el resultado en la variable 'pdf_context'.
    pdf_context: str = Depends(get_pdf_context)
):
    """Procesa un mensaje del usuario y devuelve una respuesta en streaming."""
    # Obtiene el historial de la sesión o crea uno nuevo si no existe.
    history = conversation_histories.setdefault(request.conversation_id, [])
    history.append({"role": "user", "content": request.message})
    
    # Prepara el prompt del sistema que le da instrucciones al modelo de IA.
    system_prompt = {
        "role": "system",
        "content": f"Eres un asistente experto. Responde preguntas basándote únicamente en el siguiente texto:\\n\\n{pdf_context}\\n\\nSi la respuesta no está en el texto, di 'No tengo información sobre eso en el documento.'"
    }
    messages_for_api = [system_prompt] + history
    
    # Devuelve un objeto StreamingResponse, que llamará a la función generadora.
    return StreamingResponse(_stream_openai_response(messages_for_api, history), media_type="text/event-stream")

@router.post("/reset", tags=["Chat"])
async def handle_reset(request: ResetRequest):
    """Reinicia el historial de una conversación."""
    if request.conversation_id in conversation_histories:
        del conversation_histories[request.conversation_id]
    return {"status": "ok", "message": "Conversación reiniciada"}
