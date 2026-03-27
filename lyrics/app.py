from flask import Flask
from config import Config
from db import db
from flask_migrate import Migrate
from routes import register_routes

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)


from models import Lyric

register_routes(app)

if __name__ == '__main__':
    app.run(debug=True, port=5002)