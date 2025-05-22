from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from api.database import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)
    marca_id = Column(Integer, ForeignKey("marcas.id"), nullable=True)
    precio = Column(Float, nullable=False)
    stock_actual = Column(Integer, default=0)
    stock_minimo = Column(Integer, default=0)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
