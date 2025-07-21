from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UsuarioResponse
from ..models import Usuario, TipoRol
from ..dependencies import require_role

router = APIRouter(prefix="/usuarios", tags=["Users"])

@router.get("/", response_model=List[UsuarioResponse])
def obtener_usuarios(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role([TipoRol.ADMINISTRADOR]))
):
    """Obtener lista de usuarios (solo administradores)"""
    usuarios = db.query(Usuario).offset(skip).limit(limit).all()
    return usuarios