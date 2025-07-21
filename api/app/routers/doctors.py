# app/routers/doctors.py
# rutas de doctores

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import DoctorResponse
from ..models import PerfilDoctor, DoctorEspecialidad, Especialidad

router = APIRouter(prefix="/doctores", tags=["Doctors"])

@router.get("/", response_model=List[DoctorResponse])
def obtener_doctores(
    especialidad_id: Optional[int] = Query(None, description="ID de la especialidad para filtrar doctores"),
    especialidad_nombre: Optional[str] = Query(None, description="Nombre de la especialidad para filtrar doctores"),
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=100, description="Número máximo de registros a retornar"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de doctores (ruta pública)
    
    Parámetros opcionales:
    - especialidad_id: Filtrar por ID de especialidad
    - especialidad_nombre: Filtrar por nombre de especialidad (búsqueda parcial)
    - skip: Paginación - registros a omitir
    - limit: Paginación - máximo de registros
    """
    # Construir la consulta base
    query = db.query(PerfilDoctor).join(PerfilDoctor.usuario)
    
    # Filtrar por especialidad si se proporciona
    if especialidad_id is not None:
        query = query.join(PerfilDoctor.especialidades).join(DoctorEspecialidad.especialidad).filter(
            Especialidad.id == especialidad_id
        )
    elif especialidad_nombre is not None:
        query = query.join(PerfilDoctor.especialidades).join(DoctorEspecialidad.especialidad).filter(
            Especialidad.nombre.ilike(f"%{especialidad_nombre}%")
        )
    
    # Aplicar paginación
    doctores = query.offset(skip).limit(limit).all()
    
    # Formatear la respuesta
    resultado = []
    for doctor in doctores:
        especialidades = [de.especialidad.nombre for de in doctor.especialidades]
        resultado.append({
            "id": doctor.id,
            "nombre_completo": doctor.usuario.nombre_completo,
            "email": doctor.usuario.email,
            "telefono": doctor.usuario.telefono,
            "cedula_profesional": doctor.cedula_profesional,
            "biografia": doctor.biografia,
            "foto_perfil_url": doctor.foto_perfil_url,
            "especialidades": especialidades
        })
    
    return resultado

@router.get("/{doctor_id}", response_model=DoctorResponse)
def obtener_doctor_por_id(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener información detallada de un doctor específico (ruta pública)
    """
    doctor = db.query(PerfilDoctor).filter(PerfilDoctor.id == doctor_id).first()
    
    if not doctor:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor no encontrado"
        )
    
    especialidades = [de.especialidad.nombre for de in doctor.especialidades]
    
    return {
        "id": doctor.id,
        "nombre_completo": doctor.usuario.nombre_completo,
        "email": doctor.usuario.email,
        "telefono": doctor.usuario.telefono,
        "cedula_profesional": doctor.cedula_profesional,
        "biografia": doctor.biografia,
        "foto_perfil_url": doctor.foto_perfil_url,
        "especialidades": especialidades
    }

@router.get("/especialidad/{especialidad_id}", response_model=List[DoctorResponse])
def obtener_doctores_por_especialidad(
    especialidad_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Obtener doctores de una especialidad específica (ruta pública)
    Ruta alternativa más explícita para filtrar por especialidad
    """
    # Verificar que la especialidad existe
    especialidad = db.query(Especialidad).filter(Especialidad.id == especialidad_id).first()
    if not especialidad:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Especialidad no encontrada"
        )
    
    # Obtener doctores de la especialidad
    doctores = (
        db.query(PerfilDoctor)
        .join(PerfilDoctor.especialidades)
        .join(DoctorEspecialidad.especialidad)
        .filter(Especialidad.id == especialidad_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    resultado = []
    for doctor in doctores:
        especialidades = [de.especialidad.nombre for de in doctor.especialidades]
        resultado.append({
            "id": doctor.id,
            "nombre_completo": doctor.usuario.nombre_completo,
            "email": doctor.usuario.email,
            "telefono": doctor.usuario.telefono,
            "cedula_profesional": doctor.cedula_profesional,
            "biografia": doctor.biografia,
            "foto_perfil_url": doctor.foto_perfil_url,
            "especialidades": especialidades
        })
    
    return resultado