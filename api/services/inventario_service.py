from sqlalchemy.orm import Session
from api.schemas.inventario import MovimientoInventarioIn
from api.models.movimiento import MovimientoInventario
from api.repositories import inventario_repository

def procesar_movimiento(db: Session, data: MovimientoInventarioIn):
    movimiento = MovimientoInventario(**data.model_dump())
    return inventario_repository.registrar_movimiento(db, movimiento)
