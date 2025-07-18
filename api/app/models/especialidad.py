from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.config import Base

class Especialidad(Base):
    __tablename__ = 'especialidades'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    doctores = relationship("PerfilDoctor", secondary="doctor_especialidades", back_populates="especialidades")
    citas = relationship("Cita", back_populates="especialidad")
