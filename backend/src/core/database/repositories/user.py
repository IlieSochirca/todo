"""Module that contains User Repository functionality"""
from typing import Optional
from pydantic import EmailStr
from databases import Database
from fastapi import HTTPException, status
from core.schemas.user import UserCreate, UserInDB
from services import auth_service
from .base import BaseRepository

REGISTER_NEW_USER_QUERY = """
                          INSERT INTO users (username, password, email, salt)
                          VALUES (:username, :password, :email, :salt)
                          RETURNING id, username, email, email_verified, password, salt, is_active, is_superuser
                          """

GET_USER_BY_EMAIL_QUERY = """
                          SELECT id, username, email, email_verified, password, salt, is_active, is_superuser
                          FROM users
                          WHERE email = :email;
                          """

GET_USER_BY_USERNAME_QUERY = """
                             SELECT id, username, email, email_verified, password, salt, is_active, is_superuser
                             FROM users
                             WHERE username = :username;
                             """


class UserRepository(BaseRepository):
    """User Repository Class Definition"""

    def __init__(self, database: Database) -> None:
        """Init file"""
        super().__init__(database)
        self.auth_service = auth_service

    async def get_user_by_email(self, *, email: EmailStr) -> UserInDB:
        """Method that executes a call to DB and returns an User record from DB by email"""
        user_record = await self.db.fetch_one(query=GET_USER_BY_EMAIL_QUERY, values={"email": email})
        if not user_record:
            return None
        return UserInDB(**user_record)

    async def get_user_by_username(self, *, username: str) -> UserInDB:
        """Method that executes a call to DB and returns an User record from DB by username"""
        user_record = await self.db.fetch_one(query=GET_USER_BY_USERNAME_QUERY, values={"username": username})
        if not user_record:
            return None
        return UserInDB(**user_record)

    async def register_new_user(self, *, new_user: UserCreate) -> UserInDB:
        """Method that executes a call to DB and
        creates a new entry in 'User' table"""
        # check email is not already taken
        if await self.get_user_by_email(email=new_user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="That email is already taken. Login with that email or register with another one.")
        # check username is not already taken
        if await self.get_user_by_username(username=new_user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="That username is already taken. Login with that username or register with another one.")

        user_password = self.auth_service.create_salt_and_hashed_password(plaintext_password=new_user.password)
        new_user_params = new_user.copy(update=user_password.dict())

        created_user = await self.db.fetch_one(query=REGISTER_NEW_USER_QUERY, values={**new_user_params.dict()})
        return UserInDB(**created_user)

    async def authenticate_user(self, *, email: EmailStr, password: str) -> Optional[UserInDB]:
        """Method that executes a call to DB and search for a user in DB
           and checks if sent password is the same as in DB"""
        user = await self.get_user_by_email(email=email)
        if not user:
            return None
        if not self.auth_service.verify_password(password=password, salt=user.salt, hashed_password=user.password):
            return None
        return user
