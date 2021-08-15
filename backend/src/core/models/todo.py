""" Model Definition File"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from src.core.database.base import Base


class TODOItem(Base):
    """ TO DO model definition"""
    __tablename__ = "todoitems"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    owner_id = Column(Integer, foreign_key='users.id')
    completed = Column(Boolean, default=False)
    created_on = Column(DateTime)
