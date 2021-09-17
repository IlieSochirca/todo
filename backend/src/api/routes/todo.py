"""Module to specify all available routes for 'TODO' entity """
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT

from core.schemas.todo import TodoPublic, TodoCreate, TodoUpdate

from core.database.repositories.todo import TodoRepository

from api.dependencies.database import get_repository

todo_router = APIRouter()


@todo_router.post("/todos", response_model=TodoPublic, status_code=HTTP_201_CREATED)
async def create_todo(new_todo: TodoCreate = Body(...),
                       todo_repo: TodoRepository = Depends(get_repository(TodoRepository))) -> TodoPublic:
    """
    Method to be called when a new 'TODO' entity needs to created

    :param new_todo: to validate incoming data from the client, by specifying it's Python type(TodoCreate)
    :param todo_repo: is our database interface, and the route's only dependency => result of "get_repository()"
    :return: TodoPublic instance
    """
    created_todo = await todo_repo.create_todo(new_todo=new_todo)
    return created_todo


@todo_router.put("/todos/{id}", response_model=TodoPublic)
async def update_todo(id: int = Path(..., ge=1, title="The ID of the TODO to update"),
                      todo_update: TodoUpdate = Body(..., embed=True), 
                      todo_repo: TodoRepository = Depends(get_repository(TodoRepository))) -> TodoPublic:
    """
    Method to be called when a 'TODO' entity needs to be updated
    """

    print(id, todo_update)
    updated_todo = await todo_repo.update_todo(id=id, todo_update=todo_update)
    print(updated_todo)

    if not updated_todo:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No TODO found with this ID")

    return updated_todo

@todo_router.get("/todos", response_model=List[TodoPublic])
async def get_all_todos(todo_repo: TodoRepository = Depends(get_repository(TodoRepository))) -> List[TodoPublic]:
    """Method to be called to return all 'TODO' entities from DB"""
    return await todo_repo.get_all_todos()


@todo_router.get("/todos/{id}", response_model=TodoPublic)
async def get_todo(id: int, todo_repo: TodoRepository = Depends(get_repository(TodoRepository))) -> TodoPublic:
    """Method to be called to get the details of a 'TODO' entity from DB"""

    todo = await todo_repo.get_todo_by_id(id=id)
    if not todo:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No TODO found with this ID")
    return todo

@todo_router.delete("/todos/{id}", status_code=HTTP_204_NO_CONTENT)
async def remove_todo(id:int, todo_repo: TodoRepository = Depends(get_repository(TodoRepository))):
    """Method to be called to delete a 'TODO' entity from DB"""
    
    todo = await todo_repo.get_todo_by_id(id=id)
    if not todo:
         raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No TODO found with this id")
    
    await todo_repo.delete_todo(id=id)
