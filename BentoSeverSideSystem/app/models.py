from app import db
from datetime import datetime
from werkzeug import generate_password_hash, check_password_hash
from random import randint

counter = 0


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(64), index=True, unique=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    mobile_number = db.Column(db.String(64))
    date_joined = db.Column(db.DateTime)
    clearance = db.Column(db.Integer())
    email = db.Column(db.String(120), index=True, unique=True)	
    pwdhash = db.Column(db.String(54))
    password = db.Column(db.String(54))

 
    def __init__(self, firstname,lastname, mobile_number, clearance, email, password):      
       	self.create_employee_id(firstname,lastname)
        self.firstname = firstname.title()
      	self.lastname = lastname.title()
      	self.mobile_number = mobile_number
      	self.clearance = clearance
        self.date_joined = datetime.now()
        self.email = email.lower()
        self.set_password(password)
        self.password = password

    def create_employee_id(self,firstname,lastname):
      	self.employee_id = firstname.lower()+"."+lastname.lower() + str(randint(0,100))

     
    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)
   
    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '< User: %r , Email: %r , Password: %r>' % (self.employee_id,self.email,self.password)

