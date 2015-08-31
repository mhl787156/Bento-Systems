import os
import unittest

from config import basedir
from app import app,db
from app.models import User

class AbstractTestCases(unittest.TestCase):
  
  def setUp(self):
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'SectionTests/test.db')
    self.app = app.test_client()
    db.create_all()

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    os.remove('SectionTests/test.db')

  def signup(self,firstname,lastname,mobile_number,clearance,email,password):
    self.app.get('/signup') 
    return self.app.post('/signup', data = dict(
      firstname = firstname,
      lastname=lastname,
      mobile_number=mobile_number,
      clearance=clearance,
      email=email,
      password=password,
      ) , follow_redirects=True)

  def login(self,employee_id,password):
    self.app.get('/login')    

    return self.app.post('/login', data = dict(
      employee_id = employee_id,
      password = password
      ) ,follow_redirects = True)

  def tryLogin(self,firstname,lastname,password):
    for x in range(0,100):
      rv = self.login(firstname+'.'+lastname+str(x) , password)
      if 'Successful Login' in rv.data:
        return True
    return False

