from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_instance


class User(UserMixin, db.Model):  # class to create db schema for user details
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(
        self, password
    ):  # method for security, password setting and hashing
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):  # method for checking set password validity
        return check_password_hash(self.password_hash, password)


class Post(db.Model):  # class to create db schema for post details
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "<Post {}>".format(self.body)


@login_instance.user_loader  # to load the user from db given a user ID, when running logged in user session
def load_user(id):
    return User.query.get(int(id))
