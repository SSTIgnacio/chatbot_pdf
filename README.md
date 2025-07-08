Chatbot con Contexto de PDF
Este proyecto es una aplicación web full-stack que implementa un chatbot inteligente. El chatbot es capaz de responder preguntas basadas exclusivamente en el contenido de un documento PDF proporcionado, utilizando la API de OpenAI para el procesamiento del lenguaje natural.

La aplicación está diseñada siguiendo una arquitectura profesional, con una clara separación entre el backend (servidor de lógica) y el frontend (interfaz de usuario).

Arquitectura
El proyecto está dividido en dos componentes principales:

Backend (FastAPI): Un servidor robusto y asíncrono construido con FastAPI. Se encarga de:

Cargar y procesar el documento PDF al iniciar.

Gestionar las peticiones de la API de forma segura.

Integrarse con la API de OpenAI para generar respuestas.

Transmitir las respuestas en tiempo real al cliente usando Server-Sent Events (SSE).

Mantener un historial de conversación en memoria para cada sesión de usuario.

Frontend (React): Una moderna Single-Page Application (SPA) construida con React y Vite. Se encarga de:

Proporcionar una ventana de chat intuitiva y reactiva.

Gestionar el estado de la interfaz de forma eficiente.

Enviar las preguntas del usuario al backend.

Recibir y mostrar las respuestas del bot en tiempo real.

Características
Respuestas Basadas en Contexto: El bot solo utiliza la información del PDF, evitando alucinaciones o datos externos.

Streaming en Tiempo Real: Las respuestas del bot aparecen palabra por palabra, mejorando la experiencia de usuario.

Arquitectura Modular: El código del backend está organizado por responsabilidades (API, servicios, configuración), facilitando su mantenimiento y escalabilidad.

Manejo Seguro de Secretos: La clave de la API de OpenAI se gestiona de forma segura a través de un archivo .env.

Documentación de API Automática: Gracias a FastAPI, se puede acceder a una documentación interactiva de la API en http://localhost:8000/docs.

Control de Versiones con GitHub
Este proyecto utiliza una estrategia de ramificación Git Flow simplificada para asegurar un desarrollo ordenado y un código estable.

main: Esta rama contiene únicamente el código de producción, estable y probado. No se debe hacer push directamente a esta rama.

QA (Quality Assurance): Esta es una rama de pre-producción. El código de develop se fusiona aquí para realizar pruebas exhaustivas.

develop: Es la rama principal de desarrollo. Todo el código nuevo se integra aquí.

Flujo de trabajo:

El desarrollo se realiza en la rama develop.

Cuando una funcionalidad está lista para ser probada, se crea un Pull Request de develop a QA.

Una vez que las pruebas en QA son exitosas, se crea un Pull Request de QA a main para lanzar la nueva versión estable.

Requisitos Previos
Python 3.8+

Node.js 18+ y npm

Una clave de API de OpenAI.

Instalación y Ejecución
Sigue estos pasos para poner en marcha el proyecto en tu máquina local.

1. Configuración del Backend
Navega a la carpeta del backend y configura el entorno.

# 1. Ve a la carpeta del backend
cd backend

# 2. Crea un entorno virtual de Python
python -m venv .venv

# 3. Activa el entorno virtual
# En Windows (CMD):
.venv\Scripts\activate
# En Mac/Linux:
# source .venv/bin/activate

# 4. Instala las dependencias necesarias
pip install -r requirements.txt

# 5. Configura tu clave de API
# Crea un archivo llamado .env dentro de la carpeta backend/
# y añade tu clave de API de OpenAI de la siguiente manera:
# OPENAI_API_KEY="sk-..."

2. Ejecución del Servidor Backend
Con el entorno virtual activado, inicia el servidor FastAPI.

# Desde la carpeta backend/
python -m uvicorn main:app --reload --port 8001

El servidor estará disponible en http://localhost:8001/docs.
