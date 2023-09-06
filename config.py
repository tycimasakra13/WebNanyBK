import os
import sqlalchemy


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secret_string"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEVELOPMENT_DATABASE_URL")





