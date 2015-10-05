from app import db
from datetime import datetime
from werkzeug import generate_password_hash, check_password_hash
from random import randint





def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
      return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

"""//////////////////////////////////////////////////////////////
                        EMPLOYEE DATABASE ITEMS
/////////////////////////////////////////////////////////////"""

class User(db.Model):
    __tablename__ = 'user'
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

        self.password = password # Remember to remove on use

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
          
    def serialize(self):
      return {
          'id' : self.id,
          'employee_id' : self.employee_id,
          'firstname' : self.firstname,
          'lastname' : self.lastname,
          'mobile_number' : self.mobile_number,
          'date_joined' : dump_datetime(self.date_joined),
          'email' : self.email
        }

    def __repr__(self):
      return '< User: %r Password: %r >' % (self.employee_id,self.password)

class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(64), index=True, unique=True)
    pwdhash = db.Column(db.String(54))
 
    def __init__(self, device_id , password):      
        device_id = device_id
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)
   
    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


    def __repr__(self):
      return '< Device_id: %r >' % (self.device_id)


"""//////////////////////////////////////////////////////////////
                        MENU DATABASE ITEMS
/////////////////////////////////////////////////////////////"""


menu_to_section = db.Table("menu_to_section",
    db.Column("menu_id",db.Integer,db.ForeignKey('menu.id')),
    db.Column("menusection_id",db.Integer,db.ForeignKey('menusection.id'))
)


class Menu(db.Model):
    __tablename__ = 'menu'
    #Items
    id = db.Column(db.Integer, primary_key=True)
    menu_name = db.Column(db.String(64),unique = True,index=True)
    last_date_changed = db.Column(db.DateTime)
    total_number_of_sections = db.Column(db.Integer())
    total_number_of_items = db.Column(db.Integer())

    #Relationships
    
    #many -> many with menu -> menu_sectionos
  
    menu_sections = db.relationship('MenuSection',
                        secondary=menu_to_section,
                        backref=db.backref('menu',lazy='dynamic'),lazy='dynamic')
    
    
    def __init__(self,menu_name):
      self.updateMenu(menu_name)

    def serialize(self):
      return {
          'id' : self.id,
          'menu_name' : self.menu_name,
          'last_date_changed' : dump_datetime(self.last_date_changed),
          'total_number_of_sections' : self.total_number_of_sections,
          'total_number_of_items' : self.total_number_of_items,
          'menu_sections' : [item.short_serialize() for item in self.menu_sections]
          }

    def updateMenu(self,menu_name=None):
      if menu_name is not None:
        self.menu_name = menu_name.lower()
      
      self.set_last_date_changed()
      self.set_total_number_of_sections()
      self.set_total_number_of_items()

    def isPartOfMenu(self,section):
      return self.menu_sections.filter(menu_to_section.c.menusection_id==section.id).count() > 0

    def getSections(self):
      return self.menu_sections.all()
    
    def addSection(self,section):
      if not self.isPartOfMenu(section):
        self.menu_sections.append(section)
        self.updateMenu()
        return self


    def deleteSection(self,section):
      if self.isPartOfMenu(section):
        self.menu_sections.remove(section)
        self.updateMenu()
        return self
    
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
        counter = counter + section.get_total_number_of_items()
      self.total_number_of_items = counter  

    def set_last_date_changed(self):
      self.last_date_changed = datetime.now()

    def get_last_date_changed(self):
      return last_date_changed

    def __repr__(self):
      return '< Menu: %r , last_date_changed: %r , numSections: %r , numItems: %r>' % (self.menu_name,self.last_date_changed,self.total_number_of_sections,self.total_number_of_items)

section_to_item = db.Table("section_to_item",
    db.Column("menusection_id",db.Integer,db.ForeignKey('menusection.id')),
    db.Column("menuitem_id",db.Integer,db.ForeignKey('menuitem.id'))
    )

section_to_subsection = db.Table("section_to_subsection",
    db.Column("menusection_id",db.Integer,db.ForeignKey('menusection.id')),
    db.Column("menusubsection_id",db.Integer,db.ForeignKey("menusection.id"))
    )


class MenuSection(db.Model):
    __tablename__ = 'menusection'
    #Items
    id = db.Column(db.Integer , primary_key=True)
    section_name = db.Column(db.String(64),unique=True,index=True)
    number_of_groups = db.Column(db.Integer())
    total_number_of_items = db.Column(db.Integer())
    visibility = db.Column(db.Boolean())
    staggered_service_order = db.Column(db.Integer())
    # 0=anytime 1 = Before Main meal, 2= with main meal, 3=after main meal

    #Relationships
    #many <-> many with section <-> item
    section_items = db.relationship('MenuItem',secondary=section_to_item,
        backref='section',lazy='dynamic')
    #many <-> many with section <-> subsection
    subsections = db.relationship('MenuSection',secondary=section_to_subsection,
        primaryjoin=(section_to_subsection.c.menusection_id == id), 
        secondaryjoin=(section_to_subsection.c.menusubsection_id == id),
        backref='parentSection',lazy='dynamic')

    def __init__(self,section_name,visibility,staggered_service_order):
      self.updateMenuSection(section_name)
      self.visibility = visibility
      self.staggered_service_order = staggered_service_order

    def serialize(self):
      return {
            'id' : self.id,
            'section_name' : self.section_name,
            'number_of_groups' : self.number_of_groups,
            'total_number_of_items' : self.total_number_of_items,
            'visibility' : self.visibility,
            'staggered_service_order' : self.staggered_service_order,
            'section_items' : [item.serialize() for item in self.section_items],
            'subsections' : [s.serialize() for s in self.subsections],
            'menus_belonged_to' : [s.id for s in self.menu],
            'parent_sections' : [s.id for s in self.parentSection]
          }

    def short_serialize(self):
      if self.number_of_groups > 0:
        return {
            'id' : self.id,
            'section_name' : self.section_name,
            'number_of_groups' : self.number_of_groups,
            'total_number_of_items' : self.total_number_of_items,
            'subsections' : [s.short_serialize() for s in self.subsections],
          }
      
      return {
            'id' : self.id,
            'section_name' : self.section_name,
            'number_of_groups' : self.number_of_groups,
            'total_number_of_items' : self.total_number_of_items,
            'section_items' : [item.short_serialize() for item in self.section_items],
          }



    def updateMenuSection(self,name=None):
      if name is not None:
        self.section_name = name
      self.set_number_of_groups()
      self.set_total_number_of_items()
    
    def updateAllMenus(self):
      menus = self.menu.all()
      for m in menus:
        m.updateMenu()
    
    def isPartOfSection(self,item):
      return self.section_items.filter(section_to_item.c.menuitem_id==item.id).count() > 0

    def getItems(self):
      return self.section_items.all()

    def addItem(self,item):
      if not self.isPartOfSection(item):
        self.section_items.append(item)
        self.updateMenuSection()
        self.updateAllMenus()
        return self

    def deleteItem(self,item):
      if self.isPartOfSection(item):
        self.section_items.remove(item)
        self.updateMenuSection()
        self.updateAllMenus()
        return self

    def getSubSections(self):
      return self.subsections.all()

    def addSubSection(self,section):
      if section not in self.subsections.all():
        self.subsections.append(section)
        self.updateMenuSection()
        self.updateAllMenus()
        return self

    def deleteSubSection(self,section):
      if section in self.subsections.all():
        self.subsections.remove(section)
        self.updateMenuSection()
        self.updateAllMenus()
        return self
    
    def set_number_of_groups(self):
      self.number_of_groups = self.subsections.count()
    
    def set_total_number_of_items(self):
      if self.number_of_groups > 0:
        total_combinations = 1
        for subsection in self.subsections.all():
          num = subsection.get_total_number_of_items()
          total_combinations *= num
        self.total_number_of_items = total_combinations
        return
      if self.section_items.count() >= 0:
        self.total_number_of_items = self.section_items.count()


    def get_total_number_of_items(self):
      return self.total_number_of_items

    def has_parents(self):
      return len(self.parentSection) != 0

    def __repr__(self):
      return '< MenuSection: %r , Number_of_groups: %r ,  Number_of_items: %r >' % (self.section_name,self.number_of_groups,self.total_number_of_items)


class MenuItem(db.Model):  
    __tablename__ = 'menuitem'
    #Items
    id = db.Column(db.Integer , primary_key=True)
    item_id=db.Column(db.String(64),index=True,unique=True)
    item_name = db.Column(db.String(64),unique=True)
    price = db.Column(db.Numeric(precision=2))
    short_description = db.Column(db.String(128))
    long_description = db.Column(db.String(256))
    availability = db.Column(db.Boolean())
    ingrediants = db.Column(db.String(256))
    allergens = db.Column(db.String(256))

    #Relations
    #many <-> many , orderItem <-> menuItem
    
    def __init__(self,item_id,item_name,price,sd,ld,a,i,al):
      self.updateItem(item_id,item_name,price,sd,ld,a,i,al)

    def serialize(self):
      return {
            'id' : self.id,
            'item_id' : self.item_id,
            'item_name' : self.item_name,
            'price' : str(self.price),
            'short_description' : self.short_description,
            'long_description' : self.long_description,
            'availability' : self.availability,
            'ingrediants' : self.ingrediants,
            'allergens' : self.allergens,
            'parent_section' : [s.id for s in self.section]
          }
    
    def short_serialize(self):
      return {
            'id' : self.id,
            'item_id' : self.item_id,
            'item_name' : self.item_name,
            'price' : str(self.price),
          }


    def updateItem(self,item_id,item_name,price,sd,ld,a,i,al):
      self.set_item_id(item_id)
      self.set_item_name(item_name)
      self.set_price(price)
      self.set_short_description(sd)
      self.set_long_description(ld)
      self.set_availability(a)
      self.set_ingrediants(i)
      self.set_allergens(al)

    def updateAllSections(self):
      sections = self.section.all()
      for section in sections:
        section.updateMenuSection()
        section.updateAllMenus()

    def set_item_id(self,item_id):
      self.item_id=item_id
    def get_item_id(self):
      return self.item_id
 
    def set_item_name(self,item_name):
      self.item_name = item_name
    def get_item_name(self):
      return self.item_name

    def set_price(self,price):
      self.price = price
    def get_price(self):
      return self.price

    def set_short_description(self,sd):
      self.short_description = sd
    def get_short_description(self):
      return self.short_description

    def set_long_description(self,ld):
      self.long_description = ld
    def get_long_description(self):
      return self.long_description

    def set_availability(self,a):
      self.availability = a
    def get_availability(self):
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


menuitem_to_orderitem = db.Table('menuitem_to_orderitem',
    db.Column('orderitem',db.Integer,db.ForeignKey('orderitem.id')),
    db.Column('menuitem',db.Integer,db.ForeignKey('menuitem.id'))
    )  


"""//////////////////////////////////////////////////////////////
                    ORDER DATABASE ITEMS
/////////////////////////////////////////////////////////////"""


class Order(db.Model):
    __tablename__ = 'order'
    #Fields
    id = db.Column(db.Integer , primary_key=True)
    table_number = db.Column(db.Integer(),index=True)
    number_of_customers = db.Column(db.Integer())

    current_number_of_items = db.Column(db.Integer())
    total_price = db.Column(db.Numeric(precision=2))
    currently_active = db.Column(db.Boolean())
    staggered_service = db.Column(db.Boolean())
    paid = db.Column(db.Boolean())
    time_arrived = db.Column(db.DateTime())
    time_finished = db.Column(db.DateTime())
    time_elapsed = db.Column(db.DateTime())

    #Relationship Fields
    #one -> many , orders -> orderItems
    order_items = db.relationship("OrderItem",backref='parentOrder',lazy='dynamic')
    #one -> many, orders -> orderCounter
    order_counter = db.Column(db.Integer,db.ForeignKey('ordercounter.id'))


    def __init__(self,table_number,number_of_customers):
      self.updateOrder(table_number=table_number,number_of_customers=number_of_customers)
      self.time_arrived = datetime.now()
      self.staggered_service = False
      self.currently_active = True
      self.paid = False
      if self.order_counter != None:
        self.daysorders.updateCounter()

    def updateOrder(self,table_number=None,number_of_customers=None,staggered_service=None):
      if staggered_service is not None:
        self.staggered_service = staggered_service
      if table_number is not None:
        self.table_number = table_number
      if number_of_customers is not None:
        self.number_of_customers = number_of_customers
      self.set_total_price()
      self.set_number_of_items()

    def get_order_items(self):
      return self.order_items.all()
      
    def add_order_item(self,item):
      self.order_items.append(item)
      self.updateOrder()
      return self
    
    def delete_order_item(self,item):
      if item in self.order_items.all():
        self.order_items.remove(item)
        self.updateOrder()
        return self

    def get_total_price(self):
      return self.total_price

    def set_total_price(self):
      total = 0
      for orderitem in self.order_items.all():
        total += orderitem.sub_price
      self.total_price = total

    def get_number_of_items(self):
      return self.current_number_of_items

    def set_number_of_items(self):
      total = 0
      for item in self.order_items.all():
        total += item.quantity
      self.current_number_of_items = total

    def pay(self):
      self.time_finished = datetime.now()
      self.time_elasped = self.time_finished - self.time_arrived
      self.currently_active = False
      self.paid = True
      if self.daysorders != None:
        self.daysorders.updateCounter()
      return self.total_price

    def __repr__(self):
      return "< Order %r , Table %r, Total Price %r >" % (self.id,self.table_number,self.total_price)

class OrderItem(db.Model):
    __tablename__ = 'orderitem'
    #Fields
    id = db.Column(db.Integer , primary_key=True)
    quantity = db.Column(db.Integer())
    sub_price = db.Column(db.Numeric(precision=2))
    
    #Relationship Fields
    order = db.Column(db.Integer,db.ForeignKey('order.id'))
    menu_items = db.relationship("MenuItem",secondary=menuitem_to_orderitem,
        backref="orders",lazy='dynamic')

    def __init__(self,item, quantity):
      self.updateItem(quantity)
      self.add_menu_item(item)
    
    def updateItem(self,quantity=None,additionalunits=None):
      if quantity is not None:
        self.quantity = quantity
      if additionalunits is not None:
        self.update_quantity(additionalunits)
      self.set_subPrice()

    def requiresAdditionSectionItems(self):
      s= self.menu_items.first().section
      if s == []:
        return False
      ms = s[0] #One Menu Item may belong to more than one section - THink about this
      if ms.parentSection == []:
        return False
      parentsSSections = ms.parentSection[0].subsections.all()
      counter = 0
      for s in parentsSSections:
        for mi in self.get_menu_items():
          if mi in s.getItems():
            counter += 1
          
      if counter == len(parentsSSections):
        return False
      
      return True
      

      c = s[0].number_of_groups
      return c <= self.menu_items.count()

    def get_menu_items(self):
      return self.menu_items.all()

    def add_menu_item(self,item):
      if item not in self.menu_items.all():
        self.menu_items.append(item)
        self.updateItem()
        return self

    def delete_menu_item(self,item):
      if item in self.menu_items.all():
        self.menu_items.remove(item)
        self.updateItem()
        return self
  
    def update_quantity(self,additionalUnits):
      self.quantity = self.quantity + additionalUnits

    def set_subPrice(self):
      itemPrice = 0
      for item in self.menu_items.all():
        itemPrice += item.price
      self.sub_price = itemPrice * self.quantity

    def get_subPrice(self):
      return self.sub_price

    def get_quantity(self):
      return self.quantity

    def __repr__(self):
      return '< OrderItem: %r >' % self.menu_items.first().item_id

class OrderCounter(db.Model):
    __tablename__='ordercounter'
    #Fields
    id = db.Column(db.Integer , primary_key=True)
    day = db.Column(db.Date)
    current_number_of_active_orders = db.Column(db.Integer)
    total_number_of_orders = db.Column(db.Integer)
    total_income = db.Column(db.Numeric(precision=2))
    
    #Relationship Fields
    orders = db.relationship("Order",backref='daysorders',lazy='dynamic')
    
    def __init__(self):
      self.day = datetime.now().date()
      self.updateCounter()


    def updateCounter(self):
      self.set_current_number_of_active_orders()
      self.total_number_of_orders = self.orders.count()
      self.update_income()

    def get_all_orders(self):
      return self.orders.all()

    def get_all_active_orders(self):
      return self.orders.filter(Order.currently_active).all()

    def add_order(self,order):
      if order not in self.orders.all():
        self.orders.append(order)
        self.updateCounter()

    def update_income(self):
      total = 0
      for order in self.orders.all():
        total += order.total_price
      self.total_income = total

    def get_current_number_of_active_orders(self):
      return self.current_number_of_active_orders

    def set_current_number_of_active_orders(self):
      if self.orders.all() == []:
        self.current_number_of_active_orders = 0
        return
      self.current_number_of_active_orders = self.orders.filter(Order.currently_active).count()
      
    
    def __repr__(self):
      return '< OrderCounter - Day: %r , Active Orders: %r Total Orders: %r >' % (self.day,self.current_number_of_active_orders,self.total_number_of_orders)


  
