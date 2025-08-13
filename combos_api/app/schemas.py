from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, condecimal

# --------------------------
# Usuario
# --------------------------

class UsuarioBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)  # para usar alias en POST
    nombre_usuario: str
    rol: str = Field(..., pattern="^(admin|cliente)$")
    activo: Optional[bool] = True

class UsuarioCreate(UsuarioBase):
    # Permitimos enviar "contrasena" (sin ñ) en el JSON,
    # pero el campo interno sigue llamándose "contraseña".
    contraseña: str = Field(alias="contrasena")

class Usuario(UsuarioBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    creado_en: datetime

# --------------------------
# Combo
# --------------------------

class ComboBase(BaseModel):
    # condecimal asegura precisión y evita 422 raros
    precio: condecimal(max_digits=10, decimal_places=2, ge=0) # type: ignore
    nombre: str
    descripcion: str
    activo: Optional[bool] = True
    imagen: Optional[str] = None

class ComboCreate(ComboBase):
    creado_por: UUID

class Combo(ComboBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    creado_por: UUID
    creado_en: datetime
