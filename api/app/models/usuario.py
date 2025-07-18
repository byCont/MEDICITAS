import enum
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime, Enum, func
from sqlalchemy.orm import relationship
from app.config import Base

class TipoRol(enum.Enum):
    PACIENTE = "Paciente"
    DOCTOR = "Doctor"
    ADMINISTRADOR = "Administrador"

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(150), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    telefono = Column(String(20), nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    rol = Column(Enum(TipoRol), nullable=False)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relaciones
    perfil_doctor = relationship("PerfilDoctor", back_populates="usuario", uselist=False, cascade="all, delete-orphan")
    citas_paciente = relationship("Cita", foreign_keys='[Cita.paciente_id]', back_populates="paciente")
    resenas_paciente = relationship("Resena", foreign_keys='[Resena.paciente_id]', back_populates="paciente")
    notificaciones = relationship("Notificacion", back_populates="usuario")
