import os
from flask import Flask
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.httpauth import HTTPBasicAuth
from config import basedir

app = Flask(__name__)
app.config.from_object('config')

api = Api(app)

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

auth = HTTPBasicAuth()

from app import views, models, routes
