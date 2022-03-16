from flask import Flask

from storify.blueprints.account.models import User

from .register import authentication, blueprints, extensions


def create_app():
    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    """
    app = Flask(__name__, static_folder='../static')

    app.config.from_object('config.settings')

    authentication(app, User)
    blueprints(app)
    extensions(app)

    return app
