"""Module that will store routes for health checking the application"""
from fastapi import APIRouter

check_router = APIRouter()


@check_router.get("/health")
def health_check():
    """Method that is checking if server is running and return Telegram User Info"""
    return {"Message": "Active!", "status": 200}
