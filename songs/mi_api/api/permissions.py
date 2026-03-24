from rest_framework.permissions import BasePermission

from dotenv import load_dotenv
import os

load_dotenv()

TOKEN_SECRETO = os.getenv("TOKEN_SECRETO")

class ValidarTokenPersonalizado(BasePermission):
    def has_permission(self, request, view):
        token = request.headers.get('Authorization')
        return token == f"Token {TOKEN_SECRETO}"