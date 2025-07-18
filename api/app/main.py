from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Date, SmallInteger, BigInteger, ForeignKey, Enum as SQLEnum, CheckConstraint, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.sql import func
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, date
import os
from dotenv import load_dotenv
import enum

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

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

# Modelos SQLAlchemy
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
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    perfil_doctor = relationship("PerfilDoctor", back_populates="usuario", uselist=False)
    citas_como_paciente = relationship("Cita", foreign_keys="Cita.paciente_id", back_populates="paciente")
    resenas = relationship("Resena", back_populates="paciente")
    notificaciones = relationship("Notificacion", back_populates="usuario")

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
    especialidades = relationship("DoctorEspecialidad", back_populates="doctor")
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

# Modelos Pydantic
class UsuarioBase(BaseModel):
    nombre_completo: str
    email: EmailStr
    telefono: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    rol: TipoRol

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    activo: Optional[bool] = None

class UsuarioResponse(UsuarioBase):
    id: int
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    class Config:
        from_attributes = True

class EspecialidadBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class EspecialidadCreate(EspecialidadBase):
    pass

class EspecialidadResponse(EspecialidadBase):
    id: int
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True

class CitaBase(BaseModel):
    paciente_id: int
    doctor_id: int
    especialidad_id: int
    fecha_hora: datetime
    duracion_minutos: int = 30
    motivo_consulta: Optional[str] = None

class CitaCreate(CitaBase):
    pass

class CitaUpdate(BaseModel):
    fecha_hora: Optional[datetime] = None
    duracion_minutos: Optional[int] = None
    estado: Optional[EstadoCita] = None
    motivo_consulta: Optional[str] = None
    notas_doctor: Optional[str] = None

class CitaResponse(CitaBase):
    id: int
    estado: EstadoCita
    notas_doctor: Optional[str] = None
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    class Config:
        from_attributes = True

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Inicializar FastAPI
app = FastAPI(
    title="MediCitas API",
    description="Especialistas para ti, cuando lo necesitas.",
    version="1.0.0"
)

# Importar las semillas
try:
    from .seeds import crear_semillas_completas
except ImportError:
    # Si no se puede importar, usar semillas básicas
    def crear_semillas_completas(db: Session):
        if db.query(Especialidad).first():
            return
        
        # Crear especialidades básicas
        especialidades = [
            Especialidad(nombre="Cardiología", descripcion="Especialidad médica que se ocupa del diagnóstico y tratamiento de las enfermedades del corazón"),
            Especialidad(nombre="Dermatología", descripcion="Especialidad médica que se ocupa del diagnóstico y tratamiento de las enfermedades de la piel"),
            Especialidad(nombre="Neurología", descripcion="Especialidad médica que se ocupa del diagnóstico y tratamiento de las enfermedades del sistema nervioso"),
            Especialidad(nombre="Pediatría", descripcion="Especialidad médica que se ocupa de la salud de los niños"),
        ]
        
        for especialidad in especialidades:
            db.add(especialidad)
        db.commit()

# Rutas de la API
@app.get("/")
def root():
    return {
        "message": "Bienvenido a MediCitas API",
        "slogan": "Especialistas para ti, cuando lo necesitas.",
        "version": "1.0.0"
    }

@app.post("/init-db")
def inicializar_base_datos(db: Session = Depends(get_db)):
    """Inicializar la base de datos con datos de prueba completos"""
    try:
        crear_semillas_completas(db)
        return {"message": "Base de datos inicializada con datos de prueba completos"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al inicializar la base de datos: {str(e)}")

@app.get("/stats")
def obtener_estadisticas(db: Session = Depends(get_db)):
    """Obtener estadísticas generales del sistema"""
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
        }
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")

@app.get("/usuarios/", response_model=List[UsuarioResponse])
def obtener_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de usuarios"""
    usuarios = db.query(Usuario).offset(skip).limit(limit).all()
    return usuarios

@app.get("/especialidades/", response_model=List[EspecialidadResponse])
def obtener_especialidades(db: Session = Depends(get_db)):
    """Obtener lista de especialidades"""
    especialidades = db.query(Especialidad).all()
    return especialidades

@app.get("/doctores/")
def obtener_doctores(db: Session = Depends(get_db)):
    """Obtener lista de doctores con sus especialidades"""
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

@app.post("/citas/", response_model=CitaResponse)
def crear_cita(cita: CitaCreate, db: Session = Depends(get_db)):
    """Crear una nueva cita"""
    # Verificar que el doctor existe
    doctor = db.query(PerfilDoctor).filter(PerfilDoctor.id == cita.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    
    # Verificar que el paciente existe
    paciente = db.query(Usuario).filter(Usuario.id == cita.paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Verificar que la especialidad existe
    especialidad = db.query(Especialidad).filter(Especialidad.id == cita.especialidad_id).first()
    if not especialidad:
        raise HTTPException(status_code=404, detail="Especialidad no encontrada")
    
    # Crear la cita
    db_cita = Cita(**cita.dict())
    db.add(db_cita)
    db.commit()
    db.refresh(db_cita)
    
    return db_cita

@app.get("/citas/", response_model=List[CitaResponse])
def obtener_citas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de citas"""
    citas = db.query(Cita).offset(skip).limit(limit).all()
    return citas

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Verificar la conexión a la base de datos"""
    try:
        # Hacer una consulta simple para verificar la conexión
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)