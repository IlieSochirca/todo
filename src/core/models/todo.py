""" Model Definition File"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from src.core.database.base import Base


class TODO(Base):
    """ TO DO model definition"""
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    owner_id = Column(Integer, foreign_key='users.id')
    completed = Column(Boolean, default=False)
    created_on = Column(DateTime)
