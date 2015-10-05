import os
from flask import Flask
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.script import Manager
from flask.ext.migrate import Migrate,MigrateCommand
from config import basedir

app = Flask(__name__)
app.config.from_object('config')

api = Api(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

auth = HTTPBasicAuth()

from app import views, models, database
