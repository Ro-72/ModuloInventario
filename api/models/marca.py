from sqlalchemy import Column, Integer, String
from api.database import Base

class Marca(Base):
    __tablename__ = "marcas"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True, nullable=False)
