from sqlalchemy.orm import Session
from api.schemas.producto import ProductoCreate, ProductoUpdate
from api.models.producto import Producto
from api.repositories import producto_repository

def crear_producto(db: Session, data: ProductoCreate):
    producto = Producto(**data.model_dump())
    return producto_repository.crear_producto(db, producto)

def actualizar_producto(db: Session, producto_id: int, data: ProductoUpdate):
    return producto_repository.actualizar_producto(db, producto_id, data)

def obtener_productos(db: Session):
    return producto_repository.obtener_todos(db)

def eliminar_producto(db: Session, producto_id: int):
    
    return producto_repository.eliminar_producto(db, producto_id)
