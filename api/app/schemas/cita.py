from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.cita import EstadoCita

class CitaBase(BaseModel):
    fecha_hora: datetime
    motivo_consulta: Optional[str] = None

class CitaCreate(CitaBase):
    doctor_id: int
    especialidad_id: int
    paciente_id: int

class Cita(CitaBase):
    id: int
    paciente_id: int
    doctor_id: int
    especialidad_id: int
    estado: EstadoCita

    class Config:
        from_attributes = True
