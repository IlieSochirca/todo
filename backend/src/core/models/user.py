"""User Model Definition"""
from sqlalchemy import Column, Integer, String

from src.core.database.base import Base


class User(Base):
    """User Model Declaration"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
