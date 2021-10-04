"""Repository Module where is defined the layer of abstraction on top of database actions regarding 'TODO' Model"""

from typing import List
import json
import datetime

from fastapi import HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST

from .base import BaseRepository

from core.schemas.todo import TodoCreate, TodoUpdate, TodoInDB
from core.schemas.comment import CommentInDB, CommentBase

CREATE_QUERY = """
                INSERT INTO todos (text, created_on, completed)
                VALUES (:text, :created_on, :completed)
                RETURNING id, text, created_on, completed
               """

GET_ALL_QUERY = """
                 SELECT todos.*,  array_agg(comments) as comments
                 FROM todos
                 LEFT JOIN comments ON comments.todo_id=todos.id
                 GROUP by todos.id
                """

GET_QUERY_BY_ID = """
                  SELECT todos.*,  array_agg(comments) as comments
                  FROM todos
                  LEFT JOIN comments ON comments.todo_id=todos.id
                  WHERE todos.id = :id
                  GROUP by todos.id
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

GET_QUERY_BY_TODO_ID = """
                        SELECT * FROM comments
                        WHERE comments.todo_id = :todo_id
                       """


class TodoRepository(BaseRepository):
    """All database actions related to 'TODO' Model"""

    async def create_todo(self, *, new_todo: TodoCreate) -> TodoInDB:
        """Method that executes a call to DB and
        creates a new entry in 'TODO' table"""
        query_values = new_todo.dict()
        query_values.update({"created_on": datetime.datetime.now(), "completed": False})
        todo = await self.db.fetch_one(query=CREATE_QUERY, values=query_values)

        return TodoInDB(**todo)

    async def update_todo(self, *, id: int, todo_update: TodoUpdate) -> TodoInDB:
        """Method that executes a call to DB and updates a specified row from DB"""
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
                                detail=e)

    async def get_all_todos(self) -> List[TodoInDB]:
        """Method that retrieves all 'TODO' entities from DB"""
        todos = [dict(todo) for todo in await self.db.fetch_all(query=GET_ALL_QUERY)]
        result = []
        for todo in todos:
            comments = todo.pop("comments")
            print([CommentInDB(**comment) for comment in comments])
            todo["comments"] = [CommentInDB(**comment).dict() for comment in comments]
            result.append(todo)
        try:
            return [TodoInDB(**todo) for todo in todos]
        except Exception as e:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                                detail=json.loads(e.json()))

    async def get_todo_by_id(self, *, id: int) -> TodoInDB:
        """Method used to retrieve a 'TODO' from DB by ID"""
        todo = dict(await self.db.fetch_one(query=GET_QUERY_BY_ID, values={"id": id}))
        comments = todo.pop("comments")
        todo["comments"] = [CommentInDB(**comment).dict() for comment in comments]
        print(todo)
        if not todo:
            return None
        try:
            return TodoInDB(**todo)
        except Exception as e:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                                detail=json.loads(e.json()))

    async def delete_todo(self, *, id: int):
        """Method used to delete a 'TODO' entry from DB by ID"""
        return await self.db.execute(query=DELETE_QUERY, values={"id": id})
