import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail


app = Flask(__name__)
app.secret_key = os.getenv('SESSION_KEY')
app.config.from_object('config')

db = SQLAlchemy(app)
mail = Mail(app)

from app import views, models