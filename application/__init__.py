import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)

app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://webnany:Nanydb123@webnany.postgres.database.azure.com:5432/webnany"

db = SQLAlchemy(app)

from application import routes


