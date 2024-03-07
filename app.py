from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from db import db
from models import db, Artifact, Signature


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)

app.config["UPLOAD_FOLDER"] = "uploads"
app.config["ALLOWED_EXTENSIONS"] = {"txt", "pdf", "doc", "docx"}


@app.route("/upload_artifact", methods=["POST"])
def upload_artifact():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    owner_id = data.get("owner_id")

    artifact = Artifact(name=name, description=description, owner_id=owner_id)
    db.session.add(artifact)
    db.session.commit()

    return jsonify({"message": "Artifact uploaded successfully"})


if __name__ == "__main__":
    app.run(debug=True)
