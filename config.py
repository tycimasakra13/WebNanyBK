import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secret_string"
    DB_SETTINGS = {"db_name": "webnany"}
