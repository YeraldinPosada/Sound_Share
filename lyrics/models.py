from db import db

class Lyric(db.Model):
    __tablename__ = 'lyrics'

    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "song_id": self.song_id,
            "content": self.content,
            "created_at": self.created_at
        }