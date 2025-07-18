import enum
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.config import Base

class EstadoCita(enum.Enum):
    PROGRAMADA = "Programada"
    CONFIRMADA = "Confirmada"
    COMPLETADA = "Completada"
    CANCELADA = "Cancelada"
    NO_ASISTIO = "No Asistió"

class Cita(Base):
    __tablename__ = 'citas'

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey('usuarios.id', ondelete="SET NULL"), nullable=False)
    doctor_id = Column(Integer, ForeignKey('perfiles_doctores.id', ondelete="CASCADE"), nullable=False)
    especialidad_id = Column(Integer, ForeignKey('especialidades.id', ondelete="RESTRICT"), nullable=False)
    fecha_hora = Column(DateTime(timezone=True), nullable=False)
    duracion_minutos = Column(Integer, default=30, nullable=False)
    estado = Column(Enum(EstadoCita), default=EstadoCita.PROGRAMADA, nullable=False)
    motivo_consulta = Column(Text, nullable=True)
    notas_doctor = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relaciones
    paciente = relationship("Usuario", foreign_keys=[paciente_id], back_populates="citas_paciente")
    doctor = relationship("PerfilDoctor", back_populates="citas_doctor")
    especialidad = relationship("Especialidad", back_populates="citas")
    resena = relationship("Resena", back_populates="cita", uselist=False, cascade="all, delete-orphan")
    notificaciones = relationship("Notificacion", back_populates="cita")

    __table_args__ = (UniqueConstraint('doctor_id', 'fecha_hora', name='uq_doctor_fecha_hora'),)
