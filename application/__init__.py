import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from config import Config

app = Flask(__name__)

app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://webnany:Nanydb123@webnany.postgres.database.azure.com:5432/webnany"
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:admin@localhost:5432/webnany"

db = SQLAlchemy(app)

metadata_obj = MetaData(schema="wn")
db.metadata.schema = metadata_obj.schema

from application import routes


