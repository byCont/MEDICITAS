# app/models.py
# modelos SQLAlchemy

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, Date, 
    SmallInteger, BigInteger, ForeignKey, Enum as SQLEnum, 
    CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

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
    email_verificado = Column(Boolean, default=False)
    ultimo_acceso = Column(DateTime(timezone=True))
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    perfil_doctor = relationship("PerfilDoctor", back_populates="usuario", uselist=False)
    citas_como_paciente = relationship("Cita", foreign_keys="Cita.paciente_id", back_populates="paciente")
    resenas = relationship("Resena", back_populates="paciente")
    notificaciones = relationship("Notificacion", back_populates="usuario")
    tokens_refresh = relationship("RefreshToken", back_populates="usuario")

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