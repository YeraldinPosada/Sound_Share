import firebase_admin
from firebase_admin import credentials, firestore
from config import Config

credencial= credentials.Certificate(Config.FIREBASECREDENTIAL)
firebase_admin.initialize_app(credencial)

db= firestore.client()