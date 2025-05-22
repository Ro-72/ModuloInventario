from pydantic import BaseModel, Field

class AlmacenCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, pattern=r"^[\w\s\-áéíóúÁÉÍÓÚñÑ]+$")
    ubicacion: str = Field(..., min_length=3, max_length=200)

class AlmacenOut(AlmacenCreate):
    id: int

    class Config:
        from_attributes = True
