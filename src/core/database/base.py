"""Base Class declaration"""
import sqlalchemy
from databases import Database
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from src.core.settings import DATABASE_URL


@as_declarative()
class Base:
    """
    Base Class Definition. Used for Models creation
    """
    id: int
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()


# initialize DB
database = Database(DATABASE_URL, echo=True)
# Specifying echo=True upon the engine initialization will enable us to see generated SQL queries in the console.

metadata = sqlalchemy.MetaData()
