from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


cat: Flask = Flask(__name__)  # cat is the instance/object of Flask class
cat.config.from_object(Config)  # cat is importing the configuration from config.py
db = SQLAlchemy(cat)  # db is an instance of SQLAlchemy with argument as Flask object
migration_instance = Migrate(
    cat, db
)  # migration_instance is an object of Migrate class
login_instance = LoginManager(
    cat
)  # login_instance is object of LoginManager taken from flask_login
login_instance.login_view = (
    "login"  # Flask-Login needs to know what is the view function that handles logins
)
from app import (
    views,
    models,
)  # from app import views and models later after cat instance, as circular reference
