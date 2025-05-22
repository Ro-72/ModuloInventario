
import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from api.main import app

client = TestClient(app)

# ---------- PRODUCTOS ----------
def test_crear_producto_valido():
    response = client.post("/productos/", json={
        "nombre": "Producto Test",
        "precio": 100.0,
        "stock_actual": 10,
        "stock_minimo": 2,
        "activo": True
    })
    assert response.status_code == 200
    assert response.json()["nombre"] == "Producto Test"

def test_crear_producto_invalido():
    response = client.post("/productos/", json={
        "nombre": "Producto Incompleto",
        "stock_actual": 10,
        "stock_minimo": 2,
        "activo": True
    })
    assert response.status_code == 422

def test_actualizar_producto_existente():
    response = client.put("/productos/1", json={
        "nombre": "Producto Actualizado",
        "precio": 120.0,
        "stock_actual": 12,
        "stock_minimo": 3,
        "activo": True
    })
    assert response.status_code == 200
    assert response.json()["nombre"] == "Producto Actualizado"

def test_actualizar_producto_inexistente():
    response = client.put("/productos/9999", json={
        "nombre": "Producto Fantasma",
        "precio": 120.0,
        "stock_actual": 12,
        "stock_minimo": 3,
        "activo": True
    })
    assert response.status_code == 404

def test_listar_productos():
    response = client.get("/productos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ---------- CATEGORÍAS ----------
def test_crear_categoria_valida():
    import random
    nombre_unico = f"Categoría Test {random.randint(1000, 9999)}"
    response = client.post("/categorias/", json={"nombre": nombre_unico})
    assert response.status_code == 200

def test_crear_categoria_duplicada():
    response = client.post("/categorias/", json={"nombre": "Electrodomésticos"})
    assert response.status_code in [400, 409]

def test_listar_categorias():
    response = client.get("/categorias/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ---------- MARCAS ----------
def test_crear_marca_valida():
    import random
    nombre_unico = f"Marca Test {random.randint(1000, 9999)}"
    response = client.post("/marcas/", json={"nombre": nombre_unico})
    assert response.status_code == 200

def test_listar_marcas():
    response = client.get("/marcas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ---------- ALMACENES ----------
def test_crear_almacen_valido():
    response = client.post("/almacenes/", json={
        "nombre": "Almacén Central",
        "ubicacion": "Av. Siempre Viva 123"
    })
    assert response.status_code == 200
    assert response.json()["nombre"] == "Almacén Central"

def test_listar_almacenes():
    response = client.get("/almacenes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ---------- MOVIMIENTOS ----------
def test_crear_movimiento_valido():
    response = client.post("/movimientos/", json={
        "producto_id": 1,
        "tipo": "entrada",
        "cantidad": 5,
        "almacen_id": 1,
        "origen": "compra",
        "observaciones": "test entrada"
    })
    assert response.status_code == 200

def test_listar_movimientos():
    response = client.get("/movimientos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ---------- USUARIOS / LOGIN ----------
def test_login_usuario_correcto():
    response = client.post("/auth/login", json={
        "email": "carlos@empresa.com",
        "password": "admin123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "carlos@empresa.com"
    assert data["nombre"] == "Carlos Pérez"
    assert data["rol"] == "Administrador"

def test_login_usuario_incorrecto():
    response = client.post("/auth/login", json={
        "email": "incorrecto@empresa.com",
        "password": "admin123"
    })
    assert response.status_code == 401

def test_login_contrasena_incorrecta():
    response = client.post("/auth/login", json={
        "email": "carlos@empresa.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401
# ---------- PRODUCTOS: Crear con precio negativo ----------
def test_crear_producto_precio_negativo():
    response = client.post("/productos/", json={
        "nombre": "Producto Inválido",
        "precio": -50.0,
        "stock_actual": 10,
        "stock_minimo": 2,
        "activo": True
    })
    assert response.status_code == 422  # FastAPI detecta error por validación Pydantic


# ---------- CATEGORÍAS: Crear con nombre vacío ----------
def test_crear_categoria_nombre_vacio():
    response = client.post("/categorias/", json={"nombre": ""})
    assert response.status_code == 422  # Error de validación por campo requerido


# ---------- MARCAS: Listar cuando no hay ninguna ----------
def test_listar_marcas_sin_datos():
    # Asume que la base está vacía o se limpió para el test
    response = client.get("/marcas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ---------- MOVIMIENTOS: Crear con cantidad = 0 ----------
def test_crear_movimiento_cantidad_cero():
    response = client.post("/movimientos/", json={
        "producto_id": 1,
        "tipo": "entrada",
        "cantidad": 0,
        "almacen_id": 1,
        "origen": "error de prueba",
        "observaciones": "cantidad inválida"
    })
    assert response.status_code in [400, 422]


# ---------- LOGIN: Contraseña incorrecta ----------
def test_login_contraseña_incorrecta():
    response = client.post("/auth/login", json={
        "email": "carlos@empresa.com",
        "password": "contraseñamal"
    })
    assert response.status_code == 401

def test_eliminar_producto_existente():
    response = client.delete("/productos/1")
    assert response.status_code in [200, 409]

def test_eliminar_producto_inexistente():
    response = client.delete("/productos/9999")
    assert response.status_code == 404

def test_listar_productos_sin_datos():
    response = client.get("/productos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_obtener_categoria_por_id():
    response = client.get("/categorias/1")
    if response.status_code == 200:
    
        assert "nombre" in response.json()
    else:
        assert response.status_code == 404

def test_crear_marca_nombre_vacio():
    response = client.post("/marcas/", json={"nombre": ""})
    assert response.status_code == 422

def test_crear_marca_nombre_vacio():
    response = client.post("/marcas/", json={"nombre": ""})
    assert response.status_code == 422

def test_crear_almacen_sin_ubicacion():
    response = client.post("/almacenes/", json={"nombre": "Sin Ubicación"})
    assert response.status_code == 422

def test_crear_movimiento_tipo_invalido():
    response = client.post("/movimientos/", json={
        "producto_id": 1,
        "tipo": "traslado",  
        "cantidad": 5,
        "almacen_id": 1,
        "origen": "error",
        "observaciones": "tipo no válido"
    })
    assert response.status_code in [400, 422]

def test_crear_movimiento_producto_inexistente():
    response = client.post("/movimientos/", json={
        "producto_id": 9999,
        "tipo": "entrada",
        "cantidad": 1,
        "almacen_id": 1,
        "origen": "desconocido",
        "observaciones": "producto no existe"
    })
    assert response.status_code in [400, 422, 404]

def test_login_email_formato_invalido():
    response = client.post("/auth/login", json={
        "email": "notanemail",
        "password": "admin123"
    })
    assert response.status_code == 422
