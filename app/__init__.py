from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_mail import Mail
from flask_bootstrap import Bootstrap


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
mail = Mail(cat)

from app import (
    views,
    models,
    errors,
)  # from app import views and models later after cat instance, as circular reference

bootstrap = Bootstrap(cat)

if (
    not cat.debug
):  # setting up e-mail server system to send error reports when debugging is OFF,only error messages, not warning
    if cat.config["MAIL_SERVER"]:
        auth = None
        if cat.config["MAIL_USERNAME"] or cat.config["MAIL_PASSWORD"]:
            auth = (cat.config["MAIL_USERNAME"], cat.config["MAIL_PASSWORD"])
        secure = None
        if cat.config["MAIL_USE_TLS"]:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cat.config["MAIL_SERVER"], cat.config["MAIL_PORT"]),
            fromaddr="no-reply@" + cat.config["MAIL_SERVER"],
            toaddrs=cat.config["ADMINS"],
            subject="Microblog Failure",
            credentials=auth,
            secure=secure,
        )
        mail_handler.setLevel(logging.ERROR)
        cat.logger.addHandler(mail_handler)
    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = RotatingFileHandler(
        "logs/microblog.log", maxBytes=10240, backupCount=10
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(logging.INFO)
    cat.logger.addHandler(file_handler)

    cat.logger.setLevel(logging.INFO)
    cat.logger.info("Microblog startup")
