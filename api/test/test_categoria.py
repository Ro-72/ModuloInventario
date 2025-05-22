import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

# -----------------------
# 1. Casos válidos (30)
# -----------------------
@pytest.mark.parametrize("nombre", [
    f"Categoría{i}" for i in range(1, 31)
])
def test_categoria_valida(nombre):
    response = client.post("/categorias/", json={"nombre": nombre})
    assert response.status_code in (200, 201)
    assert "nombre" in response.json()

# -----------------------
# 2. Casos con tildes y símbolos comunes (15)
# -----------------------
@pytest.mark.parametrize("nombre", [
    "Niñez", "Óptica", "Créditos", "Música & Arte", "Cine y TV",
    "Comida - Bebida", "Ropa / Moda", "Libros: Ciencia", "Viajes + Aventura",
    "Salud (General)", "¡Ofertas!", "¿Preguntas?", "Categoría_1", "Categoría-2", "Nombre con Ñ"
])
def test_categoria_simbolos_comunes(nombre):
    response = client.post("/categorias/", json={"nombre": nombre})
    assert response.status_code in (200, 201)

# -----------------------
# 3. Unicode, emojis y multilenguaje (10)
# -----------------------
@pytest.mark.parametrize("nombre", [
    "日本語", "中文分类", "Español", "Русский", "عربي",
    "Français", "Deutsch", "🌟 Estrellas", "🎵 Música", "💻 Tecnología"
])
def test_categoria_unicode(nombre):
    response = client.post("/categorias/", json={"nombre": nombre})
    assert response.status_code in (200, 201)

# -----------------------
# 4. Casos inválidos (20+)
# -----------------------
@pytest.mark.parametrize("nombre", [
    "", "A", "A" * 101, "<script>alert(1)</script>", "'; DROP TABLE categorias; --",
    "123456", "@@@", "\n", "\t", "   ", "🔥" * 51, "A" * 200, "  ", "🚀" * 100,
    ";--", "--", "' or 1=1 --", "' AND '1'='1", "' UNION SELECT *", "%20", "\x00"
])
def test_categoria_invalida(nombre):
    response = client.post("/categorias/", json={"nombre": nombre})
    assert response.status_code in (400, 422)

# -----------------------
# 5. Tipo incorrecto (10)
# -----------------------
@pytest.mark.parametrize("nombre", [None, 123, True, False, [], {}, 0.5, b"bytes", object, lambda x: x])
def test_categoria_tipo_incorrecto(nombre):
    response = client.post("/categorias/", json={"nombre": nombre})
    assert response.status_code == 422

# -----------------------
# 6. Duplicados exactos (5)
# -----------------------
def test_categoria_duplicada():
    nombre = "Duplicada123"
    client.post("/categorias/", json={"nombre": nombre})
    response = client.post("/categorias/", json={"nombre": nombre})
    assert response.status_code == 409

@pytest.mark.parametrize("nombre", [
    "CaseTest", "casetest", "CASETEST", "CasETest", "caseTest"
])
def test_categoria_duplicados_con_variantes(nombre):
    client.post("/categorias/", json={"nombre": nombre.lower()})
    response = client.post("/categorias/", json={"nombre": nombre})
    assert response.status_code in (409, 200)  # depende si el sistema es case-sensitive

# -----------------------
# 7. Espacios (5)
# -----------------------
@pytest.mark.parametrize("nombre", [
    "  inicio", "final  ", "  ambos  ", " medio   espacios ", "   "
])
def test_categoria_con_espacios(nombre):
    response = client.post("/categorias/", json={"nombre": nombre.strip()})
    assert response.status_code in (200, 201, 422)

# -----------------------
# 8. Métodos incorrectos (5)
# -----------------------
@pytest.mark.parametrize("method", ["put", "patch", "delete"])
def test_metodo_no_permitido(method):
    response = getattr(client, method)("/categorias/", json={"nombre": "MétodoNoPermitido"})
    assert response.status_code == 405

# -----------------------
# 9. JSON malformado (2)
# -----------------------
def test_json_malformado():
    response = client.post("/categorias/", data="{nombre: sin comillas}")
    assert response.status_code in (400, 422)

def test_sin_json():
    response = client.post("/categorias/")
    assert response.status_code in (400, 422)

# -----------------------
# 10. Listar categorías (1)
# -----------------------
def test_listar_categorias():
    response = client.get("/categorias/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
