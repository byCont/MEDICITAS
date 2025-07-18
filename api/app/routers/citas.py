from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config import get_db
from app.models.usuario import TipoRol
from app.models.cita import Cita
from app.schemas.cita import Cita as CitaSchema, CitaCreate
from app.dependencies import role_checker

router = APIRouter(
    prefix="/citas",
    tags=["Citas"],
)

@router.post("/", response_model=CitaSchema, status_code=status.HTTP_201_CREATED, dependencies=[role_checker([TipoRol.PACIENTE, TipoRol.ADMINISTRADOR])])
def create_cita(cita: CitaCreate, db: Session = Depends(get_db)):
    # TODO: Añadir validación para asegurar que el doctor está disponible en esa fecha y hora.
    db_cita = Cita(**cita.model_dump())
    db.add(db_cita)
    db.commit()
    db.refresh(db_cita)
    return db_cita

@router.get("/", response_model=List[CitaSchema], dependencies=[role_checker([TipoRol.ADMINISTRADOR])])
def get_all_citas(db: Session = Depends(get_db)):
    return db.query(Cita).all()

@router.get("/{cita_id}", response_model=CitaSchema, dependencies=[role_checker([TipoRol.PACIENTE, TipoRol.DOCTOR, TipoRol.ADMINISTRADOR])])
def get_cita(cita_id: int, db: Session = Depends(get_db)):
    # TODO: Añadir lógica para que un paciente o doctor solo pueda ver sus propias citas.
    db_cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not db_cita:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada")
    return db_cita
