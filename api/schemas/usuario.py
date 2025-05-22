from pydantic import BaseModel, EmailStr, Field

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=64)

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    rol: str
    email: str

    class Config:
        from_attributes = True
