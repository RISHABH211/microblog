from flask import Flask

cat = Flask(__name__)
from app import views
