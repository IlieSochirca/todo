"""
Module that is responsible for TODO Schema Definition using Pydantic.
Grace to Pydantic models, the input data will be validated, serialized (converted), and annotated
"""
from datetime import datetime

from pydantic import BaseModel


class TODOSchema(BaseModel):
    """Class that is responsible for data validation"""
    id: int
    text: str
    completed: bool
    created_on: datetime

    class Config:
        """The line 'orm_mode = True' allows the app to take ORM objects and translate them into responses automatically.
        This automation saves us from manually taking data out of ORM, making it into a dictionary,
        then loading it in with Pydantic."""
        orm_mode = True
