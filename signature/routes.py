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


@app.route("/artifacts", methods=["GET"])
@login_required
def get_artifacts():
    # Retrieve artifacts owned by the current user
    artifacts = Artifact.query.filter_by(owner_id=current_user.id).all()
    artifacts_data = [
        {"id": artifact.id, "name": artifact.name, "description": artifact.description}
        for artifact in artifacts
    ]
    return jsonify({"artifacts": artifacts_data})


@app.route("/generate_signature/<int:artifact_id>/<int:user_id>", methods=["POST"])
@login_required
def generate_signature(artifact_id, user_id):
    # Check if the current user owns the artifact
    artifact = Artifact.query.filter_by(
        id=artifact_id, owner_id=current_user.id
    ).first()
    if not artifact:
        return (
            jsonify(
                {
                    "error": "Artifact not found or you do not have permission to generate signature"
                }
            ),
            404,
        )

    # Generate signature using cryptographic hashing
    signature = hashlib.sha256(f"{artifact_id}{user_id}".encode()).hexdigest()
    return jsonify({"signature": signature})


@app.route(
    "/validate_signature/<int:artifact_id>/<int:user_id>/<string:signature>",
    methods=["GET"],
)
@login_required
def validate_signature(artifact_id, user_id, signature):
    # Check if the current user owns the artifact
    artifact = Artifact.query.filter_by(
        id=artifact_id, owner_id=current_user.id
    ).first()
    if not artifact:
        return (
            jsonify(
                {
                    "error": "Artifact not found or you do not have permission to validate signature"
                }
            ),
            404,
        )

    # Regenerate signature using the same cryptographic hashing algorithm
    regenerated_signature = hashlib.sha256(
        f"{artifact_id}{user_id}".encode()
    ).hexdigest()

    if regenerated_signature == signature:
        return jsonify({"valid": True})
    else:
        return jsonify({"valid": False})
