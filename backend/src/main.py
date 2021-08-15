"""App entrypoint module"""
from core.service import Application

app = Application()
application = app.run()
