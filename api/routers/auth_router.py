from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.schemas.usuario import UsuarioLogin
from api.services.usuario_service import verificar_usuario

router = APIRouter(prefix="/auth", tags=["Autenticación"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    user = verificar_usuario(db, usuario.email, usuario.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return user
