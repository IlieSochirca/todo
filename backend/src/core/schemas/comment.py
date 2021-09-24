"""Module that will contain schema definition for Comment object"""

from datatime import datetime
from .core import CoreModel, IDMixinModel

from typing import Optional


class CommentBase(CoreModel):
    """Class that contains all shared attributes of Comment resource"""
    text: Optional[str]
    todo_id: int

    class Config:
        """The line 'orm_mode = True' allows the app to take ORM objects and translate them into responses automatically.
        This automation saves us from manually taking data out of ORM, making it into a dictionary,
        then loading it in with Pydantic."""
        orm_mode = True


class CommentCreate(CoreModel):
    """Class that contains attributes required to create a new resource - used at POST requests"""
    text: Optional[str]


class CommentUpdate(CommentBase):
    """Class that contains attributes that can be updated - used at PUT requests"""
    text: Optional[str]


class CommentInDB(IDMixinModel, CommentBase):
    """Class that contains attributes present on any resource coming out of the database"""
    created_on: datetime


class CommentPublic(IDMixinModel, CommentBase):
    """Class that contains attributes present on public facing resources being returned
       from GET, POST, and PUT requests"""
    created_on: datetime

