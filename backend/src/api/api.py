"""Entrypoint module to store all application routes"""

from fastapi import APIRouter

from .routes.check import check_router
from .routes.todo import todo_router
from .routes.comment import comment_router

api_router = APIRouter()
api_router.include_router(check_router, tags=["login"])
api_router.include_router(todo_router, tags=["todo_crud"])
api_router.include_router(comment_router, tags=["comment_crud"])

