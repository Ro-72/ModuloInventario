from sqlalchemy.orm import Session
from api.models.usuario import Usuario
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_usuario(db: Session, email: str, password: str):
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if user and pwd_context.verify(password, user.password):
        return user
    return None

def encriptar_password(password: str) -> str:
    return pwd_context.hash(password)
