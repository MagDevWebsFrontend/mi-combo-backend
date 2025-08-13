import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, Numeric, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre_usuario = Column(String(50), nullable=False, unique=True)
    # OJO: la columna en la BD se llama "contraseña"
    contraseña = Column(Text, nullable=False)
    rol = Column(String(20), nullable=False)  # 'admin' | 'cliente'
    activo = Column(Boolean, default=True)
    # usar valor por defecto del servidor para evitar problemas de tz
    creado_en = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    combos_creados = relationship("Combo", back_populates="creador")

class Combo(Base):
    __tablename__ = "combos"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100), nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)
    descripcion = Column(Text, nullable=False)
    activo = Column(Boolean, default=True)
    imagen = Column(Text, nullable=True)
    creado_por = Column(PG_UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    creado_en = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    creador = relationship("Usuario", back_populates="combos_creados")
