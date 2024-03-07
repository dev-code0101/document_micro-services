# document/routes.py

import os
from flask import request, jsonify, send_from_directory
from flask_login import login_required, current_user
from . import app, db
from .models import Document

UPLOAD_FOLDER = "uploads"


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


@app.route("/upload_document", methods=["POST"])
@login_required
def upload_document():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # Save document metadata to the database
        document = Document(name=filename, file_path=file_path)
        db.session.add(document)
        db.session.commit()

        return jsonify({"message": "Document uploaded successfully"})
    else:
        return jsonify({"error": "File type not allowed"}), 400


@app.route("/download_document/<int:document_id>", methods=["GET"])
@login_required
def download_document(document_id):
    document = Document.query.filter_by(id=document_id, user_id=current_user.id).first()
    if document:
        return send_from_directory(directory=UPLOAD_FOLDER, filename=document.file_path)
    else:
        return jsonify({"error": "Document not found"}), 404


@app.route("/update_document/<int:document_id>", methods=["PUT"])
@login_required
def update_document(document_id):
    document = Document.query.filter_by(id=document_id, user_id=current_user.id).first()
    if document:
        new_name = request.json.get("name")
        document.name = new_name
        db.session.commit()
        return jsonify({"message": "Document updated successfully"})
    else:
        return jsonify({"error": "Document not found"}), 404


@app.route("/delete_document/<int:document_id>", methods=["DELETE"])
@login_required
def delete_document(document_id):
    document = Document.query.filter_by(id=document_id, user_id=current_user.id).first()
    if document:
        db.session.delete(document)
        db.session.commit()
        return jsonify({"message": "Document deleted successfully"})
    else:
        return jsonify({"error": "Document not found"}), 404
