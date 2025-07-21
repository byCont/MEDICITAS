# app/config.py
# configuracion de la aplicacion

import os
import secrets
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la aplicación
class Settings:
    # Base de datos
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # Seguridad
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # API
    API_TITLE: str = "MediCitas API con Autenticación"
    API_DESCRIPTION: str = "Especialistas para ti, cuando lo necesitas."
    API_VERSION: str = "2.0.0"

settings = Settings()