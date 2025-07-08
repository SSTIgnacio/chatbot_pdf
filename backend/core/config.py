# Importa las herramientas necesarias de la biblioteca pydantic-settings.
from pydantic_settings import BaseSettings, SettingsConfigDict

# Se define una clase que hereda de BaseSettings.
class Settings(BaseSettings):
    # Se declara un campo obligatorio. Pydantic se asegurará de que
    # la variable de entorno OPENAI_API_KEY exista al iniciar la app.
    OPENAI_API_KEY: str
    
    # Se configura el comportamiento de la clase Settings.
    model_config = SettingsConfigDict(
        # Le dice a Pydantic que busque un archivo llamado ".env".
        env_file=".env",
        # Le dice a Pydantic que no diferencie mayúsculas de minúsculas.
        case_sensitive=False 
    )

# Se crea una instancia única de la configuración.
# Al crearla, Pydantic lee y valida automáticamente el archivo .env.
# Esta instancia 'settings' se importará en otros módulos para usar la clave.
settings = Settings()