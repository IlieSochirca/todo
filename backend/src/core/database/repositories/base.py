"""
The purpose of a repository is to serve as a layer of abstraction on top of database actions.
Each repository encapsulates database functionality corresponding to a particular resource.
In doing so, we decouple persistence logic from our application logic.
The Repository Pattern, introduced in Domain Driven Design back in 2004, has a number of popular implementations.
For Phresh, we'll stick to a slightly customized approach and treat repositories as a stand-in for a more traditional ORM.
"""
from databases import Database


class BaseRepository:
    """Base Repository Implementation Class.
       Will be inherited by more other Repository Classes to follow
    """
    def __init__(self, db: Database) -> None:
        self.db = db

