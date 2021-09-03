"""App entry point module to start the application server"""
from core.service import Application

application = Application.run()
