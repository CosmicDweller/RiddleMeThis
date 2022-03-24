from datetime import timezone
from enum import unique
from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Puzzle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(1500), unique=True)
    answer = db.Column(db.String(1500))
    difficulty = db.Column(db.Integer)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))