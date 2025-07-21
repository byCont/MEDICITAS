# app/routers/appointments.py
# rutas de citas

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import CitaResponse
from ..models import Cita, PerfilDoctor, Usuario, TipoRol
from ..dependencies import get_current_active_user

router = APIRouter(prefix="/citas", tags=["Appointments"])

@router.get("/mis-citas", response_model=List[CitaResponse])
def obtener_mis_citas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener citas del usuario actual"""
    if current_user.rol == TipoRol.PACIENTE:
        citas = db.query(Cita).filter(Cita.paciente_id == current_user.id).all()
    elif current_user.rol == TipoRol.DOCTOR:
        doctor_perfil = db.query(PerfilDoctor).filter(PerfilDoctor.usuario_id == current_user.id).first()
        if doctor_perfil:
            citas = db.query(Cita).filter(Cita.doctor_id == doctor_perfil.id).all()
        else:
            citas = []
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo pacientes y doctores pueden ver sus citas"
        )
    
    return citas