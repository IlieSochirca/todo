"""App configurations module"""
import os
from urllib.parse import quote_plus

host_server = os.getenv("POSTGRES_HOST", "localhost")
database_port = os.getenv("POSTGRES_PORT", 5432)
database_name = os.getenv("POSTGRES_NAME", "dutch_postgres")
database_username = quote_plus(str(os.getenv("POSTGRES_USER", "postgres")))
database_password = quote_plus(str(os.getenv("POSTGRES_PASSWORD", "secret")))
ssl_mode = quote_plus(str(os.getenv("SSL_MODE", "prefer")))

DATABASE_URL = f"postgresql://{database_username}:{database_password}@" \
               f"{host_server}:{database_port}/{database_name}?sslmode={ssl_mode}"
