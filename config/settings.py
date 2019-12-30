import os
from distutils.util import strtobool

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = os.getenv('SECRET_KEY', 'dev')

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
    os.path.join(BASE_DIR, 'sqlite.db')

# Flask-Mail.
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'no-reply@example.com')
MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = os.getenv('MAIL_PORT', 587)
MAIL_USE_TLS = bool(strtobool(os.getenv('MAIL_USE_TLS', 'true')))
MAIL_USE_SSL = bool(strtobool(os.getenv('MAIL_USE_SSL', 'false')))
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_SUBJECT_PREFIX = "[Storify] "
