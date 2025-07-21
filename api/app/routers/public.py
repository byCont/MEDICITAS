# app/routers/public.py
# rutas publicas

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from ..schemas import EspecialidadResponse
from ..models import (
    Usuario, Especialidad, RefreshToken, Cita, PerfilDoctor, 
    Resena, Notificacion, TipoRol, EstadoCita, DoctorEspecialidad
)
from ..dependencies import require_role

router = APIRouter(tags=["Public"])

@router.get("/")
def root():
    return {
        "message": "Bienvenido a MediCitas API",
        "slogan": "Especialistas para ti, cuando lo necesitas.",
        "version": "2.0.0",
        "auth_enabled": True,
        "public_endpoints": [
            "/docs",
            "/health",
            "/especialidades/",
            "/doctores/",
            "/doctores/{doctor_id}",
            "/doctores/especialidad/{especialidad_id}"
        ]
    }

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Verificar la conexión a la base de datos"""
    try:
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@router.get("/especialidades/", response_model=List[dict])
def obtener_especialidades_publicas(db: Session = Depends(get_db)):
    """Obtener lista de especialidades con conteo de doctores (público)"""
    especialidades = db.query(Especialidad).all()
    
    resultado = []
    for especialidad in especialidades:
        # Contar doctores en esta especialidad
        count_doctores = (
            db.query(DoctorEspecialidad)
            .filter(DoctorEspecialidad.especialidad_id == especialidad.id)
            .count()
        )
        
        resultado.append({
            "id": especialidad.id,
            "nombre": especialidad.nombre,
            "descripcion": especialidad.descripcion,
            "total_doctores": count_doctores,
            "fecha_creacion": especialidad.fecha_creacion
        })
    
    return resultado

@router.get("/especialidades/{especialidad_id}")
def obtener_especialidad_detalle(
    especialidad_id: int,
    db: Session = Depends(get_db)
):
    """Obtener detalles de una especialidad específica (público)"""
    especialidad = db.query(Especialidad).filter(Especialidad.id == especialidad_id).first()
    
    if not especialidad:
        raise HTTPException(
            status_code=404,
            detail="Especialidad no encontrada"
        )
    
    # Contar doctores en esta especialidad
    count_doctores = (
        db.query(DoctorEspecialidad)
        .filter(DoctorEspecialidad.especialidad_id == especialidad.id)
        .count()
    )
    
    return {
        "id": especialidad.id,
        "nombre": especialidad.nombre,
        "descripcion": especialidad.descripcion,
        "total_doctores": count_doctores,
        "fecha_creacion": especialidad.fecha_creacion
    }

@router.get("/stats")
def obtener_estadisticas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role([TipoRol.ADMINISTRADOR]))
):
    """Obtener estadísticas del sistema (solo administradores)"""
    try:
        stats = {
            "usuarios_total": db.query(Usuario).count(),
            "pacientes": db.query(Usuario).filter(Usuario.rol == TipoRol.PACIENTE).count(),
            "doctores": db.query(Usuario).filter(Usuario.rol == TipoRol.DOCTOR).count(),
            "administradores": db.query(Usuario).filter(Usuario.rol == TipoRol.ADMINISTRADOR).count(),
            "especialidades": db.query(Especialidad).count(),
            "citas_total": db.query(Cita).count(),
            "citas_programadas": db.query(Cita).filter(Cita.estado == EstadoCita.PROGRAMADA).count(),
            "citas_confirmadas": db.query(Cita).filter(Cita.estado == EstadoCita.CONFIRMADA).count(),
            "citas_completadas": db.query(Cita).filter(Cita.estado == EstadoCita.COMPLETADA).count(),
            "resenas_total": db.query(Resena).count(),
            "notificaciones_total": db.query(Notificacion).count(),
            "tokens_activos": db.query(RefreshToken).filter(
                RefreshToken.activo == True,
                RefreshToken.fecha_expiracion > datetime.utcnow()
            ).count()
        }
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")

@router.get("/stats/public")
def obtener_estadisticas_publicas(db: Session = Depends(get_db)):
    """Obtener estadísticas públicas básicas"""
    try:
        stats = {
            "total_doctores": db.query(Usuario).filter(Usuario.rol == TipoRol.DOCTOR).count(),
            "total_especialidades": db.query(Especialidad).count(),
            "citas_completadas": db.query(Cita).filter(Cita.estado == EstadoCita.COMPLETADA).count(),
            "resenas_total": db.query(Resena).count()
        }
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")