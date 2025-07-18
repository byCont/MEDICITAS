# Ejemplo de corrección en los archivos de rutas
# Archivo: app/routers/usuarios.py (y otros archivos de rutas)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config import get_db
from app.models.usuario import Usuario, TipoRol
from app.schemas.usuario import Usuario as UsuarioSchema
from app.dependencies import role_checker

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
)

# CAMBIO IMPORTANTE: Usar Depends() alrededor de role_checker() en dependencies
@router.get("/", response_model=List[UsuarioSchema], dependencies=[Depends(role_checker([TipoRol.ADMINISTRADOR]))])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

# CAMBIO IMPORTANTE: Usar Depends() alrededor de role_checker() en parámetros de función
@router.get("/me", response_model=UsuarioSchema)
def get_me(current_user: dict = Depends(role_checker([TipoRol.PACIENTE, TipoRol.DOCTOR, TipoRol.ADMINISTRADOR]))):
    user_email = current_user.get("sub")
    db = next(get_db())
    user = db.query(Usuario).filter(Usuario.email == user_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user
