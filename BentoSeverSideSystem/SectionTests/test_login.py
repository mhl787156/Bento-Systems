import os 
import unittest

from config import basedir
from app import app,db
from app.models import User
from forms import SignupForm, SigninForm

 """------------ Create TestSuite  -----------"""
def suite():
  return unittest.TestLoader().loadTestsFromTestCase(LoginTestCases)


class LoginTestCases(unittest.TestCase):
  
  def setUp(self):
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'test.db')
    self.app = app.test_client()
    db.create_all()

    user = User('test1','test2','07980639802',5,'test@test.com','123')
    db.session.add(user)
    db.session.commit()

  def tearDown(self):
    db.session.remove()
    db.drop_all()


 
  """------------ SignUpForm Tests  -----------"""
  def test_validate1(self):
    form = SignupForm()
    form.firstname.data = 'test1'
    form.lastname.data = 'test2'
    form.mobile_number.data = '07980639802'
    form.clearance.data = '5'
    form.email.data = 'asd@asd.com'
    form.password.data = '123'
    
    assertTrue(form.validate(),"test_validate1 failed")

  def test_validate2(self):
    form = SignupForm()
    form.firstname.data = 'test1'
    form.lastname.data = ''
    form.mobile_number.data = '07980639802'
    form.clearance.data = '5'
    form.email.data = ''
    form.password.data = '123'

    assertFalse(form.validate(),"test_validate2 failed")

  def test_emailClash(self):

    form = SignupForm()
    form.firstname.data = 'test3'
    form.lastname.data = 'test4'
    form.mobile_number.data = '0798063987'
    form.clearance.data = '5'
    form.email.data = 'test@test.com'
    form.password.data = '123'    

    assertFalse(form.validate(),"test_emailClash failed")

    



if __name__ == '__main__':
  logintest.main()
