import enum
from sqlalchemy import Column, BigInteger, Integer, Text, DateTime, Enum, func, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.config import Base

class TipoNotificacion(enum.Enum):
    EMAIL = "Email"
    SMS = "SMS"
    PUSH = "Push"

class EventoNotificacion(enum.Enum):
    CITA_PROGRAMADA = "Cita_Programada"
    CITA_CONFIRMADA = "Cita_Confirmada"
    CITA_CANCELADA = "Cita_Cancelada"
    RECORDATORIO_24H = "Recordatorio_24h"
    RECORDATORIO_1H = "Recordatorio_1h"

class Notificacion(Base):
    __tablename__ = 'notificaciones'

    id = Column(BigInteger, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    cita_id = Column(Integer, ForeignKey('citas.id'), nullable=True)
    tipo = Column(Enum(TipoNotificacion), nullable=False)
    evento = Column(Enum(EventoNotificacion), nullable=False)
    contenido = Column(Text, nullable=False)
    enviada_exitosamente = Column(Boolean, default=False)
    fecha_envio = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    usuario = relationship("Usuario", back_populates="notificaciones")
    cita = relationship("Cita", back_populates="notificaciones")
