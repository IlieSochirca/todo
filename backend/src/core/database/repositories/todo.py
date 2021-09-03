"""Repository Module where is defined the layer of abstraction on top of database actions regarding 'TODO' Model"""
import datetime
from .base import BaseRepository
from core.schemas.todo import TodoCreate, TodoInDB

CREATE_QUERY = """
                INSERT INTO todos (text, created_on, completed)
                VALUES (:text, :created_on, :completed)
                RETURNING id, text, created_on, completed
               """


class TodoRepository(BaseRepository):
    """All database actions related to 'TODO' Model"""

    async def create_todo(self, *, new_todo: TodoCreate) -> TodoInDB:
        """Methods used to create a new entry in 'TODO' table in DB"""
        query_values = new_todo.dict()
        query_values.update({"created_on": datetime.datetime.now(), "completed": False})
        todo = await self.db.fetch_one(query=CREATE_QUERY, values=query_values)

        return TodoInDB(**todo)
