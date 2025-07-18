from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config import get_db
from app.models.usuario import Usuario
from app.schemas.auth import UsuarioCreate, LoginRequest, Token
from app.security import get_password_hash, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=Token)
def register(user: UsuarioCreate, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado."
        )
    
    hashed_password = get_password_hash(user.password)
    db_user = Usuario(
        nombre_completo=user.nombre_completo,
        email=user.email,
        password_hash=hashed_password,
        telefono=user.telefono,
        fecha_nacimiento=user.fecha_nacimiento,
        rol=user.rol
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token = create_access_token(data={"sub": db_user.email, "role": db_user.rol.value})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(form_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == form_data.email).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La cuenta está inactiva."
        )

    access_token = create_access_token(data={"sub": user.email, "role": user.rol.value})
    return {"access_token": access_token, "token_type": "bearer"}