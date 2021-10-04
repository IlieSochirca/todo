"""
Module that is responsible for User Schema Definition using Pydantic.
Grace to Pydantic models, the input data will be validated, serialized (converted), and annotated
"""
import string
from pydantic import EmailStr, constr, validator
from typing import Optional

from .core import CoreModel, IDMixinModel
from .token import AccessToken


def validate_username(username: str) -> str:
    """Method that is checking username validity"""
    allowed = string.ascii_letters + string.digits + "-" + "_"
    assert all(char in allowed for char in username), "Invalid characters in username."
    assert len(username) >= 3, "Username must be 3 characters or more."
    return username


class UserBase(CoreModel):
    """User Schema declaration"""
    username: str
    email: Optional[EmailStr]
    email_verified: bool = False
    is_active: bool = False
    is_superuser: bool = False

    class Config:
        """The line 'orm_mode = True' allows the app to take ORM objects and translate them into responses automatically.
        This automation saves us from manually taking data out of ORM, making it into a dictionary,
        then loading it in with Pydantic."""
        orm_mode = True


class UserCreate(CoreModel):
    """Pydantic Model used at User Creation"""
    email: EmailStr
    password: constr(min_length=7, max_length=100)
    username: str

    @validator("username", pre=True)
    def username_is_valid(cls, username: str) -> str:
        """Method used to validate user's username"""
        return validate_username(username)


class UserUpdate(CoreModel):
    """Pydantic Model used at updating User object fields"""
    email: Optional[EmailStr]
    username: str

    @validator("username", pre=True)
    def username_is_valid(cls, username: str) -> str:
        """Method used to validate user's username"""
        return validate_username(username)


class UserPasswordUpdate(CoreModel):
    """
    Pydantic Model used at updating User object password
    """
    password: constr(min_length=7, max_length=100)
    salt: str


class UserInDB(IDMixinModel, UserBase):
    """Pydantic Model used for DB interactions that adds id, password and salt to object fields"""
    password: constr(min_length=7, max_length=100)
    salt: str


class UserPublic(IDMixinModel, UserBase):
    """Pydantic Model used for public User objects representations"""
    access_token: Optional[AccessToken]
