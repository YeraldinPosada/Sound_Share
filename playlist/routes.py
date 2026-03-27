from flask import jsonify, request
from firebase import db
from functools import wraps

from dotenv import load_dotenv
import os

load_dotenv()

def require_token(f):
    @wraps(f)
    def decorate(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token != os.getenv("TOKEN"):
            return jsonify({"error": "Usuario no autorizado"}), 401
        return f(*args, **kwargs)
    return decorate
    


def register_routes(app):

    @app.route("/api/playlists", methods=['POST'])
    @require_token
    def create_playlist():
        data = request.get_json()

        playlist = {
            "name": data["name"],
            "user_id": data["user_id"],
            "songs": data.get("songs", [])
        }

        db.collection("playlists").add(playlist)

        return jsonify({"mensaje": "Playlist creada"}), 201


    @app.route("/api/playlists", methods=['GET'])
    @require_token
    def get_playlists():
        playlists = db.collection("playlists").stream()

        return jsonify([
            {
                "id": p.id,
                "name": p.get("name"),
                "user_id": p.get("user_id"),
                "songs": p.get("songs")
            }
            for p in playlists
        ])


    @app.route("/api/playlists/<id>", methods=['GET'])
    @require_token
    def get_playlist(id):
        doc = db.collection("playlists").document(id).get()

        if not doc.exists:
            return jsonify({"error": "Playlist no encontrada"}), 404

        return jsonify({
            "id": doc.id,
            "name": doc.get("name"),
            "user_id": doc.get("user_id"),
            "songs": doc.get("songs")
        })


    @app.route("/api/playlists/<id>", methods=['PUT'])
    @require_token
    def update_playlist(id):
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se enviaron datos"}), 400
        db.collection("playlists").document(id).update({
            "name": data["name"],
            "user_id": data["user_id"],
            "songs": data["songs"]
        })

        return jsonify({"mensaje": "Playlist actualizada"})


    @app.route("/api/playlists/<id>", methods=['DELETE'])
    @require_token
    def delete_playlist(id):
        db.collection("playlists").document(id).delete()

        return jsonify({"mensaje": "Playlist eliminada"})


    @app.route("/api/playlists/<id>/songs", methods=['PUT'])
    @require_token
    def add_song(id):
        data = request.get_json()

        doc_ref = db.collection("playlists").document(id)
        playlist = doc_ref.get()

        if not playlist.exists:
            return jsonify({"error": "Playlist no encontrada"}), 404

        songs = playlist.get("songs") or []

        nueva_cancion = {
            "title": data["title"],
            "artist": data["artist"]
        }

        songs.append(nueva_cancion)

        doc_ref.update({"songs": songs})

        return jsonify({"mensaje": "Canción agregada", "songs": songs})


    # Eliminar canción por índice
    @app.route("/api/playlists/<id>/songs/<int:index>", methods=['DELETE'])
    @require_token
    def delete_song(id, index):
        doc_ref = db.collection("playlists").document(id)
        playlist = doc_ref.get()

        if not playlist.exists:
            return jsonify({"error": "Playlist no encontrada"}), 404

        songs = playlist.get("songs") or []

        if index < 0 or index >= len(songs):
            return jsonify({"error": "Índice inválido"}), 400

        songs.pop(index)

        doc_ref.update({"songs": songs})

        return jsonify({"mensaje": "Canción eliminada", "songs": songs})