# app/routers/auth.py
# rutas de autenticación

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UsuarioRegistro, UsuarioLogin, Token, TokenRefresh, UsuarioResponse
from ..auth.services import AuthService
from ..dependencies import get_current_active_user
from ..models import Usuario

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/registro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(user_data: UsuarioRegistro, db: Session = Depends(get_db)):
    """Registrar nuevo usuario"""
    try:
        user = AuthService.create_user(db, user_data)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.post("/login", response_model=Token)
def iniciar_sesion(user_credentials: UsuarioLogin, db: Session = Depends(get_db)):
    """Iniciar sesión de usuario"""
    user = AuthService.authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return AuthService.create_tokens(db, user)

@router.post("/refresh", response_model=Token)
def refrescar_token(token_data: TokenRefresh, db: Session = Depends(get_db)):
    """Refrescar token de acceso"""
    return AuthService.refresh_access_token(db, token_data.refresh_token)

@router.post("/logout")
def cerrar_sesion(token_data: TokenRefresh, db: Session = Depends(get_db)):
    """Cerrar sesión de usuario"""
    success = AuthService.logout_user(db, token_data.refresh_token)
    if success:
        return {"message": "Sesión cerrada exitosamente"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token de refresco inválido"
        )

@router.get("/me", response_model=UsuarioResponse)
def obtener_usuario_actual(current_user: Usuario = Depends(get_current_active_user)):
    """Obtener información del usuario actual"""
    return current_user

@router.get("/profile", response_model=UsuarioResponse)
def obtener_perfil_usuario(current_user: Usuario = Depends(get_current_active_user)):
    """Obtener perfil completo del usuario actual"""
    return current_user