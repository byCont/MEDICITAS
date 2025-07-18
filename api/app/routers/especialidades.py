from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config import get_db
from app.models.usuario import TipoRol
from app.models.especialidad import Especialidad
from app.schemas.especialidad import Especialidad as EspecialidadSchema, EspecialidadCreate
from app.dependencies import role_checker

router = APIRouter(
    prefix="/especialidades",
    tags=["Especialidades"],
)

@router.post("/", response_model=EspecialidadSchema, status_code=status.HTTP_201_CREATED, dependencies=[role_checker([TipoRol.ADMINISTRADOR])])
def create_especialidad(especialidad: EspecialidadCreate, db: Session = Depends(get_db)):
    db_especialidad = Especialidad(**especialidad.model_dump())
    db.add(db_especialidad)
    db.commit()
    db.refresh(db_especialidad)
    return db_especialidad

@router.get("/", response_model=List[EspecialidadSchema])
def get_all_especialidades(db: Session = Depends(get_db)):
    return db.query(Especialidad).all()

@router.get("/{especialidad_id}", response_model=EspecialidadSchema)
def get_especialidad(especialidad_id: int, db: Session = Depends(get_db)):
    db_especialidad = db.query(Especialidad).filter(Especialidad.id == especialidad_id).first()
    if not db_especialidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Especialidad no encontrada")
    return db_especialidad

@router.put("/{especialidad_id}", response_model=EspecialidadSchema, dependencies=[role_checker([TipoRol.ADMINISTRADOR])])
def update_especialidad(especialidad_id: int, especialidad: EspecialidadCreate, db: Session = Depends(get_db)):
    db_especialidad = db.query(Especialidad).filter(Especialidad.id == especialidad_id).first()
    if not db_especialidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Especialidad no encontrada")
    
    for var, value in vars(especialidad).items():
        setattr(db_especialidad, var, value) if value else None

    db.commit()
    db.refresh(db_especialidad)
    return db_especialidad

@router.delete("/{especialidad_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker([TipoRol.ADMINISTRADOR])])
def delete_especialidad(especialidad_id: int, db: Session = Depends(get_db)):
    db_especialidad = db.query(Especialidad).filter(Especialidad.id == especialidad_id).first()
    if not db_especialidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Especialidad no encontrada")
    
    db.delete(db_especialidad)
    db.commit()
    return {"ok": True}
