from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class TipoMovimiento(str, Enum):
    entrada = 'entrada'
    salida = 'salida'

class MovimientoInventarioIn(BaseModel):
    producto_id: int = Field(..., ge=1)
    tipo: TipoMovimiento
    cantidad: int = Field(..., gt=0)
    almacen_id: Optional[int] = Field(None, ge=1)
    origen: Optional[str] = Field(None, max_length=150)
    observaciones: Optional[str] = Field(None, max_length=255)
