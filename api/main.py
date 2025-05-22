from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.database import Base, engine
from api.models import producto, categoria, marca, usuario, movimiento, almacen

# Routers
from api.routers import (
    producto_router,
    inventario_router,
    auth_router,
    categoria_router,
    marca_router,
    almacen_router,
    movimiento_router
)

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

# App FastAPI
app = FastAPI(title="API Inventario")

# Incluir todos los routers
app.include_router(auth_router.router)
app.include_router(producto_router.router)
app.include_router(inventario_router.router)
app.include_router(categoria_router.router)
app.include_router(marca_router.router)
app.include_router(almacen_router.router)
app.include_router(movimiento_router.router)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta de prueba
@app.get("/api/test")
def test_endpoint():
    return {"message": "Hello from FastAPI!"}
