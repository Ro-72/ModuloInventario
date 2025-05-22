from sqlalchemy.orm import Session
from api.models.producto import Producto
from api.schemas.producto import ProductoUpdate

def obtener_todos(db: Session):
    return db.query(Producto).all()

def obtener_por_id(db: Session, producto_id: int):
    return db.query(Producto).filter(Producto.id == producto_id).first()

def crear_producto(db: Session, producto: Producto):
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto

def actualizar_producto(db: Session, producto_id: int, data: ProductoUpdate):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(producto, key, value)
    db.commit()
    db.refresh(producto)
    return producto

def eliminar_producto(db: Session, producto_id: int):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        return None
    db.delete(producto)
    db.commit()
    return producto
