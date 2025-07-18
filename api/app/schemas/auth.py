from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from app.models.usuario import TipoRol

class UsuarioCreate(BaseModel):
    nombre_completo: str
    email: EmailStr
    password: str
    telefono: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    rol: TipoRol

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[str] = None
