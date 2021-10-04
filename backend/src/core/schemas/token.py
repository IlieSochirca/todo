"""Module that will store JWT token Definition Schema"""
from datetime import datetime, timedelta
from pydantic import EmailStr
from core.settings import JWT_AUDIENCE, ACCESS_TOKEN_EXPIRE_MINUTES
from .core import CoreModel


class JWTMeta(CoreModel):
    """Meta Class Definition for JWT with following fields:
    iss - the issuer of the token (that's us)
    aud - who this token is intended for
    iat - when this token was issued at
    exp - when this token expires and is no longer valid proof that the requesting user is logged in.
    """
    iss: str = "phresh.io"
    aud: str = JWT_AUDIENCE
    iat: float = datetime.timestamp(datetime.utcnow())
    exp: float = datetime.timestamp(datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))


class JWTCreds(CoreModel):
    """How we'll identify users"""
    sub: EmailStr
    username: str


class JWTPayload(JWTMeta, JWTCreds):
    """
    JWT Payload right before it's encoded - combine meta and username
    """
    pass


class AccessToken(CoreModel):
    """Access Token Model"""
    access_token: str
    token_type: str
