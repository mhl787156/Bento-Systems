from app import db
from datetime import datetime
from werkzeug import generate_password_hash, check_password_hash
from random import randint

"""//////////////////////////////////////////////////////////////
                        EMPLOYEE DATABASE ITEMS
/////////////////////////////////////////////////////////////"""

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



"""//////////////////////////////////////////////////////////////
                        MENU DATABASE ITEMS
/////////////////////////////////////////////////////////////"""

class Menu(db.Model):
    #Items
    id = db.Column(db.Integer, primary_key=True)
    menu_name = db.Column(db.String(64),unique = True,index=True)
    last_date_changed = db.Column(db.DateTime)
    total_number_of_sections = db.Column(db.Integer())
    total_number_of_items = db.Column(db.Integer())

    #Relationships
    #one -> many with menu -> menu_sections
    menu_sections = db.relationship('MenuSection',backref='menu',lazy='dynamic')
    
    def __init__(self,menu_name):
      self.updateMenu(menu_name)

    def updateMenu(self,menu_name):
      if menu_name is not none:
        self.menu_name = menu_name.lower()
      
      self.set_last_date_changed()
      self.set_total_number_of_sections()
      self.set_total_number_of_items()

    def get_total_number_of_sections(self):
      return self.total_number_of_sections

    def set_total_number_of_sections(self):
      self.total_number_of_sections =  len(self.menu_sections.all())

    def get_total_number_of_items(self):
      return self.total_number_of_items

    def set_total_number_of_items(self):
      counter = 0
      list_of_sections = self.menu_sections.all()
      for section in list_of_sections:
        counter = counter + len(section.get_total_number_of_items())
      self.total_number_of_items = counter  

    def set_last_date_changed(self):
      self.last_date_changed = datetime.now()

    def get_last_date_changed(self):
      return last_date_changed
`
    def __repr__(self):
      return '< Menu: %r , last_date_changed: %r , numSections: %r , numItems: %r>' % (self.menu_name,self.last_date_changed,self.total_number_of_sections,self.total_number_of_items)
    
class MenuSection(db.item):
    #Items
    id = db.Column(db.Integer , primary_key=True)
    section_name = db.Column(db.String(64),unique=True,index=True)
    total_number_of_items = db.Column(db.Integer())
    menu_id = db.Column(db.Integer,db.ForeignKey('menu.id'))
    
    #Relationships
    #one -> many with 
    section_items = db.relationship('MenuItems',backref='section',lazy='dynamic')

    def __init__(self,section_name):
      self.updateMenuSection(section_name)

    def updateMenuSection(self,name):
      if name is not none:
        self.section_name = name
      self.set_total_number_of_items()   

    def set_total_number_of_items(self):
      self.total_number_of_items = len(self.section_items.all())


    def get_total_number_of_items(self):
      return self.total_number_of_items
      
    


class MenuItem(db.Model):  
    #Items
    id = db.Column(db.Integer , primary_key=True)
    item_name = db.Column(db.String(64),unique=True,index=True)
    price = db.Column(db.Integer())
    short_description = db.Column(db.String(128))
    long_description = db.Column(db.String(256))
    availability = db.Column(db.Boolean())
    ingrediants = db.Column(db.String(256))
    allergens = db.Column(db.String(256))
    menuSection_id = db.Column(db.Integer,db.ForeignKey('menusection.id'))

    #Relations
    #many <-> many , orderItem <-> menuItem
    #TODO
    
    def __init__(self,item_name,price,sd,ld,a,i,al):
      set_item_name(item_name)
      set_price(price)
      set_short_description(sd)
      set_long_description(ld)
      set_availability(a)
      set_ingrediants(i)
      set_allergens(al)


    def set_item_name(self,item_name):
      self.item_name = item_name
    def get_item_name(self):
      return self.item_name

    def set_price(self,price):
      self.price = price
    def get_price(self)
      return self.price

    def set_short_description(self,sd):
      self.short_description = sd
    def get_short_description(self):
      return self.short_description

    def set_long_description(self,ld):
      self.long_description = ld
    def get_short_description(self):
      return self.long_description

    def set_availability(self,a):
      self.availability = a
    def get_avaliability(self):
      return self.availability

    def set_ingrediants(self,i):
      self.ingrediants = i
    def get_ingrediants(self):
      return self.ingrediants

    def set_allergens(self,al):
      self.allergens = al
    def get_allergens(self):
      return self.allergens

    
    def __repr__(self):
      return '< ItemName: %r , Price %r >' % (self.item_name , self.price)

#Might be right thing to do??

menuItem_orderItem = db.Table('menuItem_orderItem',
    db.Column('orderItem_id',db.Integer,db.ForeignKey('orderItem.id'))
    db.Column('menuItem_id',db.Integer,db.ForeignKey('menuItem.id'))
)            



"""//////////////////////////////////////////////////////////////
                    ORDER DATABASE ITEMS
/////////////////////////////////////////////////////////////"""


class Order(db.Model):
    #Fields
    id = db.Column(db.Integer , primary_key=True)
    table_number = db.Column(db.Integer())
    number_of_customers = db.Column(db.Integer())

    current_number_of_items = db.Column(db.Integer())
    total_price = db.Column(db.Integer())
    
    #Relationship Fields




    def __init__(self,table_number,number_of_customers):
      self.table_number = table_number
      self.number_of_customers = number_of_customers
      self.current_number_of_items = 0
      self.total_price = 0
      
    def add_item(self,itemID,quantity):
      #TODO

    def get_current_price(self):
      return self.current_price

    def set_current_price(self,price):
      self.current_price = price

    def get_number_of_items(self):
      return current_number_of_items

    def update_number_of_items(self):
      #TODO

    def pay(self):
      #TODO

    def __repr__(self):
      #TODO


class OrderItem(db.Model):
    #Fields
    id = db.Column(db.Integer , primary_key=True)
    item_number = db.Column(db.Integer())
    quantity = db.Column(db.Integer())
    sub_price = db.Column(db.Integer())
    
    #Relationship Fields
    #TODO menuItem = 

    def __init__(self,itemNumber, quantity):
      self.item_number = itemNumber
      self.quantity = quantity
      self.set_subPrice()#TODO


    def get_itemNumber_menuItem(self):  
    #TODO
  
    def update_quantity(self,additionalUnits):
      self.quantity = self.quantity + additionalUnits

    def set_subPrice(self,itemPrice):
      q = itemPrice * self.quantity
      self.sub_price = q

    def get_subPrice(self):
      return sub_price

    def get_quantity(self):
      return quantity

    def __repr__(self):
      return '< OrderItem: %r >' % item_number


class OrderCounter(db.Model):
    #Fields
    id = db.Column(db.Integer , primary_key=True)
    current_number_of_orders = db.Column(db.Integer)
    
    #Relationship Fields
    #orders = 
    
    def __init__(self):
      set_current_number_of_orders()

    def get_current_number_of_orders(self):
      #TODO

    def set_current_number_of_orders(self):
      #TODO
    
    def __repr__(self):
      return '< Ongoing orders: %r >' % (current_number_of_orders)



class OrderLogger(db.Model):
    #Fields
    id = db.Column(db.Integer , primary_key=True)
    date = db.Column(db.datetime)
    
    #Relationship Fields











  
