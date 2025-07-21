# app/schemas.py
# esquemas pydantic

from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
from datetime import datetime, date
from .models import TipoRol, EstadoCita

# Schemas de autenticación
class UsuarioRegistro(BaseModel):
    nombre_completo: str
    email: EmailStr
    password: str
    telefono: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    rol: TipoRol = TipoRol.PACIENTE
    
    @validator('password')
    def validate_password(cls, v):
        from .auth.utils import PasswordUtils
        if not PasswordUtils.validate_password_strength(v):
            raise ValueError('La contraseña debe tener al menos 8 caracteres, incluir mayúsculas, minúsculas y números')
        return v
    
    @validator('nombre_completo')
    def validate_nombre(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('El nombre completo debe tener al menos 2 caracteres')
        return v.strip()

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenRefresh(BaseModel):
    refresh_token: str

class UsuarioResponse(BaseModel):
    id: int
    nombre_completo: str
    email: str
    telefono: Optional[str]
    fecha_nacimiento: Optional[date]
    rol: TipoRol
    activo: bool
    email_verificado: bool
    ultimo_acceso: Optional[datetime]
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True

class UsuarioActual(BaseModel):
    id: int
    email: str
    rol: TipoRol
    activo: bool

# Schemas de doctores
class DoctorResponse(BaseModel):
    id: int
    nombre_completo: str
    email: str
    telefono: Optional[str]
    cedula_profesional: str
    biografia: Optional[str]
    foto_perfil_url: Optional[str]
    especialidades: List[str]

# Schemas de citas
class CitaResponse(BaseModel):
    id: int
    paciente_id: Optional[int]
    doctor_id: int
    especialidad_id: int
    fecha_hora: datetime
    duracion_minutos: int
    estado: EstadoCita
    motivo_consulta: Optional[str]
    notas_doctor: Optional[str]
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True

# Schemas de especialidades
class EspecialidadResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    
    class Config:
        from_attributes = True