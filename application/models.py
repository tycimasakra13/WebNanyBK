import cv2
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import Any
from sqlalchemy.orm import relationship, backref

from application import db
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    e_mail = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)

    def to_json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'e_mail': self.e_mail,
            'password': self.password
        }


class Devices(db.Model):
    device_id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(50), unique=False, nullable=False)
    device_platform = db.Column(db.String(50), unique=True, nullable=False)
    is_streaming = db.Column(db.Boolean)
    is_watching = db.Column(db.Boolean)
    user_id = db.mapped_column(db.Integer, ForeignKey("users.id"))
    user = db.relationship("Users", foreign_keys=[user_id])


    def to_json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'e_mail': self.e_mail,
            'password': self.password
        }

class Camera:
    def __init__(self, fps=20, video_source=0):
        print(f"Initializing camera class with {fps} fps and video_source={video_source}")
        self.fps = fps
        self.video_source = video_source
        self.camera = cv2.VideoCapture(self.video_source)
        # We want a max of 5s history to be stored, thats 5s*fps
        self.max_frames = 5 * self.fps
        self.frames = []
        self.isrunning = False