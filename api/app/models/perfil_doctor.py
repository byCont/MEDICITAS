from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.config import Base

# Tabla de asociación para la relación muchos-a-muchos entre doctores y especialidades
doctor_especialidades = Table('doctor_especialidades',
    Base.metadata,
    Column('doctor_id', Integer, ForeignKey('perfiles_doctores.id', ondelete="CASCADE"), primary_key=True),
    Column('especialidad_id', Integer, ForeignKey('especialidades.id', ondelete="CASCADE"), primary_key=True)
)

class PerfilDoctor(Base):
    __tablename__ = 'perfiles_doctores'

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id', ondelete="CASCADE"), nullable=False, unique=True)
    cedula_profesional = Column(String(50), unique=True, nullable=False)
    biografia = Column(Text, nullable=True)
    foto_perfil_url = Column(String(255), nullable=True)
    fecha_actualizacion = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relaciones
    usuario = relationship("Usuario", back_populates="perfil_doctor")
    especialidades = relationship("Especialidad", secondary=doctor_especialidades, back_populates="doctores")
    citas_doctor = relationship("Cita", back_populates="doctor")
    resenas_doctor = relationship("Resena", back_populates="doctor")
