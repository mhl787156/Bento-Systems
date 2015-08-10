from models import db, User
from flask import g
from flask.ext.wtf import Form
from wtforms import SelectField , TextField, SubmitField, ValidationError, PasswordField , validators , IntegerField


"""/////////////////////////////////////////////////////////
                    Menu Forms
/////////////////////////////////////////////////////////"""
class CreateMenuForm(Form):
  menuName = TextField("Menu Name" , [validators.Required("Please enter a Menu Name.")])
  
  def __init__(self,*args,**kwargs):
    Form.__init__(self,*args,**kwargs)

  def validate(self):
    if not Form.validate(self):
      return False

    if User.querty.filter_by(menu_name = self.menuName.data.lower()).first() is not None:
      self.menuName.errors.append('Duplicated menu name')
      return False
    return True


class AddMenuSectionForm(Form):
  #menu = drop down of all available menus
  sectionName = TextField("Section Name" ,[validators.Required("Please enter a Section Name")])
  
  def __init__(self,*args,**kwargs):
    Form.__init__(self,*args,**kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    return True

"""/////////////////////////////////////////////////////////
                    Profile Forms
/////////////////////////////////////////////////////////"""

class SignupForm(Form):
  firstname = TextField("First Name",  [validators.Required("Please enter a First Name.")])
  lastname = TextField("Last Name",  [validators.Required("Please enter a Last Name.")])
  mobile_number = TextField("Mobile Phone Number", [validators.Required("Please enter a phone number")])
  clearance = IntegerField("Clearance" , [validators.Required("Please determine your system clearance."), validators.NumberRange(min = 0, max = 5,message = "Make sure we have a valid clearance")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter a valid email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Add to Database")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      print "Form Not Validated!!!!" + str(Form.validate(self))
      return False
    
    #check email uniquness
    if User.query.filter_by(email = self.email.data.lower()).first() is not None:
      self.email.errors.append("Duplicated email")
      return False
        
    return True;
    
class editProfile(Form):
  mobile_number = TextField("Mobile Phone Number", [validators.Required("Please enter a phoe number")])
  email = TextField("Email", [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])  
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Edit details")
 
  def __init__(self, *args, **kwargs):
       Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
       return False
    
    #If new emil is not None, then we are ok
    if self.email.data.lower() != user.email and User.query.filter_by(email = self.email.data.lower()) is not None:
       self.email.errors.append("Duplicated email")
       return False
  
    if user.check_password(self.password.data):
      if user.mobile_number != self.mobile_number.data:
        user.mobile_number = self.mobile_number.data
      
      if user.email != self.email.data.lower():
        user.email = self.email.data.lower()
       
      return True
    else:
      self.employee_id.errors.append("Invalid ID or password")
      return False  
    


class SigninForm(Form):
  employee_id = TextField("Employee_id: ",  [validators.Required("Please enter A valid employee_ID.")])
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
