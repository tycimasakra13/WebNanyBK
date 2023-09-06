import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config



app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DEVELOPMENT_DATABASE_URL")

db = SQLAlchemy(app)

from application import routes


