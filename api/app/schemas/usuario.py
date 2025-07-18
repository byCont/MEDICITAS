from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from app.models.usuario import TipoRol

class UsuarioBase(BaseModel):
    nombre_completo: str
    email: EmailStr
    telefono: Optional[str] = None

class Usuario(UsuarioBase):
    id: int
    rol: TipoRol
    activo: bool
    fecha_creacion: date

    class Config:
        from_attributes = True
