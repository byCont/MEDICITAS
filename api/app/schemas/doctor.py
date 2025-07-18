from pydantic import BaseModel
from typing import Optional, List
from .especialidad import Especialidad

class PerfilDoctorBase(BaseModel):
    cedula_profesional: str
    biografia: Optional[str] = None
    foto_perfil_url: Optional[str] = None

class PerfilDoctorCreate(PerfilDoctorBase):
    usuario_id: int

class PerfilDoctor(PerfilDoctorBase):
    id: int
    usuario_id: int
    especialidades: List[Especialidad] = []

    class Config:
        from_attributes = True
