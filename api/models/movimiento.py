from sqlalchemy import Column, Integer, Enum, ForeignKey, String, Text, DateTime
from api.database import Base
from sqlalchemy.sql import func
import enum

class TipoMovimientoEnum(str, enum.Enum):
    entrada = "entrada"
    salida = "salida"

class MovimientoInventario(Base):
    __tablename__ = "movimientos_inventario"

    id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    tipo = Column(Enum(TipoMovimientoEnum), nullable=False)
    cantidad = Column(Integer, nullable=False)
    almacen_id = Column(Integer, ForeignKey("almacenes.id"))
    origen = Column(String(100))
    observaciones = Column(Text)
    fecha = Column(DateTime, server_default=func.now())
