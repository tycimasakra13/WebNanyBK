from flask import Flask
from config import Config
from flask_postgresql import PostgreSQL

app = Flask(__name__)
app.config.from_object(Config)

db = PostgreSQL()
db.init_app(app)

from application import routes
