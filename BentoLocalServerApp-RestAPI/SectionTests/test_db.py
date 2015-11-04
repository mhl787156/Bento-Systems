import os
from config import basedir
from app import app,db
from app.models import Menu, MenuSection, MenuItem, OrderItem,Order,OrderCounter
from SectionTests import test_set_up
from datetime import datetime

class DBTestCases(test_set_up.AbstractTestCases):
  
  def setUp(self):
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'SectionTests/test.db')
    self.app = app.test_client()
    db.create_all()


  """--------------Helper Functions --------------"""
  def buildMenu(self,numSections,numItems,menu):
    for n in range(numSections):
      s_n = menu.menu_name + str(n)
      s = MenuSection(s_n,True,2)
      db.session.add(s)
      self.buildSection(numItems,s)
      menu.addSection(s)
    db.session.commit()
    return menu
  
  def buildMenuwithSubSections(self,numSectionsOnly,numSectionsWithSubSections,
                          numSubSections,numItems,menu):
    last_n = 0
    for n in range(numSectionsOnly):
      s_n = menu.menu_name + str(n)
      s = MenuSection(s_n,True,2)
      db.session.add(s)
      self.buildSection(numItems,s)
      menu.addSection(s)
      last_n = n
    db.session.commit()
 
    for n in range(last_n+1,numSectionsWithSubSections):
      s_n = menu.menu_name + str(n)
      s = MenuSection(s_n,True,2)
      db.session.add(s)
      self.buildSectionwithSubSection(numSubSections,numItems,s)
      menu.addSection(s)
    db.session.commit()
    return menu

  def buildSectionwithSubSection(self,numSubSections,numItems,section):
    for n in range(numSubSections):
      s_n = section.section_name + 'SUB' + str(n)
      s = MenuSection(s_n,True,2)
      db.session.add(s)
      self.buildSection(numItems,s)
      section.addSubSection(s)
    db.session.commit()
    return section

  def buildSection(self,numItems,section):
    for n in range(numItems):
      i_n = section.section_name + str(n)
      i = MenuItem(i_n,i_n,n,"","",True,"","")
      db.session.add(i)
      section.addItem(i)
    db.session.commit()
    return section

  def createFullMenu(self):
    m = Menu("m")     #Returns a menu 'm'
    db.session.add(m)
    db.session.commit()
    numSOnly = 4      #with this number of Item only Sections named 'm0','m1'...'m'+str(numSonly-1)
    numSwSS = 6       #and this number of SubSection only Sections 'm(numSonly)' ... 'm' + str(numSwSS-1)
    numSS = 3         #Sections with subsections each have numSS subsections
    numItems = 10     #Each end node section has numItems number of items named 'm00','m01'...'m010','m10','m11'...
    self.buildMenuwithSubSections(numSOnly,numSwSS,numSS,numItems,m)
    return m

  def getMenuItem(self,i_id):
    if Menu.query.all() == []:
      self.createFullMenu()
    mi = MenuItem.query.filter(MenuItem.item_name == i_id).first()
    return mi

  """------------- Order Database Tests -------"""
  def test_orderInit(self):
    t_n = 2
    num_c = 4
    o = Order(t_n,num_c,0)
    db.session.add(o)
    db.session.commit()
    o = Order.query.first()
    self.assertTrue(o.get_number_of_items() == 0)
    self.assertTrue(o.table_number == t_n)
    self.assertTrue(o.number_of_customers == 4)
    self.assertTrue(o.get_order_items() == [])
    self.assertTrue(o.get_total_price() == 0)

  def test_orderItemInit(self):
    i_id = 'm02'
    menuitem = self.getMenuItem(i_id)
    actualPrice = menuitem.price
    self.assertTrue(actualPrice == 2)
    q = 2
    oi = OrderItem(menuitem,q)
    db.session.add(oi)
    db.session.commit()
    oi = OrderItem.query.first()
    self.assertTrue(oi.get_quantity() == q)
    self.assertTrue(oi.menu_items.count() == 1)
    self.assertTrue(not oi.requiresAdditionSectionItems())  
    self.assertTrue(oi.get_menu_items()[0].item_id == i_id)
    self.assertTrue(oi.get_subPrice() == actualPrice*q)

  def test_orderCounterInit(self):
    oc = OrderCounter()
    db.session.add(oc)
    db.session.commit()
    oc = OrderCounter.query.first()
    self.assertTrue(oc.get_current_number_of_active_orders() == 0)
    self.assertTrue(oc.get_all_active_orders() == [])
    self.assertTrue(oc.get_all_orders() == [])
    self.assertTrue(oc.total_income == 0)
    self.assertTrue(oc.day == datetime.now().date())
    self.assertTrue(oc.orders.all() == [])

  def test_orderaddOrderItem(self):
    i_id1 = 'm00'
    i_id2 = 'm08'
    i_id3 = 'm5SUB00'
    i_id4 = 'm5SUB11'
    i_id5 = 'm5SUB20'
    mi1 = self.getMenuItem(i_id1)
    mi2 = self.getMenuItem(i_id2)
    mi3 = self.getMenuItem(i_id3)
    mi4 = self.getMenuItem(i_id4)
    mi5 = self.getMenuItem(i_id5)

    t_n = 2
    n_p = 4
    o = Order(t_n,n_p,0)
    db.session.add(o)

    oi1 = OrderItem(mi1,1)
    o.add_order_item(oi1)
    db.session.add(oi1)
    db.session.commit()
    o = Order.query.first()
    self.assertTrue(o.get_number_of_items() == 1)
    self.assertTrue(o.table_number == t_n)
    self.assertTrue(o.number_of_customers == n_p)
    self.assertTrue(o.get_order_items()[0] == oi1)
    self.assertTrue(o.get_total_price() == oi1.sub_price)
    self.assertTrue(o.currently_active == True)

    o.delete_order_item(oi1)
    db.session.commit()
    self.assertTrue(o.get_number_of_items() == 0)
    self.assertTrue(o.table_number == t_n)
    self.assertTrue(o.number_of_customers == n_p)
    self.assertTrue(o.get_order_items() == [])
    self.assertTrue(o.get_total_price() == 0)

    oi2 = OrderItem(mi2,2)
    db.session.add(oi2)
    o.add_order_item(oi1)
    o.add_order_item(oi2)
    db.session.commit()
    self.assertTrue(o.get_number_of_items() == 3,o.get_number_of_items())
    self.assertTrue(o.table_number == t_n)
    self.assertTrue(o.number_of_customers == n_p)
    self.assertTrue(oi1 in o.get_order_items() and oi2 in o.get_order_items(),o.get_order_items())
    self.assertTrue(o.get_total_price() == (oi1.sub_price + oi2.sub_price))
    self.assertTrue(o.currently_active == True)

    oi3 = OrderItem(mi3,1)
    db.session.add(oi3)
    db.session.commit()
    self.assertTrue(oi3.requiresAdditionSectionItems())
    oi3.add_menu_item(mi4)
    db.session.commit()
    self.assertTrue(oi3.requiresAdditionSectionItems())
    oi3.add_menu_item(mi5)
    db.session.commit()
    self.assertTrue(not oi3.requiresAdditionSectionItems())

    o.add_order_item(oi3)
    db.session.commit()
    self.assertTrue(o.get_number_of_items() == 4,o.get_number_of_items())
    self.assertTrue(o.table_number == t_n)
    self.assertTrue(o.number_of_customers == n_p)
    self.assertTrue(oi1 in o.get_order_items() 
                    and oi2 in o.get_order_items()
                    and oi3 in o.get_order_items()
                    ,o.get_order_items())
    self.assertTrue(o.get_total_price() == (oi1.sub_price + oi2.sub_price + oi3.sub_price))
    self.assertTrue(o.currently_active == True)

    final = o.pay()
    self.assertTrue(o.time_finished != None)
    self.assertTrue(not o.currently_active)
    self.assertTrue(o.paid)
    self.assertTrue(final == (oi1.sub_price + oi2.sub_price + oi3.sub_price))

  def test_orderCounteraddOrder(self):
    oc = OrderCounter()
    db.session.add(oc)
    db.session.commit()
    oc = OrderCounter.query.first()
    
    o1 = Order(4,4,0)
    o1.total_price = 10.50
    o2 = Order(2,2,0)
    o2.total_price = 20.50
    o3 = Order(3,3,0)
    o3.total_price = 15.75

    total = o1.total_price + o2.total_price + o3.total_price

    db.session.add(o1)
    db.session.add(o2)
    db.session.add(o3)
    db.session.commit()

    self.assertTrue(oc.get_current_number_of_active_orders() == 0)
    self.assertTrue(oc.get_all_active_orders() == [])
    self.assertTrue(oc.get_all_orders() == [])
    self.assertTrue(oc.total_income == 0)
    self.assertTrue(oc.day == datetime.now().date())
    self.assertTrue(oc.orders.all() == [])

    oc.add_order(o1)
    oc.add_order(o2)
    oc.add_order(o3)
    db.session.commit()

    self.assertTrue(oc.get_current_number_of_active_orders() == 3)
    self.assertTrue(oc.total_number_of_orders == 3)
    activeOrders = oc.get_all_active_orders()
    self.assertTrue(o1 in activeOrders and o2 in activeOrders and o3 in activeOrders)
    self.assertTrue(oc.total_income == total)
    self.assertTrue(o1 in oc.get_all_orders() and o2 in oc.get_all_orders() and o3 in oc.get_all_orders())
    o1.pay()
    db.session.commit()
    self.assertTrue(oc.get_current_number_of_active_orders() == 2)
    self.assertTrue(oc.total_number_of_orders == 3)
    activeOrders = oc.get_all_active_orders()
    self.assertTrue(o1 not in activeOrders and o2 in activeOrders and o3 in activeOrders)
    self.assertTrue(oc.total_income ==total)
    self.assertTrue(o1 in oc.get_all_orders() and o2 in oc.get_all_orders() and o3 in oc.get_all_orders())


  """------------- Menu Database Tests---------"""  
  def test_menuInit(self):
    menuName = 'menu1'
    m1 = Menu(menuName)
    db.session.add(m1)
    db.session.commit()
    m = Menu.query.get(1)
    self.assertTrue(m.menu_name == menuName
                    and m.get_total_number_of_sections() == 0
                    and m.get_total_number_of_items()  == 0
                    ,"Menu init error")
    

  def test_sectionInit(self):
    sectionName = 'section1'
    s1 = MenuSection(sectionName,True,1)
    db.session.add(s1)
    db.session.commit()
    s = MenuSection.query.get(1)
    self.assertTrue(s.section_name == sectionName)
    self.assertTrue(s.getItems() == [] and s.getSubSections() == [])
    self.assertTrue(s.visibility and s.staggered_service_order == 1)
    self.assertTrue(s.get_total_number_of_items() == 0 and s.number_of_groups == 0
                    , "Section init error")

  def test_itemInit(self):
    itemName = 'item1'
    i_id = '22'
    sd = "sd"
    ld = "long description"
    a = True
    ing = 'Some'
    al = 'Some More'
    i1 = MenuItem(i_id,itemName,0,sd,ld,a,ing,al)
    db.session.add(i1)
    db.session.commit()
    i = MenuItem.query.get(1)
    self.assertTrue(i.get_item_name() == itemName)
    self.assertTrue(i.get_item_id() == i_id)
    self.assertTrue(i.get_short_description() == sd)
    self.assertTrue(i.get_long_description() == ld)
    self.assertTrue(i.get_availability()
                    and i.get_ingrediants() == ing
                    and i.get_allergens() == al
                    , "Item init error")
    
  def test_sectionAddItem(self):
      sn = 's1'
      in1 = 'i1'
      p1 = 1.11
      in2 = 'i2'
      p2 = 2.22
      in3 = 'i3'
      p3 = 3.33
      
      s = MenuSection(sn,True,2)
      i1 = MenuItem(in1,in1,p1,"","",True,"","")
      i2 = MenuItem(in2,in2,p2,"","",True,"","")
      i3 = MenuItem(in3,in3,p3,"","",True,"","")

      db.session.add(s)
      db.session.add(i1)
      db.session.add(i2)
      db.session.add(i3)
      db.session.commit()

      s = MenuSection.query.get(1)
      self.assertTrue(s.section_name == sn , "Section add error")
      self.assertTrue(MenuItem.query.count() == 3, "Item add error")

      s.addItem(i1)
      db.session.commit()

      self.assertTrue(s.getItems()[0].item_name == in1, "Add single item to section error")

      s.deleteItem(i1)
      db.session.commit()
      self.assertTrue(s.getItems() == [], "Section delete item error")

      s.addItem(i1)
      s.addItem(i2)
      s.addItem(i3)
      db.session.commit()
      self.assertTrue(s.get_total_number_of_items() == 3,"setting total number of items fails")

      l = s.getItems()
      self.assertTrue(i1 in l and i2 in l and i3 in l,"testgetItems and index")
    
  def test_sectionAddSubSection(self):
      sn = 's'
      ssn1 = 'ss1'
      ss1_num_items = 3
      ssn2 = 'ss2'
      ss2_num_items = 5
      ssn3 = 'ss3'
      ss3_num_items = 7

      s = MenuSection(sn,True,2)
      ss1 = MenuSection(ssn1,False,0)
      ss2 = MenuSection(ssn2,False,0)
      ss3 = MenuSection(ssn3,False,0)

      db.session.add(s)
      db.session.add(ss1)
      db.session.add(ss2)
      db.session.add(ss3)

      self.assertTrue(s in MenuSection.query.all()
                      and ss1 in MenuSection.query.all()
                      and ss2 in MenuSection.query.all()
                      and ss3 in MenuSection.query.all()
                      , "section add to db error")
      
      self.buildSection(ss1_num_items,ss1)
      self.assertTrue(len(ss1.getItems()) == ss1_num_items,"item add error")
      
      s.addSubSection(ss1)
      db.session.commit()
      self.assertTrue(s.number_of_groups == 1)
      self.assertTrue(s.total_number_of_items == ss1_num_items)
      self.assertTrue(s.subsections.first().section_name == ssn1,"subsection add failure")

      s.deleteSubSection(ss1)
      db.session.commit()
      self.assertTrue(s.number_of_groups == 0
                      and s.total_number_of_items ==0
                      and s.subsections.all() == []
                      , "subsection remove failure")
      
      self.buildSection(ss2_num_items,ss2)
      self.buildSection(ss3_num_items,ss3)

      s.addSubSection(ss1)
      s.addSubSection(ss2)
      s.addSubSection(ss3)

      db.session.commit()
      self.assertTrue(s.number_of_groups == 3
                      and s.total_number_of_items == ss1_num_items * ss2_num_items *ss3_num_items
                      and s.subsections.count() == s.number_of_groups
                      ,"multi add subsection test failure")
    

  def test_menuAddSections(self):
        mn = 'menu1'
        numSections = 4
        numItems = 3
        numSubSections = 2

        mn = Menu(mn)
        db.session.add(mn)
        db.session.commit()

        self.buildMenu(numSections,numItems,mn)
        
        totalNumItems = numSections * numItems
        self.assertTrue(mn.get_total_number_of_sections() == 4
                        and mn.get_total_number_of_items() == totalNumItems
                        , "Menu add normal section failure")

        sec = mn.getSections()
        for s in sec:
          self.buildSectionwithSubSection(numSubSections,numItems,s)

        totalNumItems = numSections * (numItems**numSubSections)
        self.assertTrue(mn.get_total_number_of_sections() == 4
                        and mn.get_total_number_of_items() == totalNumItems
                        , "Menu add all Subsection'd sections failure")


  def test_sectionItemManyToMany(self):
          sn1 = 's1'
          sn2 = 's2'
          in1 = 'i1'

          s1 = MenuSection(sn1,True,2)
          s2 = MenuSection(sn2,True,2)
          i1 = MenuItem(in1,in1,10.00,"","",True,"","")

          db.session.add(s1)
          db.session.add(s2)
          db.session.commit()
          
          sq1 = MenuSection.query.filter(MenuSection.section_name==sn1).first()
          sq2 = MenuSection.query.filter(MenuSection.section_name==sn2).first()

          self.assertTrue(s1 == sq1 and s2 == sq2)

          sq1.addItem(i1)
          sq2.addItem(i1)

          db.session.commit()

          sq1 = MenuSection.query.filter(MenuSection.section_name == sn1).first()
          sq2 = MenuSection.query.filter(MenuSection.section_name == sn2).first()

          self.assertTrue(sq1.getItems()[0].item_name == in1
                          and sq2.getItems()[0].item_name == in1
                          , "add same item to multiplie sections error")

          i1 = sq1.getItems()[0]
          in1 = "some_other-name"
          i1.set_item_name(in1)
          db.session.commit()



          self.assertTrue(sq1.getItems()[0].item_name == in1,"item_name hasnt changed")
          self.assertTrue(sq2.getItems()[0].item_name == in1
                          , "add changed name to multiple sections error")



if __name__ == '__main__':
  unittest.main()
