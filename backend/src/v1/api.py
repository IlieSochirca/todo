"""Entrypoint mo"""

from fastapi import APIRouter

from .routes.check import check_router

api_router = APIRouter()
api_router.include_router(check_router, tags=["login"])
