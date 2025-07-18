from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config import get_db
from app.models.usuario import TipoRol
from app.models.perfil_doctor import PerfilDoctor
from app.schemas.doctor import PerfilDoctor as PerfilDoctorSchema, PerfilDoctorCreate
from app.dependencies import role_checker

router = APIRouter(
    prefix="/doctores",
    tags=["Doctores"],
)

@router.post("/", response_model=PerfilDoctorSchema, status_code=status.HTTP_201_CREATED, dependencies=[role_checker([TipoRol.ADMINISTRADOR])])
def create_perfil_doctor(perfil: PerfilDoctorCreate, db: Session = Depends(get_db)):
    # TODO: Verificar que el usuario_id corresponde a un usuario con rol 'Doctor'
    db_perfil = PerfilDoctor(**perfil.model_dump())
    db.add(db_perfil)
    db.commit()
    db.refresh(db_perfil)
    return db_perfil

@router.get("/", response_model=List[PerfilDoctorSchema])
def get_all_doctores(db: Session = Depends(get_db)):
    return db.query(PerfilDoctor).all()

@router.get("/{doctor_id}", response_model=PerfilDoctorSchema)
def get_perfil_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_perfil = db.query(PerfilDoctor).filter(PerfilDoctor.id == doctor_id).first()
    if not db_perfil:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil de doctor no encontrado")
    return db_perfil
