"""Database configuration module"""
import logging
from fastapi import FastAPI
from typing import Callable

from .base import database

logger = logging.getLogger(__name__)


async def connect_to_db(app: FastAPI) -> None:
    """
    Callback that will create a connection pool to the database on app start up
    """
    try:
        await database.connect()
        app.state.db = database
        logger.warning("--- DB CONNECTION CREATED ---")
    except Exception as e:
        logger.warning("--- DB CONNECTION ERROR ---")
        logger.warning(e)
        logger.warning("--- DB CONNECTION ERROR ---")


async def close_db_connection(app: FastAPI) -> None:
    """
    Callback that will close the connection pool to the database on app shutdown
    """
    try:
        await app.state._db.disconnect()
    except Exception as e:
        logger.warning("--- DB DISCONNECT ERROR ---")
        logger.warning(e)
        logger.warning("--- DB DISCONNECT ERROR ---")


def create_start_app_handler(app: FastAPI) -> Callable:
    """Returns an async function that's responsible for creating our database connection"""

    async def start_app() -> None:
        await connect_to_db(app)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    """Returns an async function that's responsible for shutting our database connection"""
    async def stop_app() -> None:
        await close_db_connection(app)
    return stop_app
