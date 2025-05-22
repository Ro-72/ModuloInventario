from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.schemas.inventario import MovimientoInventarioIn
from api.schemas.movimiento import MovimientoOut  # Schema correcto de salida
from api.services import inventario_service
from api.repositories import inventario_repository

router = APIRouter(prefix="/inventario", tags=["Inventario"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/entrada")
def registrar_entrada(data: MovimientoInventarioIn, db: Session = Depends(get_db)):
    if data.tipo != "entrada":
        raise HTTPException(status_code=400, detail="Este endpoint es solo para entradas")
    try:
        return inventario_service.procesar_movimiento(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error al registrar entrada")

@router.post("/salida")
def registrar_salida(data: MovimientoInventarioIn, db: Session = Depends(get_db)):
    if data.tipo != "salida":
        raise HTTPException(status_code=400, detail="Este endpoint es solo para salidas")
    try:
        return inventario_service.procesar_movimiento(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error al registrar salida")

@router.get("/movimientos", response_model=list[MovimientoOut])
def listar_movimientos(db: Session = Depends(get_db)):
    return inventario_repository.obtener_todos(db)
