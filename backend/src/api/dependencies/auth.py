"""Module that store authentication dependency, that will grab the authenticated user's details"""
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.database.repositories.user import UserRepository
from core.schemas.user import UserInDB

from api.dependencies.database import get_repository
from core.settings import SECRET_KEY, API_PREFIX
from services import auth_service

# OAuth2PasswordBearer is a class we import from FastAPI that we can instantiate by passing it the path
# that our users will send their email and password to so that they can authenticate.
# This class simply informs FastAPI that the URL provided is the one used to get a token.
# That information is used in OpenAPI and in FastAPI's interactive docs.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_PREFIX}/auth/login")


async def get_user_from_token(
        *,
        token: str = Depends(oauth2_scheme),
        user_repo: UserRepository = Depends(get_repository(UserRepository))) -> Optional[UserInDB]:
    """
    :param token:
    :param user_repo:
    :return: User's details from token
    """
    try:
        username = auth_service.get_username_from_token(token=token, secret_key=str(SECRET_KEY))
        user = await user_repo.get_user_by_username(username=username)
    except Exception as e:
        raise e

    return user


def get_current_authenticated_user(current_user: UserInDB = Depends(get_user_from_token)) -> Optional[UserInDB]:
    """

    :param current_user:
    :return: Authenticated User's details
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authenticated user.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not an active user.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return current_user
