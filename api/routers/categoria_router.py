from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models.categoria import Categoria
from api.schemas.categoria import CategoriaCreate, CategoriaOut

router = APIRouter(prefix="/categorias", tags=["Categorías"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CategoriaOut)
def crear_categoria(data: CategoriaCreate, db: Session = Depends(get_db)):
    existente = db.query(Categoria).filter(Categoria.nombre == data.nombre).first()
    if existente:
        raise HTTPException(status_code=409, detail="La categoría ya existe.")

    nueva = Categoria(**data.model_dump())
    try:
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Conflicto con categoría existente")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error interno al crear categoría")

@router.get("/", response_model=list[CategoriaOut])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()
