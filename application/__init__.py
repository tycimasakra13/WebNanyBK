import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_socketio import SocketIO, emit
from azure.messaging.webpubsubservice import WebPubSubServiceClient
import base64

from config import Config

app = Flask(__name__)
#socketio = SocketIO(app)
connection_string='Endpoint=https://webnany.webpubsub.azure.com;AccessKey=CEO246i3eWgYIt57HIgNGD47d4UqFJpz5Cy/jMhQnBk=;Version=1.0;'
socketio = WebPubSubServiceClient.from_connection_string(connection_string=connection_string, hub='Hub')

app.config.from_object(Config)
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:admin@localhost:5432/webnany"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://webnany:Nanydb123@webnany.postgres.database.azure.com:5432/webnany"

db = SQLAlchemy(app)

metadata_obj = MetaData(schema="wn")
db.metadata.schema = metadata_obj.schema

from application import routes



