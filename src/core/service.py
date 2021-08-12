from fastapi import FastAPI


class Application:

    def run(self):
        """Method responsible for post installation steps and running the application"""
        app = FastAPI()
        return app
