"""Repository Module where is defined the layer of abstraction on top of database actions regarding 'Comment' Model"""
import datetime
from .base import BaseRepository
from core.schemas.comment import CommentCreate, CommentInDB

CREATE_QUERY = """
                INSERT INTO comments (text, todo_id, created_on)
                VALUES (:text, :todo_id, :created_on)
                RETURNING id, text, todo_id, created_on
               """

GET_QUERY_BY_TODO_ID = """
                        SELECT comments.id, comments.text, comments.created_on FROM comments
                        WHERE comments.todo_id = :todo_id
                       """


class CommentRepository(BaseRepository):
    """All database actions related to 'Comment' Model
    Note: Any parameter that appears after the * should be called
    as a keyword argument, and doesn't require a default value."""

    async def create_comment(self, *, new_comment: CommentCreate) -> CommentInDB:
        """Method that executes a call to DB and
        creates a new entry in 'Comment' table"""
        query_values = new_comment.dict()
        query_values.update({"created_on": datetime.datetime.now()})
        comment = await self.db.fetch_one(query=CREATE_QUERY, values=query_values)
        return CommentInDB(**comment)

    async def get_comments_by_todo_id(self, *, todo_id: int) -> CommentInDB:
        """Method used to retrieve a 'Comment' from DB by  TODO ID"""
        comments = await self.db.fetch(query=GET_QUERY_BY_TODO_ID, values={"id": todo_id})
        return [CommentInDB(**comment) for comment in comments]
