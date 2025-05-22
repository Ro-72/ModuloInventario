from sqlalchemy.orm import Session
from api.models.movimiento import MovimientoInventario
from api.models.producto import Producto

def registrar_movimiento(db: Session, movimiento: MovimientoInventario):
    db.add(movimiento)

    producto = db.query(Producto).filter(Producto.id == movimiento.producto_id).first()
    if not producto:
        return None

    if movimiento.tipo == "entrada":
        producto.stock_actual += movimiento.cantidad
    elif movimiento.tipo == "salida":
        producto.stock_actual -= movimiento.cantidad
        if producto.stock_actual < 0:
            raise ValueError("Stock insuficiente para realizar la salida.")

    db.commit()
    db.refresh(movimiento)
    return movimiento
def obtener_todos(db: Session):
    return db.query(MovimientoInventario).all()