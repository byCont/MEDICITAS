import jwt
from fastapi import Request, Response
from typing import Callable
from app import settings

# Rutas que no requieren autenticación
PUBLIC_PATHS = [
    "/api/login",
    "/api/register",  # Asumiendo que habrá un endpoint de registro
    "/docs",
    "/openapi.json",
    "/uploads"
]

async def authenticate(request: Request, next: Callable):
    # Comprobar si la ruta es pública
    is_public = any(request.url.path.startswith(path) for path in PUBLIC_PATHS)

    if is_public:
        return await next(request)

    # Si no es pública, verificar el token
    header = request.headers.get("Authorization")
    if not header or not header.startswith("Bearer "):
        return Response(status_code=401, content="No se proporcionó token de autenticación.")

    token = header.split(" ")[1]

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        # TODO: Verificar que el usuario (payload.get("sub")) existe y está activo en la BBDD.
        # Esto es crucial para la seguridad, para poder revocar sesiones.
        request.state.user = payload
    except jwt.ExpiredSignatureError:
        return Response(status_code=401, content="El token ha expirado.")
    except jwt.InvalidTokenError:
        return Response(status_code=401, content="Token inválido.")

    return await next(request)