# auth/app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import User
from .routes import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../db/database.db"
app.secret_key = "your_secret_key_here"  # Change this to a secure secret key
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = (
    "login"  # Redirect to login page if user tries to access restricted content
)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
