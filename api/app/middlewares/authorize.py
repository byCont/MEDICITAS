# Este middleware ha sido descontinuado.
# La autorización ahora se gestiona a través de dependencias en cada endpoint.

from fastapi import Request
from typing import Callable

async def authorize(request: Request, next: Callable):
    # La lógica de autorización se ha movido a dependencias.
    # Este middleware ya no es necesario y puede ser eliminado de main.py.
    return await next(request)

    return Response(status_code=403)