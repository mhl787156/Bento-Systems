import os 
import unittest


from .config import basedir
from app import app,db
from app.models import User
from app.forms import SignupForm, SigninForm

"""------------ Create TestSuite  -----------"""
def suite():
  return unittest.TestLoader().loadTestsFromTestCase(LoginTestCases)


class LoginTestCases(unittest.TestCase):
  
  def setUp(self):
    app.config['TESTING'] = True
    #app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'test.db')
    self.app = app.test_client()
    db.create_all()

    user = User('test1','test2','07980639802',5,'test@test.com','123')
    db.session.add(user)
    db.session.commit()

  def tearDown(self):
    db.session.remove()
    db.drop_all()

  """------------ Helper Functions -----------"""
  def login(self,firstname,lastname,mobile_number,clearance,email,password):
    return self.app.post('/login', data = dict(
      firstname = firstname,
      lastname=lastname,
      mobile_number=mobile_number,
      clearance=clearance,
      email=email,
      password=password
      ) , follow_redirects=True)

  def logout(self):
    return self.app.get('/signout',follow_redirects=True)

 
  """------------ SignUpForm Tests  -----------"""
  def test_validate1(self):
    rv = self.login('test1','test2','07980639802',5,'asd@asd','123')
    assert 'Successful Login' in rv.data
    rv = self.logout
    assert 'You were logged out' in rv.data



  """
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
  """
    



if __name__ == '__main__':
  logintest.main()
