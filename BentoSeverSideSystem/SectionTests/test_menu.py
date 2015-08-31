import os
from config import basedir
from app import app,db
from app.models import Menu, MenuSection, MenuItem
from app.forms import CreateMenuForm, AddMenuSectionForm, AddMenuItemForm
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
  def createMenu(self,menu_name):
    self.app.get('/createMenu')
    return self.app.post('/createMenu' , data = dict(
      menuName = menu_name
      ),follow_redirects = True)

  def addSection(self,menuName, sectionName):
    self.app.get('/addMenuSection')
    return self.app.post('/addMenuSection', data = dict(
      menu = menuName,
      sectionName = sectionName,
      ),follow_redirects = True)


  """------------- Create Menu Form Tests---------"""
  def test_successfulCreateMenu(self):
    rv = self.createMenu('menu1')
    self.assertTrue('New Menu Created' in rv.data,"Menu did not go through")
    self.assertTrue(Menu.query.get(1).menu_name == 'menu1' ,"menu not added to database")
  
  def test_successfulAddSection(self):
    menuName = 'menu1'
    self.createMenu(menuName)
    rv = self.addSection(Menu.query.get(1).id,'new section')
    self.assertTrue('New Section added Successfully' in rv.data,"section did not get through")
    menu1 = Menu.query.get(1)
    self.assertTrue(menu1.menu_sections[0].section_name == 'new section',"section not added to database")


if __name__ == '__main__':
  unittest.main()
