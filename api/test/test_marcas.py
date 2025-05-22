import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

# 1. Casos válidos (30)
@pytest.mark.parametrize("nombre", [f"Marca{i}" for i in range(1, 31)])
def test_marca_valida(nombre):
    response = client.post("/marcas/", json={"nombre": nombre})
    assert response.status_code in (200, 201)
    assert "nombre" in response.json()

# 2. Nombres con símbolos comunes (15)
@pytest.mark.parametrize("nombre", [
    "Sony", "LG", "HP Inc.", "Samsung Electronics", "Café del Valle",
    "Tech & Go", "Ropa-Marca", "Audio/Video", "Libro:Tech", "¡Sorpresa!",
    "¿Dudas?", "ÑTech", "Marca_2024", "Marca-Plus", "Compañía S.A."
])
def test_marca_con_simbolos(nombre):
    response = client.post("/marcas/", json={"nombre": nombre})
    assert response.status_code in (200, 201)

# 3. Nombres unicode, emojis, lenguas extranjeras (10)
@pytest.mark.parametrize("nombre", [
    "📱 Tecnología", "Música 🎵", "日本企業", "中文品牌", "Марка",
    "Marca Árabe عربي", "Marca🌍", "Marque Française", "DeutschMark", "Marca🌟VIP"
])
def test_marca_unicode(nombre):
    response = client.post("/marcas/", json={"nombre": nombre})
    assert response.status_code in (200, 201)

# 4. Casos inválidos (20)
@pytest.mark.parametrize("nombre", [
    "", "A", "A" * 101, "<script>", "'; DROP TABLE marcas;", "@@@", "\n", "\t",
    "   ", "\x00", "🔥" * 51, "SELECT * FROM marcas", "' or 1=1 --",
    "'; --", "--", "1' OR '1'='1", "null", "%00", "   ", ";--"
])
def test_marca_invalida(nombre):
    response = client.post("/marcas/", json={"nombre": nombre})
    assert response.status_code in (400, 422)

# 5. Tipos incorrectos (10)
@pytest.mark.parametrize("nombre", [None, 123, True, False, {}, [], 0.5, b"bytes", object, lambda x: x])
def test_marca_tipo_incorrecto(nombre):
    response = client.post("/marcas/", json={"nombre": nombre})
    assert response.status_code == 422

# 6. Duplicados (5)
def test_marca_duplicada():
    nombre = "MarcaDuplicada"
    client.post("/marcas/", json={"nombre": nombre})
    response = client.post("/marcas/", json={"nombre": nombre})
    assert response.status_code == 409

@pytest.mark.parametrize("nombre", [
    "MarcaTest", "marcatest", "MARCATest", "marcaTest", "MARCATest"
])
def test_marca_duplicados_variantes(nombre):
    client.post("/marcas/", json={"nombre": nombre.lower()})
    response = client.post("/marcas/", json={"nombre": nombre})
    assert response.status_code in (409, 200)

# 7. Espacios (5)
@pytest.mark.parametrize("nombre", [
    "  inicio", "final  ", "  ambos  ", "marca   con   espacios", "   "
])
def test_marca_con_espacios(nombre):
    response = client.post("/marcas/", json={"nombre": nombre.strip()})
    assert response.status_code in (200, 201, 422)

# 8. Métodos incorrectos (5)
@pytest.mark.parametrize("method", ["put", "patch", "delete"])
def test_marca_metodo_no_permitido(method):
    response = getattr(client, method)("/marcas/", json={"nombre": "Prohibido"})
    assert response.status_code == 405

# 9. JSON malformado (2)
def test_marca_json_malformado():
    response = client.post("/marcas/", data="{nombre: sin comillas}")
    assert response.status_code in (400, 422)

def test_marca_sin_json():
    response = client.post("/marcas/")
    assert response.status_code in (400, 422)

# 10. Listar marcas (1)
def test_listar_marcas():
    response = client.get("/marcas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
