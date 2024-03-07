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


import boto3
from botocore.exceptions import NoCredentialsError

s3 = boto3.client(
    "s3", aws_access_key_id="YOUR_ACCESS_KEY", aws_secret_access_key="YOUR_SECRET_KEY"
)

app.config["S3_BUCKET"] = "your-s3-bucket-name"


def upload_to_s3(file, bucket_name=app.config["S3_BUCKET"], object_name=None):
    if object_name is None:
        object_name = file.name
    try:
        s3.upload_fileobj(file, bucket_name, object_name)
    except NoCredentialsError:
        return False
    return True


from google.cloud import storage

storage_client = storage.Client.from_service_account_json(
    "path/to/your/credentials.json"
)


def upload_to_gcs(file, bucket_name=app.config["BUCKET_NAME"], object_name=None):
    if object_name is None:
        object_name = file.name
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_file(file)


def save_locally(file):
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)


@app.route("/upload_document", methods=["POST"])
@login_required
def upload_document():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        save_locally(file)

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
