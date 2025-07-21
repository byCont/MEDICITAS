# app/auth/services.py
# servicios de autenticacion

from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import Usuario, RefreshToken
from ..schemas import UsuarioRegistro, Token
from .utils import PasswordUtils, JWTUtils
from ..config import settings

class AuthService:
    """Servicio de autenticación"""
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[Usuario]:
        """Autenticar usuario"""
        user = db.query(Usuario).filter(Usuario.email == email).first()
        if not user:
            return None
        if not user.activo:
            return None
        if not PasswordUtils.verify_password(password, user.password_hash):
            return None
        return user
    
    @staticmethod
    def create_user(db: Session, user_data: UsuarioRegistro) -> Usuario:
        """Crear nuevo usuario"""
        # Verificar si el email ya existe
        if db.query(Usuario).filter(Usuario.email == user_data.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Crear usuario
        hashed_password = PasswordUtils.hash_password(user_data.password)
        db_user = Usuario(
            nombre_completo=user_data.nombre_completo,
            email=user_data.email,
            password_hash=hashed_password,
            telefono=user_data.telefono,
            fecha_nacimiento=user_data.fecha_nacimiento,
            rol=user_data.rol
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def create_tokens(db: Session, user: Usuario) -> Token:
        """Crear tokens de acceso y refresco"""
        # Crear access token
        access_token = JWTUtils.create_access_token(
            data={"sub": user.email, "user_id": user.id, "role": user.rol.value}
        )
        
        # Crear refresh token
        refresh_token = JWTUtils.create_refresh_token(
            data={"sub": user.email, "user_id": user.id}
        )
        
        # Guardar refresh token en la base de datos
        db_refresh_token = RefreshToken(
            usuario_id=user.id,
            token=refresh_token,
            fecha_expiracion=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        db.add(db_refresh_token)
        
        # Actualizar último acceso
        user.ultimo_acceso = datetime.utcnow()
        db.commit()
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> Token:
        """Refrescar token de acceso"""
        # Verificar refresh token en la base de datos
        db_token = db.query(RefreshToken).filter(
            RefreshToken.token == refresh_token,
            RefreshToken.activo == True,
            RefreshToken.fecha_expiracion > datetime.utcnow()
        ).first()
        
        if not db_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido o expirado"
            )
        
        # Decodificar token
        try:
            payload = JWTUtils.decode_token(refresh_token)
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Tipo de token inválido"
                )
        except HTTPException:
            # Marcar token como inactivo
            db_token.activo = False
            db.commit()
            raise
        
        # Obtener usuario
        user = db.query(Usuario).filter(Usuario.id == payload.get("user_id")).first()
        if not user or not user.activo:
            db_token.activo = False
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no válido"
            )
        
        # Crear nuevo access token
        new_access_token = JWTUtils.create_access_token(
            data={"sub": user.email, "user_id": user.id, "role": user.rol.value}
        )
        
        return Token(
            access_token=new_access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    @staticmethod
    def logout_user(db: Session, refresh_token: str) -> bool:
        """Cerrar sesión de usuario"""
        db_token = db.query(RefreshToken).filter(
            RefreshToken.token == refresh_token,
            RefreshToken.activo == True
        ).first()
        
        if db_token:
            db_token.activo = False
            db.commit()
            return True
        return False