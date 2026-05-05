import pytest
from unittest.mock import MagicMock, patch

# Bloqueamos Firebase ANTES de que se importe cualquier módulo del proyecto,
# porque firebase.py llama a initialize_app() al momento de importarse.
@pytest.fixture(autouse=True, scope="session")
def bloquear_firebase():
    with patch("firebase_admin.credentials.Certificate"), \
         patch("firebase_admin.initialize_app"), \
         patch("firebase_admin.firestore.client") as mock_client:
        yield mock_client


@pytest.fixture
def mock_db(bloquear_firebase):
    """Retorna el mock de db que usan las rutas."""
    mock = MagicMock()
    with patch("routes.db", mock):
        yield mock


@pytest.fixture
def client(mock_db):
    """Cliente de pruebas Flask con Firebase mockeado."""
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# Token exactamente igual al del .env
TOKEN = "1234"


def auth():
    return {"Authorization": TOKEN}


# ---------------------------------------------------------------
# Helpers para simular documentos de Firestore
# ---------------------------------------------------------------

def make_doc(id, name, user_id, songs=None):
    """Simula un documento de Firestore."""
    doc = MagicMock()
    doc.id = id
    doc.exists = True
    doc.get = lambda field: {
        "name": name,
        "user_id": user_id,
        "songs": songs or []
    }.get(field)
    return doc


def make_doc_not_found():
    doc = MagicMock()
    doc.exists = False
    return doc


# ---------------------------------------------------------------
# TEST 1 — Crear playlist exitosamente
# ---------------------------------------------------------------

def test_crear_playlist_exitosa(client, mock_db):
    response = client.post("/api/playlists", json={
        "name": "Rock Classics",
        "user_id": "user_42",
        "songs": []
    }, headers=auth())

    assert response.status_code == 201
    data = response.get_json()
    assert data["mensaje"] == "Playlist creada"


# ---------------------------------------------------------------
# TEST 2 — Listar todas las playlists
# ---------------------------------------------------------------

def test_listar_playlists(client, mock_db):
    doc1 = make_doc("pl_1", "Rock Classics", "user_42", [])
    doc2 = make_doc("pl_2", "Pop Hits", "user_99", [])

    mock_db.collection.return_value.stream.return_value = [doc1, doc2]

    response = client.get("/api/playlists", headers=auth())

    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]["name"] == "Rock Classics"
    assert data[1]["name"] == "Pop Hits"


# ---------------------------------------------------------------
# TEST 3 — Obtener playlist por ID (existe y no existe)
# ---------------------------------------------------------------

def test_obtener_playlist_existente(client, mock_db):
    doc = make_doc("pl_1", "Rock Classics", "user_42", [])
    mock_db.collection.return_value.document.return_value.get.return_value = doc

    response = client.get("/api/playlists/pl_1", headers=auth())

    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == "pl_1"
    assert data["name"] == "Rock Classics"


def test_obtener_playlist_inexistente_retorna_404(client, mock_db):
    mock_db.collection.return_value.document.return_value.get.return_value = make_doc_not_found()

    response = client.get("/api/playlists/no_existe", headers=auth())

    assert response.status_code == 404
    assert "error" in response.get_json()


# ---------------------------------------------------------------
# TEST 4 — Agregar canción a playlist
# ---------------------------------------------------------------

def test_agregar_cancion_a_playlist(client, mock_db):
    doc = make_doc("pl_1", "Rock Classics", "user_42", songs=[])
    doc_ref = MagicMock()
    doc_ref.get.return_value = doc
    mock_db.collection.return_value.document.return_value = doc_ref

    response = client.put("/api/playlists/pl_1/songs", json={
        "title": "Bohemian Rhapsody",
        "artist": "Queen"
    }, headers=auth())

    assert response.status_code == 200
    data = response.get_json()
    assert data["mensaje"] == "Canción agregada"
    assert len(data["songs"]) == 1
    assert data["songs"][0]["title"] == "Bohemian Rhapsody"


def test_agregar_cancion_playlist_inexistente_retorna_404(client, mock_db):
    doc_ref = MagicMock()
    doc_ref.get.return_value = make_doc_not_found()
    mock_db.collection.return_value.document.return_value = doc_ref

    response = client.put("/api/playlists/no_existe/songs", json={
        "title": "Bohemian Rhapsody",
        "artist": "Queen"
    }, headers=auth())

    assert response.status_code == 404


# ---------------------------------------------------------------
# TEST 5 — Eliminar canción por índice
# ---------------------------------------------------------------

def test_eliminar_cancion_por_indice_valido(client, mock_db):
    songs = [
        {"title": "Bohemian Rhapsody", "artist": "Queen"},
        {"title": "Stairway to Heaven", "artist": "Led Zeppelin"}
    ]
    doc = make_doc("pl_1", "Rock Classics", "user_42", songs=songs)
    doc_ref = MagicMock()
    doc_ref.get.return_value = doc
    mock_db.collection.return_value.document.return_value = doc_ref

    response = client.delete("/api/playlists/pl_1/songs/0", headers=auth())

    assert response.status_code == 200
    data = response.get_json()
    assert data["mensaje"] == "Canción eliminada"
    assert len(data["songs"]) == 1
    assert data["songs"][0]["title"] == "Stairway to Heaven"


def test_eliminar_cancion_con_indice_invalido_retorna_400(client, mock_db):
    songs = [{"title": "Bohemian Rhapsody", "artist": "Queen"}]
    doc = make_doc("pl_1", "Rock Classics", "user_42", songs=songs)
    doc_ref = MagicMock()
    doc_ref.get.return_value = doc
    mock_db.collection.return_value.document.return_value = doc_ref

    response = client.delete("/api/playlists/pl_1/songs/5", headers=auth())

    assert response.status_code == 400
    assert "error" in response.get_json()