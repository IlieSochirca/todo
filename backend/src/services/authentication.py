"""Module that keeps all authentication service logic"""
import jwt
import bcrypt
from typing import Optional
from datetime import datetime, timedelta
from passlib.context import CryptContext
from core.schemas.user import UserPasswordUpdate, UserInDB
from core.schemas.token import JWTMeta, JWTCreds, JWTPayload
from core.settings import SECRET_KEY, JWT_ALGORITHM, JWT_AUDIENCE, JWT_TOKEN_PREFIX, ACCESS_TOKEN_EXPIRE_MINUTES
from pydantic import ValidationError
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthException(BaseException):
    """Custom Authentication Exception"""
    pass


class AuthService:
    """Class that will keep all Authentication Services logic"""

    @staticmethod
    def generate_salt():
        """:returns random generated salt"""
        return bcrypt.gensalt().decode()

    @staticmethod
    def hash_password(*, password: str, salt: str) -> str:
        """
        :returns new hashed password
        :param password:
        :param salt:
        """
        return pwd_context.hash(password + salt)

    def create_salt_and_hashed_password(self, *, plaintext_password: str) -> UserPasswordUpdate:
        """
        Returns hashed password that will be stored in DB from plaintext password
        :param plaintext_password:
        """
        salt = self.generate_salt()
        hashed_password = self.hash_password(password=plaintext_password, salt=salt)

        return UserPasswordUpdate(salt=salt, password=hashed_password)

    def verify_password(self, *, password: str, salt: str, hashed_password: str) -> bool:
        """
        :returns True or False depending on if password is the same of the hashed one or not
        """
        return pwd_context.verify(password + salt, hashed_password)

    def create_access_token(self, *,
                            user: UserInDB,
                            secret_key: str = SECRET_KEY,
                            audience: str = JWT_AUDIENCE,
                            expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
        """

        :param user:
        :param secret_key:
        :param audience:
        :param expires_in:
        :return: A new access token
        """
        if not user or not isinstance(user, UserInDB):
            return None

        jwt_meta = JWTMeta(
            aud=audience,
            iat=datetime.timestamp(datetime.utcnow()),
            exp=datetime.timestamp(datetime.utcnow() + timedelta(minutes=expires_in)),
        )

        jwt_credentials = JWTCreds(sub=user.email, username=user.username)

        token_payload = JWTPayload(**jwt_meta.dict(), **jwt_credentials.dict())

        access_token = jwt.encode(token_payload.dict(), secret_key, algorithm=JWT_ALGORITHM)

        return access_token

    def get_username_from_token(self, *, token: str, secret_key: str) -> Optional[str]:
        """
        Decodes token payload and returns user's username
        :return: User that is found out from access token
        """

        try:
            decoded_token = jwt.decode(token, str(secret_key), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM])
            payload = JWTPayload(**decoded_token)
        except (jwt.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate token credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload.username
