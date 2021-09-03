"""Module to specify all available routes for 'TODO' entity """
from fastapi import APIRouter, Body, Depends
from starlette.status import HTTP_201_CREATED

from core.schemas.todo import TodoPublic, TodoCreate

from core.database.repositories.todo import TodoRepository

from api.dependencies.database import get_repository

todo_router = APIRouter()


@todo_router.post("/create-todo", response_model=TodoPublic, status_code=HTTP_201_CREATED)
async def create_todos(new_todo: TodoCreate = Body(...),
                       todo_repo: TodoRepository = Depends(get_repository(TodoRepository))) -> TodoPublic:
    """
    Method to be called when a new 'TODO' entity needs to created

    :param new_todo: to validate incoming data from the client, by specifying it's Python type(TodoCreate)
    :param todo_repo: is our database interface, and the route's only dependency => result of "get_repository()"
    :return: TodoPublic instance
    """
    created_todo = await todo_repo.create_todo(new_todo=new_todo)
    return created_todo
