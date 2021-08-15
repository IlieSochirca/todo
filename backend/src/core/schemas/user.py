"""
Module that is responsible for User Schema Definition using Pydantic.
Grace to Pydantic models, the input data will be validated, serialized (converted), and annotated
"""
from pydantic import BaseModel


class UserSchema(BaseModel):
    """User Schema declaration"""
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        """The line 'orm_mode = True' allows the app to take ORM objects and translate them into responses automatically.
        This automation saves us from manually taking data out of ORM, making it into a dictionary,
        then loading it in with Pydantic."""
        orm_mode = True
