import os

# Se recomienda gestionar los secretos a través de variables de entorno en producción
JWT_SECRET = os.environ.get("JWT_SECRET", "a_secret_key_that_should_be_changed")
ALGORITHM = "HS256"

# 60 minutos * 24 horas * 8 dias = 8 dias de vida para el token
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8
