# artifact/app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import Artifact
from .routes import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../db/database.db"
db = SQLAlchemy(app)
