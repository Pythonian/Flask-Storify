import os
from distutils.util import strtobool

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dotenv_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

DEBUG = True

SERVER_NAME = os.getenv('SERVER_NAME')

SECRET_KEY = os.getenv('SECRET_KEY')

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
    os.path.join(BASE_DIR, 'sqlite.db')

# Flask-Mail.
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = os.getenv('MAIL_PORT')
MAIL_USE_TLS = bool(strtobool(os.getenv('MAIL_USE_TLS')))
MAIL_USE_SSL = bool(strtobool(os.getenv('MAIL_USE_SSL')))
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_SUBJECT_PREFIX = "[Storify] "
