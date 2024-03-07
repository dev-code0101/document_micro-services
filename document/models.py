# document/models.py

from db import db


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    file_path = db.Column(db.String(255))
    artifact_id = db.Column(db.Integer, db.ForeignKey("artifact.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Document {self.name}>"
