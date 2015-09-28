from models import db, User,Menu,MenuSection,MenuItem
from flask import g,flash
from flask.ext.wtf import Form
from wtforms import BooleanField, TextAreaField ,DecimalField, SelectField , TextField, SubmitField, ValidationError, PasswordField , validators , IntegerField


"""/////////////////////////////////////////////////////////
                    Menu Forms
/////////////////////////////////////////////////////////"""
class SelectMenuForm(Form):
  menu = SelectField("Menu",coerce = int, validators = [validators.Required("Please choose a menu")])
  submit = SubmitField("Select Menu")
  def validate(self):
    return Form.validate(self)

class SelectSectionForm(Form):
  publicSections = SelectField("Public Section",coerce=int)
  privateSections = SelectField("Private Section",coerce=int)
  pubsubmit = SubmitField("Select Section")
  privsubmit = SubmitField("Select Section")
  def validate(self):
    return Form.validate(self)

class SelectItemForm(Form):
  item = SelectField("Item",coerce=int,validators=[validators.Required("Please choosa a valid item")])
  submit = SubmitField("Select Item")
  def validate(self):
    return Form.validate(self)

class AddorEditMenuForm(Form):
  menuName = TextField("Menu Name", validators=[validators.Required("Please enter a Menu Name.")])
  cnSubmit = SubmitField("Change Name")
  removeSection = SelectField("Remove a section",coerce=int,default=0)
  rmSecSubmit = SubmitField("Remove Section from Menu")
  sections = SelectField("Add a Section",coerce=int,default=0)
  addSectionSubmit = SubmitField("Add a Section to this Menu")
  remove = SubmitField("Remove from Database")
  submit = SubmitField("Add to Database")
  
  def __init__(self,*args,**kwargs):
    Form.__init__(self,*args,**kwargs)

  def validate(self):
    if not self.menuName.data:
      return False

    if Menu.query.filter_by(menu_name = self.menuName.data.lower()).first() is not None:
      self.menuName.errors.append('Duplicated menu name')
      flash('Duplicated Name')
      return False
    return True




class AddorEditMenuSectionForm(Form):
  sectionName = TextField("Section Name" ,validators=[validators.Required("Please enter a Section Name")])
  visibility = BooleanField("Publicly Visible",validators=[validators.Required("Please choose whether this section will be publically visible or not")])
  s_s_o = SelectField("Staggered Service Order",coerce=int,
                choices=[(0,"Not Applicable"),(1,"Before the Main Course"),(2,"With/As the Main Course"),(3,"After the Main Course")],
                validators=[validators.Required("Please choose a Service Position")],
                default = 0)
  ppSubmit = SubmitField("Save Section Property Changes")
  subsectionRemove = SelectField("SubSection",coerce=int,default=0)
  ssRmSubmit = SubmitField("Remove Subsection from Section")
  itemRemove = SelectField("Item",coerce=int,default=0)
  itemRmSubmit = SubmitField("Remove Item form Section")
  subsection = SelectField("SubSection",coerce=int,default=0)
  sssubmit = SubmitField("Add SubSection to Section")
  items = SelectField("Items",coerce=int,default=0)
  itemsubmit = SubmitField("Add Item to Section")
  submit = SubmitField("Add to Database")
  remove = SubmitField("Remove from Database")
  
  def __init__(self,*args,**kwargs):
    Form.__init__(self,*args,**kwargs)

  def validate(self):
    if not self.sectionName.data:
      return False

    if MenuSection.query.filter_by(section_name=self.sectionName.data.lower()).first() is not None:
        self.sectionName.errors.append('Duplicated section name')
        flash('duplicated name')
        return False
    return True

class AddorEditMenuItemForm(Form):
  item_id = TextField("Item id",validators=[validators.Required("Please choose an item id")])
  item_name = TextField("Item Name", validators=[validators.Required("Please choose an item name")])
  price = DecimalField("Item Price", places=2,validators=[validators.Required("Please input a price")])
  short_description = TextAreaField("Item's Short Description")
  long_description = TextAreaField("Item's Long Description")
  availability = BooleanField("Currently Available?")
  ingrediants = TextAreaField("A list of ingrediants of this product")
  allergens = TextAreaField("A list of possible allergens in this product")
  ppItemSubmit = SubmitField("Change Properties")

  submit = SubmitField("Save Changes")
  
  remove = SubmitField("Remove this Item")
 
  def __init__(self,*args,**kwargs):
    Form.__init__(self,*args,**kwargs)

  def validate(self): 
    if not Form.validate(self):
      if MenuItem.query.filter_by(item_name=self.item_name.data.lower()).first() is not None or MenuItem.query.filter_by(item_id=self.item_id.data).first() is not None:
        flash('Duplicated name or Id, pelase change')
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
  password = PasswordField('Password')
  submit = SubmitField("Add to Database")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
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
