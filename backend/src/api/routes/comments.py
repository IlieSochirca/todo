"""Module to specify all available routes for 'Comment' resource"""
from fastapi import APIRouter, Body, Depends
from core.schemas.comment import CommentPublic, CommentCreate
from core.database.repositories.comment import CommentRepository
from starlette.status import HTTP_201_CREATED
from api.dependencies.database import get_repository

comments_router = APIRouter()


@comments_router.post("/comments", response_model=CommentPublic, status_code=HTTP_201_CREATED)
async def create_comment(new_comment: CommentCreate = Body(...),
                         comment_repo: CommentRepository = Depends(get_repository(CommentRepository))) -> CommentPublic:
    """
    Method to be called when a new 'Comment' entity needs to be created
    :param new_comment:
    :param comment_repo:
    """
    created_comment = await comment_repo.create_comment(new_comment=new_comment)
    return created_comment
