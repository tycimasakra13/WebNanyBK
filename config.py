import os
import sqlalchemy


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "b'9\xc9\xe9\x15F%o\xa9u\xfa\x92\x89\xbey\xf8\x88'"
