from . import views

from flask import Flask

__all__ = ['app']


application = Flask(__name__)
application.register_blueprint(views.bp)
