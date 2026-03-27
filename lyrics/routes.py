from flask import jsonify, request
from db import db
from models import Lyric
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

    @app.route("/api/lyrics", methods=['POST'])
    @require_token
    def create_lyric():
        data = request.get_json()

        new_lyric = Lyric(
            song_id=data["song_id"],
            content=data["content"]
        )

        db.session.add(new_lyric)
        db.session.commit()

        return jsonify({"mensaje": "Lyric creada"}), 201


    @app.route("/api/lyrics", methods=['GET'])
    @require_token
    def get_lyrics():
        lyrics = Lyric.query.all()

        return jsonify([l.to_dict() for l in lyrics])


    #Obtener por ID
    @app.route("/api/lyrics/<int:id>", methods=['GET'])
    @require_token
    def get_lyric(id):
        lyric = Lyric.query.get(id)

        if not lyric:
            return jsonify({"error": "Lyric no encontrada"}), 404

        return jsonify(lyric.to_dict())


    @app.route("/api/lyrics/<int:id>", methods=['PUT'])
    @require_token
    def update_lyric(id):
        data = request.get_json()
        lyric = Lyric.query.get(id)

        if not lyric:
            return jsonify({"error": "Lyric no encontrada"}), 404

        lyric.content = data["content"]
        db.session.commit()

        return jsonify({"mensaje": "Lyric actualizada"})


    @app.route("/api/lyrics/<int:id>", methods=['DELETE'])
    @require_token
    def delete_lyric(id):
        lyric = Lyric.query.get(id)

        if not lyric:
            return jsonify({"error": "Lyric no encontrada"}), 404

        db.session.delete(lyric)
        db.session.commit()

        return jsonify({"mensaje": "Lyric eliminada"})