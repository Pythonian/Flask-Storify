from storify.blueprints.account import auth, user
from storify.blueprints.story import story
from storify.blueprints.menu import menu
from storify.blueprints.topic import topic
from .extensions import (csrf, db, login_manager, mail, migrate, moment)

FLASK_BLUEPRINTS = [auth, user, story, menu, topic]


def authentication(app, user_model):
    """
    Initialize the Flask-Login extension (mutates the app passed in).

    :param app: Flask application instance
    :param user_model: Model that contains the authentication information
    :type user_model: SQLAlchemy model
    :return: None
    """
    login_manager.login_message = "Please login to access this page."
    login_manager.login_view = 'auth.login'
    login_manager.session_protection = 'strong'
    login_manager.login_message_category = 'danger'

    @login_manager.user_loader
    def load_user(user_id):
        return user_model.query.get(int(user_id))


def blueprints(app):
    """
    Register 0 or more blueprints (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    for blueprint in FLASK_BLUEPRINTS:
        app.register_blueprint(blueprint)

    return None


def extensions(app):
    """
    Register 0 or more flask extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    csrf.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    login_manager.init_app(app)

    return None
