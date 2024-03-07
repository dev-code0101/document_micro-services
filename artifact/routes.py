# artifact/routes.py

from flask import request, jsonify
from flask_login import login_required, current_user
from . import app, db
from .models import Artifact


@app.route("/upload_artifact", methods=["POST"])
@login_required
def upload_artifact():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    owner_id = current_user.id
    artifact = Artifact(name=name, description=description, owner_id=owner_id)
    db.session.add(artifact)
    db.session.commit()
    return jsonify({"message": "Artifact uploaded successfully"})
