from flask import Flask, render_template
from storify.blueprints.account.models import User
from .register import authentication, blueprints, extensions
from .extensions import db


def create_app():
    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    """
    app = Flask(__name__)

    app.config.from_object('config.settings')

    authentication(app, User)
    blueprints(app)
    extensions(app)

    @app.route('/')
    def home():
        return render_template("home.html")

    @app.shell_context_processor
    def make_shell_context():
        """Create a shell context for all models."""
        return dict(User=User, db=db)

    return app
