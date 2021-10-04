"""Entrypoint module to store all application routes"""

from fastapi import APIRouter

from .routes.check import check_router
from .routes.todos import todos_router
from .routes.comments import comments_router
from .routes.users import users_router

api_router = APIRouter()
api_router.include_router(check_router, tags=["login"])
api_router.include_router(todos_router, tags=["todo_crud"])
api_router.include_router(comments_router, tags=["comment_crud"])
api_router.include_router(users_router, tags=["user_crud"])
