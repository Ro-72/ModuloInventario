from pydantic import BaseModel, Field

class CategoriaCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, pattern=r"^[\w\s\-áéíóúÁÉÍÓÚñÑ]+$")

class CategoriaOut(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True
