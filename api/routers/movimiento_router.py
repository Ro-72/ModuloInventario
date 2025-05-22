from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.schemas.movimiento import MovimientoCreate
from api.services import inventario_service

router = APIRouter(prefix="/movimientos", tags=["Movimientos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def registrar_movimiento(data: MovimientoCreate, db: Session = Depends(get_db)):
    try:
        return inventario_service.procesar_movimiento(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
