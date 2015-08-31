from app import app,db
from app.models import User
from app.forms import SignupForm, SigninForm
from SectionTests import test_set_up


class LoginTestCases(test_set_up.AbstractTestCases):



  """------------ Helper Functions -----------"""
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

  def removeUser(self):
    return self.app.get('/removeUser',follow_redirects=True)

  def logout(self):
    return self.app.get('/signout',follow_redirects=True)

 
  """------------ SignUpForm Tests  -----------"""

  
  def test_signup_login_and_remove(self):
    rv = self.signup('test16','test82','07980639802',5,'asd1@asd.com','hello')
    self.assertTrue('Successful Signup' in rv.data
                    and 'test16.test82' in rv.data
                    ,"Signup was not successful")
  
    self.assertTrue(self.tryLogin('test16','test82','hello'),"Login was not Successful, no employee_id match")

    rv = self.removeUser()
    self.assertTrue('Removed Successfully' in rv.data,"Removal was not successful")

   
  def test_failedValidation(self):
    rv = self.signup('test1','','0987126352',3,'','123')

    self.assertTrue('Please enter a Last Name' in rv.data and
                     'Please enter your email address' in rv.data,
                     "validators not working")

  def test_emailClash(self):
    rv = self.signup('t','t','01238679',1,'test@test.com','123')
    self.assertTrue('Successful Signup' in rv.data)
    rv = self.signup('t','x','1234564897',1,'test@test.com','345')
    self.assertTrue('Duplicated email' in rv.data,'Failed email duplication tester')

  def test_removeUser(self):
    self.signup('t','t','01238679',1,'test@test.com','123')
    self.tryLogin('t','t','123')
    self.removeUser()
    self.assertTrue(User.query.all()==[],'did not remove')

if __name__ == '__main__':
  unittest.main()
