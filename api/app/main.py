#!/usr/bin/env python3
# /app/main.py
"""
Sistema de Autenticación para MediCitas API
Implementa registro, login, logout y protección de rutas con JWT
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Date, SmallInteger, BigInteger, ForeignKey, Enum as SQLEnum, CheckConstraint, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.sql import func
from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional, Union
from datetime import datetime, date, timedelta
import os
from dotenv import load_dotenv
import enum
import jwt
from passlib.context import CryptContext
from passlib.hash import bcrypt
import secrets
import re

# Cargar variables de entorno
load_dotenv()

# Configuración de seguridad
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Configuración de encriptación de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración de seguridad JWT
security = HTTPBearer()

# Definir ENUMs
class TipoRol(str, enum.Enum):
    PACIENTE = "Paciente"
    DOCTOR = "Doctor"
    ADMINISTRADOR = "Administrador"

class EstadoCita(str, enum.Enum):
    PROGRAMADA = "Programada"
    CONFIRMADA = "Confirmada"
    COMPLETADA = "Completada"
    CANCELADA = "Cancelada"
    NO_ASISTIO = "No Asistió"

class TipoNotificacion(str, enum.Enum):
    EMAIL = "Email"
    SMS = "SMS"
    PUSH = "Push"

class EventoNotificacion(str, enum.Enum):
    CITA_PROGRAMADA = "Cita_Programada"
    CITA_CONFIRMADA = "Cita_Confirmada"
    CITA_CANCELADA = "Cita_Cancelada"
    RECORDATORIO_24H = "Recordatorio_24h"
    RECORDATORIO_1H = "Recordatorio_1h"

# Modelos SQLAlchemy (actualizados con campos de autenticación)
class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(150), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    telefono = Column(String(20))
    fecha_nacimiento = Column(Date)
    rol = Column(SQLEnum(TipoRol), nullable=False)
    activo = Column(Boolean, default=True)
    email_verificado = Column(Boolean, default=False)
    ultimo_acceso = Column(DateTime(timezone=True))
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    perfil_doctor = relationship("PerfilDoctor", back_populates="usuario", uselist=False, cascade="all, delete-orphan")
    citas_como_paciente = relationship("Cita", foreign_keys="Cita.paciente_id", back_populates="paciente")
    resenas = relationship("Resena", back_populates="paciente")
    notificaciones = relationship("Notificacion", back_populates="usuario")
    tokens_refresh = relationship("RefreshToken", back_populates="usuario", cascade="all, delete-orphan")

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(255), unique=True, nullable=False, index=True)
    fecha_expiracion = Column(DateTime(timezone=True), nullable=False)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="tokens_refresh")

class Especialidad(Base):
    __tablename__ = "especialidades"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    doctor_especialidades = relationship("DoctorEspecialidad", back_populates="especialidad")
    citas = relationship("Cita", back_populates="especialidad")

class PerfilDoctor(Base):
    __tablename__ = "perfiles_doctores"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), unique=True, nullable=False)
    cedula_profesional = Column(String(50), unique=True, nullable=False)
    biografia = Column(Text)
    foto_perfil_url = Column(String(255))
    fecha_actualizacion = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="perfil_doctor")
    especialidades = relationship("DoctorEspecialidad", back_populates="doctor", cascade="all, delete-orphan")
    citas = relationship("Cita", back_populates="doctor")
    resenas = relationship("Resena", back_populates="doctor")

class DoctorEspecialidad(Base):
    __tablename__ = "doctor_especialidades"
    
    doctor_id = Column(Integer, ForeignKey("perfiles_doctores.id", ondelete="CASCADE"), primary_key=True)
    especialidad_id = Column(Integer, ForeignKey("especialidades.id", ondelete="CASCADE"), primary_key=True)
    
    # Relaciones
    doctor = relationship("PerfilDoctor", back_populates="especialidades")
    especialidad = relationship("Especialidad", back_populates="doctor_especialidades")

class Cita(Base):
    __tablename__ = "citas"
    
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"))
    doctor_id = Column(Integer, ForeignKey("perfiles_doctores.id", ondelete="CASCADE"), nullable=False)
    especialidad_id = Column(Integer, ForeignKey("especialidades.id", ondelete="RESTRICT"), nullable=False)
    fecha_hora = Column(DateTime(timezone=True), nullable=False)
    duracion_minutos = Column(Integer, nullable=False, default=30)
    estado = Column(SQLEnum(EstadoCita), nullable=False, default=EstadoCita.PROGRAMADA)
    motivo_consulta = Column(Text)
    notas_doctor = Column(Text)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Restricciones
    __table_args__ = (
        UniqueConstraint('doctor_id', 'fecha_hora', name='uq_doctor_fecha_hora'),
    )
    
    # Relaciones
    paciente = relationship("Usuario", foreign_keys=[paciente_id], back_populates="citas_como_paciente")
    doctor = relationship("PerfilDoctor", back_populates="citas")
    especialidad = relationship("Especialidad", back_populates="citas")
    resena = relationship("Resena", back_populates="cita", uselist=False)

class Resena(Base):
    __tablename__ = "resenas"
    
    id = Column(Integer, primary_key=True, index=True)
    cita_id = Column(Integer, ForeignKey("citas.id", ondelete="CASCADE"), unique=True, nullable=False)
    paciente_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("perfiles_doctores.id"), nullable=False)
    calificacion = Column(SmallInteger, nullable=False)
    comentario = Column(Text)
    es_anonima = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    
    # Restricciones
    __table_args__ = (
        CheckConstraint('calificacion >= 1 AND calificacion <= 5', name='check_calificacion_range'),
    )
    
    # Relaciones
    cita = relationship("Cita", back_populates="resena")
    paciente = relationship("Usuario", back_populates="resenas")
    doctor = relationship("PerfilDoctor", back_populates="resenas")

class Notificacion(Base):
    __tablename__ = "notificaciones"
    
    id = Column(BigInteger, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    cita_id = Column(Integer, ForeignKey("citas.id"))
    tipo = Column(SQLEnum(TipoNotificacion), nullable=False)
    evento = Column(SQLEnum(EventoNotificacion), nullable=False)
    contenido = Column(Text, nullable=False)
    enviada_exitosamente = Column(Boolean, default=False)
    fecha_envio = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="notificaciones")

# Crear las tablas
Base.metadata.create_all(bind=engine)

# Utilidades de autenticación
class PasswordUtils:
    """Utilidades para manejo de contraseñas"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Encriptar contraseña"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verificar contraseña"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def validate_password_strength(password: str) -> bool:
        """Validar fortaleza de contraseña"""
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        return True

class JWTUtils:
    """Utilidades para manejo de JWT"""
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Crear token de acceso JWT"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Crear token de refresco"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        
        to_encode.update({"exp": expire, "type": "refresh"})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def decode_token(token: str) -> dict:
        """Decodificar token JWT"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

# --- INICIO: Modelos Pydantic para Registro ---

# Modelo base para datos de usuario
class UsuarioBase(BaseModel):
    nombre_completo: str
    email: EmailStr
    password: str
    telefono: Optional[str] = None
    fecha_nacimiento: Optional[date] = None

    @validator('password')
    def validate_password(cls, v):
        if not PasswordUtils.validate_password_strength(v):
            raise ValueError('La contraseña debe tener al menos 8 caracteres, incluir mayúsculas, minúsculas y números')
        return v

    @validator('nombre_completo')
    def validate_nombre(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('El nombre completo debe tener al menos 2 caracteres')
        return v.strip()

# Modelo para registro de paciente
class UsuarioRegistro(UsuarioBase):
    rol: TipoRol = TipoRol.PACIENTE

# Modelo para datos del perfil del doctor
class PerfilDoctorCrear(BaseModel):
    cedula_profesional: str
    biografia: Optional[str] = None
    foto_perfil_url: Optional[str] = None

# Modelo para registro de doctor (combina usuario, perfil y especialidades)
class DoctorRegistro(BaseModel):
    usuario: UsuarioBase
    perfil: PerfilDoctorCrear
    especialidades_ids: List[int]

# --- FIN: Modelos Pydantic para Registro ---

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES * 60

class TokenRefresh(BaseModel):
    refresh_token: str

class UsuarioResponse(BaseModel):
    id: int
    nombre_completo: str
    email: str
    telefono: Optional[str]
    fecha_nacimiento: Optional[date]
    rol: TipoRol
    activo: bool
    email_verificado: bool
    ultimo_acceso: Optional[datetime]
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True

# --- INICIO: Modelos de Respuesta para Doctor ---
class EspecialidadResponse(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True

class PerfilDoctorResponse(BaseModel):
    id: int
    cedula_profesional: str
    biografia: Optional[str]
    foto_perfil_url: Optional[str]

    class Config:
        from_attributes = True

class DoctorResponse(UsuarioResponse):
    perfil_doctor: PerfilDoctorResponse
    especialidades: List[EspecialidadResponse]

    class Config:
        from_attributes = True
# --- FIN: Modelos de Respuesta para Doctor ---


class UsuarioActual(BaseModel):
    id: int
    email: str
    rol: TipoRol
    activo: bool

class CitaCrear(BaseModel):
    doctor_id: int
    especialidad_id: int
    fecha_hora: datetime
    motivo_consulta: Optional[str] = None
    duracion_minutos: int = 30

    @validator('fecha_hora')
    def validate_fecha_hora(cls, v):
        if v.tzinfo is None:
             v = v.replace(tzinfo=datetime.now().astimezone().tzinfo)

        if v <= datetime.now().astimezone():
            raise ValueError('La fecha y hora de la cita debe ser en el futuro.')
        
        if v.minute not in [0, 30]:
            raise ValueError('Las citas solo pueden programarse a en punto (00) o y media (30).')
        
        return v

class CitaResponse(BaseModel):
    id: int
    paciente_id: int
    doctor_id: int
    especialidad_id: int
    fecha_hora: datetime
    duracion_minutos: int
    estado: EstadoCita
    motivo_consulta: Optional[str]
    fecha_creacion: datetime

    class Config:
        from_attributes = True

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Servicios de autenticación
class AuthService:
    """Servicio de autenticación"""
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[Usuario]:
        """Autenticar usuario"""
        user = db.query(Usuario).filter(Usuario.email == email).first()
        if not user or not user.activo or not PasswordUtils.verify_password(password, user.password_hash):
            return None
        return user
    
    @staticmethod
    def create_user(db: Session, user_data: UsuarioRegistro) -> Usuario:
        """Crear nuevo usuario PACIENTE"""
        if db.query(Usuario).filter(Usuario.email == user_data.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        hashed_password = PasswordUtils.hash_password(user_data.password)
        db_user = Usuario(
            **user_data.model_dump(exclude={"password", "rol"}),
            password_hash=hashed_password,
            rol=TipoRol.PACIENTE
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def create_doctor(db: Session, doctor_data: DoctorRegistro) -> Usuario:
        """Crear un nuevo usuario DOCTOR con su perfil y especialidades"""
        # Validar duplicados
        if db.query(Usuario).filter(Usuario.email == doctor_data.usuario.email).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El email ya está registrado.")
        
        if db.query(PerfilDoctor).filter(PerfilDoctor.cedula_profesional == doctor_data.perfil.cedula_profesional).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La cédula profesional ya está registrada.")

        # Validar que las especialidades existan
        if not doctor_data.especialidades_ids:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Debe proporcionar al menos una especialidad.")
            
        especialidades_validas = db.query(Especialidad).filter(Especialidad.id.in_(doctor_data.especialidades_ids)).all()
        if len(especialidades_validas) != len(doctor_data.especialidades_ids):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Una o más especialidades no son válidas.")

        # Iniciar transacción
        try:
            # 1. Crear el usuario
            hashed_password = PasswordUtils.hash_password(doctor_data.usuario.password)
            db_user = Usuario(
                **doctor_data.usuario.model_dump(exclude={"password"}),
                password_hash=hashed_password,
                rol=TipoRol.DOCTOR
            )
            db.add(db_user)
            db.flush() # Para obtener el ID del usuario antes del commit

            # 2. Crear el perfil del doctor
            db_perfil = PerfilDoctor(
                **doctor_data.perfil.model_dump(),
                usuario_id=db_user.id
            )
            db.add(db_perfil)
            db.flush() # Para obtener el ID del perfil antes del commit

            # 3. Asociar especialidades
            for esp_id in doctor_data.especialidades_ids:
                db_doc_esp = DoctorEspecialidad(doctor_id=db_perfil.id, especialidad_id=esp_id)
                db.add(db_doc_esp)

            db.commit()
            db.refresh(db_user)
            
            # Cargar las relaciones para la respuesta
            db.refresh(db_user.perfil_doctor)
            for de in db_user.perfil_doctor.especialidades:
                db.refresh(de.especialidad)

            return db_user
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear el doctor: {e}"
            )
    
    @staticmethod
    def create_tokens(db: Session, user: Usuario) -> Token:
        """Crear tokens de acceso y refresco"""
        access_token = JWTUtils.create_access_token(
            data={"sub": user.email, "user_id": user.id, "role": user.rol.value}
        )
        refresh_token = JWTUtils.create_refresh_token(
            data={"sub": user.email, "user_id": user.id}
        )
        
        db_refresh_token = RefreshToken(
            usuario_id=user.id,
            token=refresh_token,
            fecha_expiracion=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )
        db.add(db_refresh_token)
        
        user.ultimo_acceso = func.now()
        db.commit()
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> Token:
        """Refrescar token de acceso"""
        db_token = db.query(RefreshToken).filter(
            RefreshToken.token == refresh_token,
            RefreshToken.activo == True,
            RefreshToken.fecha_expiracion > datetime.utcnow()
        ).first()
        
        if not db_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido o expirado"
            )
        
        try:
            payload = JWTUtils.decode_token(refresh_token)
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Tipo de token inválido"
                )
        except HTTPException:
            db_token.activo = False
            db.commit()
            raise
        
        user = db.query(Usuario).filter(Usuario.id == payload.get("user_id")).first()
        if not user or not user.activo:
            db_token.activo = False
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no válido"
            )
        
        new_access_token = JWTUtils.create_access_token(
            data={"sub": user.email, "user_id": user.id, "role": user.rol.value}
        )
        
        return Token(
            access_token=new_access_token,
            refresh_token=refresh_token,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    @staticmethod
    def logout_user(db: Session, refresh_token: str) -> bool:
        """Cerrar sesión de usuario"""
        db_token = db.query(RefreshToken).filter(
            RefreshToken.token == refresh_token,
            RefreshToken.activo == True
        ).first()
        
        if db_token:
            db_token.activo = False
            db.commit()
            return True
        return False

# Dependencias de autenticación
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    """Obtener usuario actual a partir del token"""
    token = credentials.credentials
    
    try:
        payload = JWTUtils.decode_token(token)
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tipo de token inválido"
            )
        
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        
        if email is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
    except HTTPException:
        raise
    
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if user is None or not user.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado o inactivo"
        )
    
    return user

def get_current_active_user(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    """Verificar que el usuario esté activo"""
    if not current_user.activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return current_user

def require_role(allowed_roles: List[TipoRol]):
    """Decorador para requerir roles específicos"""
    def role_checker(current_user: Usuario = Depends(get_current_active_user)):
        if current_user.rol not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para acceder a este recurso"
            )
        return current_user
    return role_checker

# Inicializar FastAPI
app = FastAPI(
    title="MediCitas API con Autenticación",
    description="Especialistas para ti, cuando lo necesitas.",
    version="2.1.0"
)

# --- INICIO: Rutas de Autenticación y Registro ---

@app.post("/auth/registro/paciente", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED, tags=["Autenticación"])
def registrar_paciente(user_data: UsuarioRegistro, db: Session = Depends(get_db)):
    """Registrar un nuevo usuario con el rol de Paciente."""
    try:
        user = AuthService.create_user(db, user_data)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@app.post("/auth/registro/doctor", status_code=status.HTTP_201_CREATED, tags=["Autenticación"])
def registrar_doctor(doctor_data: DoctorRegistro, db: Session = Depends(get_db)):
    """Registrar un nuevo usuario Doctor, incluyendo su perfil y especialidades."""
    try:
        doctor = AuthService.create_doctor(db, doctor_data)
        
        # Construir la respuesta manualmente para asegurar que todo se cargue
        especialidades_resp = [EspecialidadResponse.model_validate(de.especialidad) for de in doctor.perfil_doctor.especialidades]
        
        perfil_resp = PerfilDoctorResponse.model_validate(doctor.perfil_doctor)

        # Crear un diccionario con los datos del doctor excluyendo perfil_doctor
        doctor_dict = {k: v for k, v in doctor.__dict__.items() if k != 'perfil_doctor'}
        
        # Usar el modelo de respuesta DoctorResponse
        return DoctorResponse(
            **doctor_dict,
            perfil_doctor=perfil_resp,
            especialidades=especialidades_resp
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor al registrar doctor: {str(e)}"
        )


@app.post("/auth/login", response_model=Token, tags=["Autenticación"])
def iniciar_sesion(user_credentials: UsuarioLogin, db: Session = Depends(get_db)):
    """Iniciar sesión de usuario"""
    user = AuthService.authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return AuthService.create_tokens(db, user)

@app.post("/auth/refresh", response_model=Token, tags=["Autenticación"])
def refrescar_token(token_data: TokenRefresh, db: Session = Depends(get_db)):
    """Refrescar token de acceso"""
    return AuthService.refresh_access_token(db, token_data.refresh_token)

@app.post("/auth/logout", tags=["Autenticación"])
def cerrar_sesion(token_data: TokenRefresh, db: Session = Depends(get_db)):
    """Cerrar sesión de usuario"""
    success = AuthService.logout_user(db, token_data.refresh_token)
    if success:
        return {"message": "Sesión cerrada exitosamente"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token de refresco inválido"
        )

@app.get("/auth/me", response_model=UsuarioResponse, tags=["Autenticación"])
def obtener_usuario_actual(current_user: Usuario = Depends(get_current_active_user)):
    """Obtener información del usuario actual"""
    return current_user

# --- FIN: Rutas de Autenticación y Registro ---


# Rutas públicas (sin autenticación)
@app.get("/", tags=["General"])
def root():
    return {
        "message": "Bienvenido a MediCitas API",
        "slogan": "Especialistas para ti, cuando lo necesitas.",
        "version": "2.1.0",
        "auth_enabled": True
    }

@app.get("/health", tags=["General"])
def health_check(db: Session = Depends(get_db)):
    """Verificar la conexión a la base de datos"""
    try:
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")


@app.get("/especialidades/", tags=["General"])
def obtener_especialidades_publicas(db: Session = Depends(get_db)):
    """Obtener lista de especialidades (público)"""
    especialidades = db.query(Especialidad).all()
    return especialidades

# Rutas protegidas (requieren autenticación)
@app.get("/usuarios/", response_model=List[UsuarioResponse], tags=["Administración"])
def obtener_usuarios(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role([TipoRol.ADMINISTRADOR]))
):
    """Obtener lista de usuarios (solo administradores)"""
    usuarios = db.query(Usuario).offset(skip).limit(limit).all()
    return usuarios

@app.get("/stats", tags=["Administración"])
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
            "resenas_total": db.query(Resena).count(),
        }
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")

@app.get("/doctores/", tags=["Doctores"])
def obtener_doctores(
    db: Session = Depends(get_db)
):
    """Obtener lista de doctores (pública)"""
    doctores = db.query(PerfilDoctor).all()
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

@app.get("/mis-citas/", response_model=List[CitaResponse], tags=["Citas"])
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
    else: # Administradores pueden ver todas las citas
        citas = db.query(Cita).all()
    
    return citas

@app.post("/citas/", response_model=CitaResponse, status_code=status.HTTP_201_CREATED, tags=["Citas"])
def crear_cita(
    cita_data: CitaCrear,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Crear una nueva cita.
    - Un PACIENTE puede crear una cita para sí mismo.
    """
    if current_user.rol != TipoRol.PACIENTE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los pacientes pueden crear nuevas citas."
        )

    doctor_perfil = db.query(PerfilDoctor).join(Usuario).filter(
        PerfilDoctor.id == cita_data.doctor_id,
        Usuario.activo == True
    ).first()
    if not doctor_perfil:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor no encontrado o inactivo.")

    especialidad = db.query(Especialidad).filter(Especialidad.id == cita_data.especialidad_id).first()
    if not especialidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Especialidad no encontrada.")

    doctor_especialidad = db.query(DoctorEspecialidad).filter(
        DoctorEspecialidad.doctor_id == cita_data.doctor_id,
        DoctorEspecialidad.especialidad_id == cita_data.especialidad_id
    ).first()
    if not doctor_especialidad:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El doctor seleccionado no ofrece la especialidad indicada.")

    cita_existente = db.query(Cita).filter(
        Cita.doctor_id == cita_data.doctor_id,
        Cita.fecha_hora == cita_data.fecha_hora
    ).first()
    if cita_existente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El doctor ya tiene una cita programada en este horario.")

    nueva_cita = Cita(
        paciente_id=current_user.id,
        **cita_data.model_dump(),
        estado=EstadoCita.PROGRAMADA
    )

    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)

    return nueva_cita


# Middleware de manejo de errores
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
