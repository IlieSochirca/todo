"""Module that will keep all database related dependencies"""
from typing import Callable, Type
from databases import Database
from starlette.requests import Request
from fastapi import Depends

from core.database.repositories.base import BaseRepository


def get_database(request: Request) -> Database:
    """

    :param request:
    :return: a reference to our DB connection that is established in "on_startup_handler" function
    """
    return request.app.state._db


def get_repository(repo_type: Type[BaseRepository]) -> Callable:
    """

    :param repo_type:
    :return:
    """

    def get_repo(db: Database = Depends(get_database)) -> Type[BaseRepository]:
        """

        :param db: method dependency, depends on 'get_database' method declared above
        :return:
        """
        return repo_type(db)

    return get_repo
