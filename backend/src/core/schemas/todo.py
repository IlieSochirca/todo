"""
Module that is responsible for TODOItem Schema Definition using Pydantic.
Grace to Pydantic models, the input data will be validated, serialized (converted), and annotated.
"""
from datetime import datetime

from .core import CoreModel, IDMixinModel

from .comment import CommentInDB

from typing import Optional, List


class TodoBase(CoreModel):
    """Class that contains all shared attributes of a resource"""
    text: Optional[str]
    comments: Optional[List[CommentInDB]]

    class Config:
        """The line 'orm_mode = True' allows the app to take ORM objects and translate them into responses automatically.
        This automation saves us from manually taking data out of ORM, making it into a dictionary,
        then loading it in with Pydantic."""
        orm_mode = True


class TodoCreate(CoreModel):
    """Class that contains attributes required to create a new resource - used at POST requests"""
    text: Optional[str]


class TodoUpdate(TodoBase):
    """Class that contains attributes that can be updated - used at PUT requests"""
    text: Optional[str]


class TodoInDB(IDMixinModel, TodoBase):
    """Class that contains attributes present on any resource coming out of the database"""
    text: Optional[str]
    completed: bool
    comments: Optional[List[CommentInDB]]
    created_on: datetime


class TodoPublic(IDMixinModel, TodoBase):
    """Class that contains attributes present on public facing resources being returned
       from GET, POST, and PUT requests"""
    completed: bool
    created_on: datetime
    comments: Optional[List[CommentInDB]]

