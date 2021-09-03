"""Module where all logic about  application initialization and configuration stays"""
from fastapi import FastAPI

from api.api import api_router

from .database.tasks import create_start_app_handler, create_stop_app_handler


class Application:
    """Class responsible for app initialization and all pre and post steps configuration"""

    @staticmethod
    def run():
        """Method responsible for post installation steps and running the application"""

        app = FastAPI()
        app.include_router(api_router, prefix="/api")

        app.add_event_handler("startup", create_start_app_handler(app))
        app.add_event_handler("shutdown", create_stop_app_handler(app))

        return app