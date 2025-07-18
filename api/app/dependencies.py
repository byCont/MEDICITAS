# Archivo: app/dependencies.py
# VERSIÓN CORREGIDA

from fastapi import Depends, HTTPException, status, Request
from typing import List
from app.models.usuario import TipoRol

def role_checker(allowed_roles: List[TipoRol]):
    """
    Crea una dependencia de FastAPI que verifica si el rol del usuario, 
    extraído del token JWT, está en la lista de roles permitidos.
    """
    def checker(request: Request):
        user_payload = getattr(request.state, "user", None)
        if not user_payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No autenticado."
            )

        user_role_str = user_payload.get("role")
        if not user_role_str:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El token no contiene el rol del usuario."
            )

        try:
            user_role = TipoRol(user_role_str)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"El rol '{user_role_str}' es inválido."
            )

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para realizar esta acción."
            )
        
        return user_payload

    # CAMBIO IMPORTANTE: Devolver solo 'checker' en lugar de 'Depends(checker)'
    return checker
