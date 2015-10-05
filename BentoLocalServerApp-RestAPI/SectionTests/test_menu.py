import os
from config import basedir
from app import app,db
from app.models import Menu, MenuSection, MenuItem
from SectionTests import test_set_up

class MenuTestCases(test_set_up.AbstractTestCases):
  
  def setUp(self):
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'SectionTests/test.db')
    self.app = app.test_client()
    db.create_all()

    self.signup('t1','t2','123456789',5,'dkj@ahsd.com','123')
    self.tryLogin('t1','t2','123')


  """--------------Helper Functions --------------"""
  def addMenu(self,menu_name):
    self.app.get('/addMenu')
    return self.app.post('/addMenu' , data = dict(
      menuName = menu_name
      ),follow_redirects = True)

  def addSection(self,sectionName,visibility,s_s_o):
    self.app.get('/addMenuSection')
    return self.app.post('/addMenuSection', data = dict(
      sectionName = sectionName,
      visibility=visibility,
      s_s_o=s_s_o
      ),follow_redirects = True)

  def addItem(self,item_id,itemName,price):
    self.app.get('/addMenuItem')
    return self.app.post('/addMenuItem' , data = dict(
      item_id = item_id,
      item_name = itemName,
      price=price
      ),follow_redirects = True)


  """------------- Create Menu Form Tests---------"""
  def test_addNewMenu(self):
    rv = self.addMenu('menu1')
    self.assertTrue('created' in rv.data,"Menu did not go through")
    self.assertTrue(Menu.query.count() == 1,"menu not added {}".format(Menu.query.count()))
    self.assertTrue(Menu.query.get(1).menu_name == 'menu1' ,"menu not added to database")
  
  def test_addNewSection(self):
    rv = self.addSection('new section',True,0)
    self.assertTrue('created' in rv.data,"section did not get through")
    self.assertTrue(MenuSection.query.get(1).section_name == 'new section',"section not added to database")
  
  def test_addNewItem(self):
    rv = self.addItem('011','item1',3.00)
    self.assertTrue('created' in rv.data,"item did not go through")
    self.assertTrue(MenuItem.query.get(1).item_name == 'item1',"item not added to database")
  
  def test_editMenuRemove(self):
    self.addMenu('menu1')
    menu = Menu.query.get(1)
    rv = self.app.get('/editMenu/{}/'.format(menu.id))
    self.assertTrue(Menu.query.count() != 0)
    rv = self.app.post('/editMenu/{}/'.format(menu.id),data=dict(
                        remove=True
                        ),follow_redirects=True)
    self.assertTrue(Menu.query.count() == 0)
    self.assertTrue(menu not in Menu.query.all())

  def test_editMenuAddRemoveSection(self):
    self.addMenu('m1')
    self.addSection('s1',True,0)
    self.addSection('s2',True,0)
    self.addSection('s3',True,0)
    menuDB = Menu.query.get(1)
    url = '/editMenu/{}/'.format(menuDB.id)
    self.app.get(url)
    s1DB = MenuSection.query.filter_by(section_name='s1').first()
    
    rv = self.app.post(url,data=dict(
                  addSectionSubmit=True,
                  sections = s1DB.id
                  ),follow_redirects=True)
    menuDB = Menu.query.get(1)
    self.assertTrue(s1DB.section_name ==  menuDB.menu_sections[0].section_name,"not actually added")
    self.assertTrue("Section {} successfully added to {}".format(s1DB.section_name,menuDB.menu_name) in rv.data,"Section not successfully added")
    
    s2DB = MenuSection.query.filter_by(section_name='s2').first()
    s3DB = MenuSection.query.filter_by(section_name='s3').first()

    rv = self.app.post(url,data=dict(
                  addSectionSubmit=True,
                  sections = s1DB.id
                  ),follow_redirects=True)
    self.assertTrue("Section {} already existed".format(s1DB.section_name) in rv.data,"Duplicate section check not working")

    rv = self.app.post(url,data=dict(
                  addSectionSubmit=True,
                  sections = s1DB.id
                  ),follow_redirects=True)
    rv = self.app.post(url,data=dict(
                  addSectionSubmit=True,
                  sections = s2DB.id
                  ),follow_redirects=True)
    rv = self.app.post(url,data=dict(
                  addSectionSubmit=True,
                  sections = s3DB.id
                  ),follow_redirects=True)
    menuDB = Menu.query.get(1) 
    self.assertTrue(menuDB.menu_sections.count() == 3,"Sections not added successfully")

    rv=self.app.post(url,data=dict(
                    rmSecSubmit=True,
                    removeSection = s1DB.id
                    ),follow_redirects=True)
    menuDB = Menu.query.get(1)
    self.assertTrue(menuDB.menu_sections.count() == 2,"Section not removed successfully")
    self.assertTrue("Section {} removed from {}".format(s1DB.section_name,menuDB.menu_name) in rv.data,"Remove Section not working")
    
    rv=self.app.post(url,data=dict(
                    rmSecSubmit=True,
                    removeSection = s1DB.id
                    ),follow_redirects=True)
    self.assertTrue("Section does not exist in this menu" in rv.data,"Remove Duplicate Section not working")
  
  def test_editMenuChangeName(self):
    self.addMenu('menu1')
    omenu = Menu.query.get(1)
    url = '/editMenu/{}/'.format(omenu.id)
    self.assertTrue(omenu.menu_name == 'menu1')
    self.app.get(url)
    rv = self.app.post(url,data=dict(
                      cnSubmit=True,
                      menuName='changedMenu1'
                      ),follow_redirects=True)
    nmenu = Menu.query.get(1)
    self.assertTrue(nmenu.menu_name != omenu.menu_name,"name not changed")
    self.assertTrue(nmenu.menu_name == 'changedmenu1')
    self.assertTrue("Menu {} has changed name to {}".format(omenu.menu_name,nmenu.menu_name) in rv.data,"did not flash success message")


  def test_editSectionRemove(self):
    self.addSection('section1',True,0)
    self.assertTrue(MenuSection.query.count() == 1,"Do not just have one item")
    ms = MenuSection.query.get(1)
    url = '/editMenuSection/{}'.format(ms.id)
    self.app.get(url)
    rv=self.app.post(url,data=dict(remove=True),follow_redirects = True)
    self.assertTrue(MenuSection.query.count()==0,"Did not remove")
    self.assertTrue("removed".format(ms.section_name) in rv.data,"message did not flash")
  
  
  def test_editSectionPP(self):
    self.addSection('s1',False,0)
    ms = MenuSection.query.get(1)
    url='/editMenuSection/{}'.format(ms.id)
    self.app.get(url)
    self.app.post(url,data=dict(
                 ppSubmit = True,
                 sectionName = 'cs1',
                 visibility = True,
                 s_s_o = 1
                 ),follow_redirects=True)
    nms = MenuSection.query.get(1)
    self.assertTrue(ms.section_name != nms.section_name,"Section name not changed")
    self.assertTrue(nms.section_name == 'cs1',"Name not changed")
    self.assertTrue(nms.visibility,"visibility not changed")
    self.assertTrue(nms.staggered_service_order == 1,"s_s_o not changed")
  
  def test_editSectionAddRemoveSubSection(self):
    self.addSection('s1',True,0)
    ms = MenuSection.query.get(1)
    url = '/editMenuSection/{}'.format(ms.id)
    self.addSection('ss1',True,0)
    self.addSection('ss2',True,0)
    ss1 = MenuSection.query.filter_by(section_name ='ss1').first()
    ss2 = MenuSection.query.filter_by(section_name = 'ss2').first()
    self.app.get(url)
    self.app.post(url,data = dict(
                 sssubmit=True,
                 subsection = ss1.id
                 ),follow_redirects=True)
    ms = MenuSection.query.get(1)
    self.assertTrue(ms.subsections.count() == 1,"subsection not added")
    self.assertTrue(ss1.section_name == ms.subsections[0].section_name,'wrong subsection added')

    self.app.post(url,data = dict(
                 sssubmit=True,
                 subsection = ss2.id
                 ),follow_redirects=True)

    ms = MenuSection.query.get(1)
    self.assertTrue(ms.subsections.count() == 2,"subsection not added")

    self.app.post(url,data = dict(
                 ssRmSubmit=True,
                 subsectionRemove = ss1.id
                 ),follow_redirects=True)
    
    ms = MenuSection.query.get(1)
    self.assertTrue(ms.subsections.count() == 1,"subsection not removed")
    self.assertTrue(ss1 not in ms.subsections,'subsection not removed')
    self.assertTrue(ss2.section_name == ms.subsections[0].section_name,'wrong subsection removed')
  
  def test_editSectionAddRemoveItem(self):
    self.addSection('s1',True,0)
    ms = MenuSection.query.get(1)
    url = '/editMenuSection/{}'.format(ms.id)
    self.addItem('i1','i1',10)
    self.addItem('i2','i2',15)
    i1 = MenuItem.query.filter_by(item_name='i1').first()
    i2 = MenuItem.query.filter_by(item_name='i2').first()
    self.app.get(url)
    self.app.post(url,data =dict(
                 itemsubmit =True,
                 items=i1.id
                 ),follow_redirects=True)
    ms = MenuSection.query.get(1)
    self.assertTrue(ms.section_items.count()==1,"nothing was added")
    self.app.post(url,data =dict(
                 itemsubmit =True,
                 items=i2.id
                 ),follow_redirects=True)
    ms = MenuSection.query.get(1)
    self.assertTrue(ms.section_items.count()==2,"2nd one wasnt added")
    self.app.post(url,data=dict(
                  itemRmSubmit=True,
                  itemRemove=i1.id
                  ),follow_redirects = True)
    ms = MenuSection.query.get(1)
    self.assertTrue(ms.section_items.count()==1,'item not removed')
  
  
  def test_editItemRemove(self):
    self.addItem('01','i1',10)
    mi = MenuItem.query.get(1)
    url = '/editMenuItem/{}/'.format(mi.id)
    self.app.get(url)
    self.app.post(url,data = dict(
                 remove = True
                 ),follow_redirects=True)
    self.assertTrue(MenuItem.query.count() == 0,'not removed')
    self.assertTrue(mi not in MenuItem.query.all(),'not removed')

  def test_editItemChangePP(self):
    self.addItem('01','i1',10)
    mi = MenuItem.query.get(1)
    url = '/editMenuItem/{}/'.format(mi.id)
    self.app.get(url)
    rv = self.app.post(url,data = dict(
                 ppItemSubmit = True,
                 item_id = '02',
                 item_name = 'i2',
                 price = 15,
                 short_description = 'Blah',
                 long_description = 'Blah blah',
                 availability = False,
                 ingrediants = 'ing',
                 allergens = 'all'
                 ),follow_redirects=True)
    self.assertTrue("database modified" in rv.data,"no flash message")
    nmi = MenuItem.query.get(1)
    self.assertTrue(mi.item_id != nmi.item_id,"id not changed")
    self.assertTrue(nmi.item_id == '02')
    self.assertTrue(nmi.item_name == 'i2')
    self.assertTrue(nmi.price == 15)
    self.assertTrue(nmi.short_description =='Blah')
    self.assertTrue(nmi.long_description == 'Blah blah')
    self.assertTrue(nmi.ingrediants == 'ing')
    self.assertTrue(nmi.allergens == 'all')

if __name__ == '__main__':
  unittest.main()
