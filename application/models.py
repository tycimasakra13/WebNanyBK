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