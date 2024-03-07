# auth/routes.py

from flask import request, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from . import app, db
from .models import User


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"error": "Invalid username or password"}), 401


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"})


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Registration successful"})


import hashlib


@app.route("/generate_signature/<int:artifact_id>/<int:user_id>", methods=["POST"])
def generate_signature(artifact_id, user_id):
    # Generate signature using cryptographic hashing
    signature = hashlib.sha256(f"{artifact_id}{user_id}".encode()).hexdigest()

    return jsonify({"signature": signature})


@app.route(
    "/validate_signature/<int:artifact_id>/<int:user_id>/<string:signature>",
    methods=["GET"],
)
def validate_signature(artifact_id, user_id, signature):
    # Regenerate signature using the same cryptographic hashing algorithm
    regenerated_signature = hashlib.sha256(
        f"{artifact_id}{user_id}".encode()
    ).hexdigest()

    if regenerated_signature == signature:
        return jsonify({"valid": True})
    else:
        return jsonify({"valid": False})
