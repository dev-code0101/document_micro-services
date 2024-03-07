# db/models.py

from .db import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")

    def __repr__(self):
        return f"<User {self.username}>"


class Artifact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Artifact {self.name}>"


class Signature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    signature = db.Column(db.String(256), unique=True)
    artifact_id = db.Column(db.Integer, db.ForeignKey("artifact.id"))


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    file_path = db.Column(db.String(255))
    artifact_id = db.Column(db.Integer, db.ForeignKey("artifact.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Document {self.name}>"
