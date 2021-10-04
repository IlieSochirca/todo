"""Module that stores all User Resource related routes"""
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from fastapi.security import OAuth2PasswordRequestForm

from core.schemas.user import UserPublic, UserCreate, UserInDB
from core.schemas.token import AccessToken
from core.database.repositories.user import UserRepository

from api.dependencies.database import get_repository
from api.dependencies.auth import get_current_authenticated_user
from services import auth_service

users_router = APIRouter(prefix="/auth")


@users_router.get("/me", response_model=UserPublic)
async def get_authenticated_user(current_user: UserInDB = Depends(get_current_authenticated_user)) -> UserPublic:
    """
    Endpoint called to check if the authenticated user is authorized or not
    :return:
    """
    return current_user


@users_router.post("/users", response_model=UserPublic, status_code=HTTP_201_CREATED)
async def register_new_user(
        new_user: UserCreate = Body(..., embed=True),
        user_repo: UserRepository = Depends(get_repository(UserRepository))) -> UserPublic:
    """
    Endpoint called to create new 'User' object in DB
    :returns User data + access token
    """
    created_user = await user_repo.register_new_user(new_user=new_user)

    access_token = AccessToken(access_token=auth_service.create_access_token(user=created_user), token_type="bearer")

    return UserPublic(**created_user.dict(), access_token=access_token)


@users_router.post("/login", response_model=AccessToken)
async def login_user(
        user_repo: UserRepository = Depends(get_repository(UserRepository)),
        form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)) -> AccessToken:
    """
    Endpoint called to login the user with username and password
    OAuth2 is using "form data" for sending the username and password.
    'username' acts as 'email'
    :returns access token
    """

    user = await user_repo.authenticate_user(email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                            detail="Authentication was unsuccessful.",
                            headers={"WWW-Authenticate": "Bearer"})

    access_token = AccessToken(access_token=auth_service.create_access_token(user=user), token_type="bearer")
    return access_token
