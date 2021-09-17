"""Repository Module where is defined the layer of abstraction on top of database actions regarding 'TODO' Model"""
from typing import List
import datetime

from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from .base import BaseRepository
from core.schemas.todo import TodoCreate, TodoUpdate, TodoInDB

CREATE_QUERY = """
                INSERT INTO todos (text, created_on, completed)
                VALUES (:text, :created_on, :completed)
                RETURNING id, text, created_on, completed
               """

GET_ALL_QUERY = """
                SELECT * FROM todos;
                """

GET_QUERY_BY_ID = """
                   SELECT id, text, created_on, completed
                   FROM todos
                   WHERE id = :id;
                  """


DELETE_QUERY = """
                DELETE FROM todos 
                WHERE id = :id
               """

UPDATE_QUERY = """
                UPDATE todos  
                SET text         = :text,
                    completed    = :completed,
                    created_on   = :created_on
                WHERE id = :id
                RETURNING id, text, created_on, completed
                """


class TodoRepository(BaseRepository):
    """All database actions related to 'TODO' Model"""

    async def create_todo(self, *, new_todo: TodoCreate) -> TodoInDB:
        """Method used to create a new entry in 'TODO' table in DB"""
        query_values = new_todo.dict()
        query_values.update({"created_on": datetime.datetime.now(), "completed": False})
        todo = await self.db.fetch_one(query=CREATE_QUERY, values=query_values)

        return TodoInDB(**todo)
    
    async def update_todo(self, *, id: int, todo_update: TodoUpdate) -> TodoInDB:
        """Method used to update an specified row from DB"""
        todo = await self.get_todo_by_id(id=id)
        
        if not todo:
            return None
       
        todo_update_params = todo.copy(update=todo_update.dict(exclude_unset=True))
        try:
            updated_todo = await self.db.fetch_one(
                                query=UPDATE_QUERY,
                                values=todo_update_params.dict())
            return TodoInDB(**updated_todo)
        except Exception as e:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                                detail="Invalid updated params")

    async def get_all_todos(self) -> List[TodoInDB]:
        """Method that retrieves all 'TODO' entities from DB"""
        todos = await self.db.fetch_all(query=GET_ALL_QUERY)
        return [TodoInDB(**todo) for todo in todos]


    async def get_todo_by_id(self, *, id:int) -> TodoInDB:
        """Method used to retrieve a 'TODO' from DB by ID"""
        todo = await self.db.fetch_one(query=GET_QUERY_BY_ID, values={"id":id})

        if not todo:
            return None
        return TodoInDB(**todo)

    async def delete_todo(self, *, id: int):
        """Method used to delete a 'TODO' entry from DB by ID"""
        return await self.db.execute(query=DELETE_QUERY, values={"id":id})
    
