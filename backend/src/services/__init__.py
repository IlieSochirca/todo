"""Init file for Services Package"""
from .authentication import AuthService

# initialize "AuthService" class once and use it in all application

auth_service = AuthService()
