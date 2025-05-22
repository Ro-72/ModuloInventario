from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models.almacen import Almacen
from api.schemas.almacen import AlmacenCreate, AlmacenOut

router = APIRouter(prefix="/almacenes", tags=["Almacenes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AlmacenOut)
def crear_almacen(data: AlmacenCreate, db: Session = Depends(get_db)):
    try:
        almacen = Almacen(**data.model_dump())
        db.add(almacen)
        db.commit()
        db.refresh(almacen)
        return almacen
    except Exception:
        raise HTTPException(status_code=500, detail="Error al crear almacén")

@router.get("/{almacen_id}", response_model=AlmacenOut)
def obtener_almacen(almacen_id: int, db: Session = Depends(get_db)):
    almacen = db.query(Almacen).filter(Almacen.id == almacen_id).first()
    if not almacen:
        raise HTTPException(status_code=404, detail="Almacén no encontrado")
    return almacen

@router.get("/", response_model=list[AlmacenOut])
def listar_marcas(db: Session = Depends(get_db)):
    return db.query(Almacen).all()
