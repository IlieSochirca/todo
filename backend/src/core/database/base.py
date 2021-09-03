"""Base Class declaration"""
import sqlalchemy
from databases import Database
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from core.settings import DATABASE_URL


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
database = Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()
