from pydantic import BaseModel, Field
from typing import Optional

class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150, pattern=r"^[\w\s\-áéíóúÁÉÍÓÚñÑ]+$")
    categoria_id: Optional[int] = Field(None, ge=1)
    marca_id: Optional[int] = Field(None, ge=1)
    precio: float = Field(..., gt=0)
    stock_actual: int = Field(..., ge=0)
    stock_minimo: int = Field(..., ge=0)
    activo: bool = True

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(ProductoBase):
    pass

class ProductoOut(ProductoBase):
    id: int

    class Config:
        from_attributes = True