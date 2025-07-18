from sqlalchemy import Column, Integer, Text, DateTime, func, ForeignKey, SmallInteger, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from app.config import Base

class Resena(Base):
    __tablename__ = 'resenas'

    id = Column(Integer, primary_key=True, index=True)
    cita_id = Column(Integer, ForeignKey('citas.id', ondelete="CASCADE"), nullable=False, unique=True)
    paciente_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('perfiles_doctores.id'), nullable=False)
    calificacion = Column(SmallInteger, nullable=False)
    comentario = Column(Text, nullable=True)
    es_anonima = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    cita = relationship("Cita", back_populates="resena")
    paciente = relationship("Usuario", foreign_keys=[paciente_id], back_populates="resenas_paciente")
    doctor = relationship("PerfilDoctor", back_populates="resenas_doctor")

    __table_args__ = (CheckConstraint('calificacion >= 1 AND calificacion <= 5', name='check_calificacion_range'),)
