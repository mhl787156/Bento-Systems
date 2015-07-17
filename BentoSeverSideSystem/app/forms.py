from models import db, User
from flask.ext.wtf import Form
from wtforms import SelectField , TextField, SubmitField, ValidationError, PasswordField , validators , IntegerField

class SignupForm(Form):
  firstname = TextField("First Name",  [validators.Required("Please enter a First Name.")])
  lastname = TextField("Last Name",  [validators.Required("Please enter a Last Name.")])
  mobile_number = TextField("Mobile Phone Number", [validators.Required("Please enter a phone number")])
  clearance = IntegerField("Clearance" , [validators.Required("Please determin your system clearance."), validators.NumberRange(min = 0, max = 5,message = "Make sure we have a valid clearance")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Add to Database")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False


class SigninForm(Form):
  employee_id = TextField("Employee_id: ",  [validators.Required("Please enter your ID address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Sign In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(employee_id = self.employee_id.data.lower()).first()
   
    if user is not None and user.check_password(self.password.data):
      return True
    else:
      self.employee_id.errors.append("Invalid ID or password")
      return False
