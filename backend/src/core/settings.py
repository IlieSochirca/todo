"""App configurations module"""
import os
from urllib.parse import quote_plus

PROJECT_NAME = "todo-ilso"
VERSION = "1.0.0"
API_PREFIX = "/api"

# DATABASE CONFIGURATION

host_server = os.getenv("POSTGRES_HOST", "localhost")
database_port = os.getenv("POSTGRES_PORT", 5432)
database_name = os.getenv("POSTGRES_NAME", "dutch_postgres")
database_username = quote_plus(str(os.getenv("POSTGRES_USER", "postgres")))
database_password = quote_plus(str(os.getenv("POSTGRES_PASSWORD", "secret")))
ssl_mode = quote_plus(str(os.getenv("SSL_MODE", "prefer")))

DATABASE_URL = f"postgresql://{database_username}:{database_password}@" \
               f"{host_server}:{database_port}/{database_name}?sslmode={ssl_mode}"

# JWT AUTH CONFIGURATION
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", default=7 * 24 * 60)  # one week
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", default="HS256")
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", default="phresh:auth")
JWT_TOKEN_PREFIX = os.getenv("JWT_TOKEN_PREFIX", default="Bearer")
