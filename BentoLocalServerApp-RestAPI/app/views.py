from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, api
from .forms import SelectItemForm,SelectSectionForm,SelectMenuForm,SignupForm,SigninForm,AddorEditMenuForm,AddorEditMenuSectionForm,AddorEditMenuItemForm
from .models import User,Menu,MenuSection,MenuItem

"""--------------- RESTFUL Routes ---------------------------------"""
from resources.order import OrderAPI, NewOrderAPI, OrderEditAPI
from resources.menu import MenuAPI,MenuItemAPI,MenuSectionAPI,GetMenuAPI

api.add_resource(GetMenuAPI,'/api/menu')
api.add_resource(MenuAPI,'/api/menu/<int:data>')
api.add_resource(MenuItemAPI,'/api/menuitem/<int:data>')
api.add_resource(MenuSectionAPI,'/api/menusection/<int:data>')

api.add_resource(NewOrderAPI,'/api/order/new_order')
api.add_resource(OrderAPI,'/api/order/<int:data>')
api.add_resource(OrderEditAPI,'/api/order/<int:data>/AddOrderItem')




"""--------------- MENU METHODS -----------------------------------"""
"""helpers"""
@app.route('/<path:url>/selectMenu/',methods=['GET','POST'])
@login_required
def selectMenu(url=None):
  form = SelectMenuForm()
  form.menu.choices = [(g.id,g.menu_name) for g in Menu.query.order_by('menu_name')]
  if request.method == 'POST':
    if form.validate():
      chosenMenuId = form.menu.data
      print url_for(url,data=chosenMenuId)
      return redirect(url_for(url,data=chosenMenuId))
    flash("validation failed")
  return render_template('selectMenu.html',title='Select a Menu',form=form,url=url)
   
@app.route('/<path:url>/selectSection/',methods=['GET','POST'])
@login_required
def selectSection(url=None):
  form = SelectSectionForm()
  form.publicSections.choices = [(g.id,g.section_name) for g in MenuSection.query.filter(MenuSection.visibility==True)]
  form.privateSections.choices = [(g.id,g.section_name) for g in MenuSection.query.filter(MenuSection.number_of_groups == 0)]
  if request.method == 'POST':
    if form.pubsubmit.data and form.publicSections.choices.data:
      return redirect(url_for(url,data=form.publicSections.data))
    if form.privsubmit.data and form.privateSections.data:
      return redirect(url_for(url,data=form.privateSections.data))
    flash("validation failed")
  return render_template('selectSection.html',title='Selectal a Section', form = form,url=url)
  
@app.route('/<path:url>/selectItem/',methods=['GET','POST'])
@login_required
def selectItem(url=None):
  form = SelectItemForm()
  form.item.choices = [(g.id,g.item_name) for g in MenuItem.query.order_by('item_name')]
  if request.method == 'POST':
    if form.validate():
      chosenItemId = form.item.data
      return redirect(url_for(url,data=chosenItemId))
    flash("validation failed")
  return render_template('selectItem.html',title = 'Select an Item',form=form,url=url)

"""mains"""
#DONE - Not Tested
@app.route('/addMenu',methods=['GET','POST'])
@login_required
def addMenu():
  form = AddorEditMenuForm()

  if request.method == 'POST':
    if not form.validate():
      flash("Validation failed")
      return render_template('createNewMenu.html',title='Create New Menu',form=form)

    newMenu = Menu(form.menuName.data)

    db.session.add(newMenu)
    db.session.commit()
    flash('Menu ' + form.menuName.data + ' has been created')
    return redirect(url_for('editMenu',data=newMenu.id))

  if request.method == 'GET':
    return render_template('createNewMenu.html',title='Create New Menu',form=form)

#DONE - Not Tested
@app.route('/editMenu/',methods=['GET'])
@app.route('/editMenu/<int:data>/',methods=['GET','POST'])
@login_required
def editMenu(data=None):
  menu_id = data
  
  if data == None:
    return redirect(url_for('selectMenu',url='editMenu'))

  form = AddorEditMenuForm()
  menu = Menu.query.get(menu_id)
  availSections = MenuSection.query.except_(menu.menu_sections)
  form.sections.choices = [(g.id,g.section_name) for g in availSections]
  form.removeSection.choices = [(g.id,g.section_name) for g in menu.menu_sections]

  if request.method == 'POST':

    if form.remove.data:
      for section in menu.getSections():
        menu.deleteSection(section)
      db.session.delete(menu)
      db.session.commit()
      flash("Menu '{}' has been removed".format(menu.menu_name))
      return redirect(url_for('index'))
   
    if form.cnSubmit.data and form.menuName.data:
      oname = menu.menu_name
      menu.updateMenu(menu_name = form.menuName.data)
      db.session.commit()
      flash("Menu {} has changed name to {}".format(oname,menu.menu_name))

    if form.rmSecSubmit.data and form.removeSection.data:
      sec = MenuSection.query.get(form.removeSection.data)
      if sec in menu.getSections():
        menu.deleteSection(sec)
        db.session.commit()
        flash("Section {} removed from {}".format(sec.section_name,menu.menu_name))
      else:
        flash("Section does not exist in this menu".format(sec.section_name))

    if form.addSectionSubmit.data and form.sections.data:
      sec = MenuSection.query.get(form.sections.data)
      if sec in menu.getSections():
        flash("Section {} already existed".format(sec.section_name))
      else:
        menu.addSection(sec)
        db.session.commit()
        flash("Section {} successfully added to {}".format(sec.section_name,menu.menu_name))
      
    return redirect(url_for('editMenu',data=data))
  
  form.menuName.data=menu.menu_name
  return render_template('editMenu.html',title='Edit a Menu',form=form,menu=menu)


#DONE - Not Tested
@app.route('/addMenuSection',methods=['GET','POST'])
@login_required
def addMenuSection():
  form = AddorEditMenuSectionForm()
  if request.method == 'POST':
    if not form.validate():
      flash("validation failed")
      return render_template('addNewMenuSection.html',title='Add New Menu Section',form=form)

    newMenuSection = MenuSection(form.sectionName.data,
                                 form.visibility.data,
                                 form.s_s_o.data)
    db.session.add(newMenuSection)
    db.session.commit()
    flash(form.sectionName.data + ' successfully created')
    return redirect(url_for('index'))

  if request.method == 'GET':
    return render_template('addNewMenuSection.html',title='Add New Menu Section',form=form)


@app.route('/editMenuSection',methods=['GET'])
@app.route('/editMenuSection/<int:data>',methods=['GET','POST'])
@login_required
def editMenuSection(data=None):
  section_id = data
  
  if data == None:
    return redirect(url_for('selectSection',url='editMenuSection'))
 
  form = AddorEditMenuSectionForm()
  section = MenuSection.query.get(section_id)
  availItems = MenuItem.query.except_(section.section_items)
  form.items.choices = [(g.id,g.item_name) for g in availItems]
  availSubSections = MenuSection.query.except_(section.subsections.union(MenuSection.query.filter_by(id=section_id)))
  form.subsection.choices = [(g.id,g.section_name) for g in availSubSections]
  form.subsectionRemove.choices=[(g.id,g.section_name) for g in section.subsections]
  form.itemRemove.choices=[(g.id,g.item_name) for g in section.section_items]

  if request.method == 'POST':

    if form.remove.data:
      for item in section.getItems():
        section.deleteItem(item)
      for s in section.getSubSections():
        section.deleteSubSection(s)
      db.session.delete(section)
      db.session.commit()
      flash("Section '{}' has been removed".format(section.section_name))
      return redirect(url_for('index'))
    
    if form.ppSubmit.data:
      oname = section.section_name
      section.updateMenuSection(name = form.sectionName.data)
      section.visibility = form.visibility.data
      section.staggered_service_order = form.s_s_o.data
      db.session.commit()
      flash("Section {} has changed name to {} and visibility {} and Staggered Service Order to {}".format(oname,section.section_name,section.visibility,section.staggered_service_order))
    
    if form.ssRmSubmit.data and form.subsectionRemove.data:
      ss=MenuSection.query.get(form.subsectionRemove.data)
      if ss in section.getSubSections():
        section.deleteSubSection(ss)
        db.session.commit()
        flash("SubSection {} successfully removed from {}".format(ss.section_name,section.section_name))
      else:
        flash("SubSection {} doesnt exist in this Section".format(ss.section_name))

    if form.itemRmSubmit.data and form.itemRemove.data:
      item = MenuItem.query.get(form.itemRemove.data)
      if item in section.getItems():
        section.deleteItem(item)
        db.session.commit()
        flash("Item {} successfully removed from {}".format(item.item_name,section.section_name))
      else:
        flash("Item {} doesnt exist in this Section.".format(item.item_name))
   
    
    if form.sssubmit.data and form.subsection.data:
      ss=MenuSection.query.get(form.subsection.data)
      if ss in section.getSubSections():
        flash("Section {} already existed".format(ss.section_name))
      else:
        section.addSubSection(ss)
        db.session.commit()
        flash("Section {} successfully added to {}".format(ss.section_name,section.section_name))
    
    if form.itemsubmit.data and form.items.data:
      item = MenuItem.query.get(form.items.data)
      if item in section.getItems():
        flash("Item {} already existed".format(item.item_name))
      else:
        section.addItem(item)
        db.session.commit()
        flash("Item {} successfully added to {}".format(item.item_name,section.section_name))
      
    return redirect(url_for("editMenuSection",data=data))
  
  form.sectionName.data=section.section_name
  form.visibility.data=section.visibility
  form.s_s_o.data = section.staggered_service_order
  return render_template('editMenuSection.html',title='Edit a Section',form=form,section=section)


@app.route('/addMenuItem',methods=['GET','POST'])
@login_required
def addMenuItem():
  form = AddorEditMenuItemForm()
  if request.method == 'POST':
    if form.validate()==False:
      return render_template('addNewMenuItem.html', title='Add New Menu Item',form=form)

    newMenuItem = MenuItem(form.item_id.data,
                           form.item_name.data,
                           form.price.data,
                           form.short_description.data,
                           form.long_description.data,
                           form.availability.data,
                           form.ingrediants.data,
                           form.allergens.data)
    
    db.session.add(newMenuItem)
    db.session.commit()

    flash(form.item_name.data + " created Successfully" )
    return redirect(url_for('index'))

  if request.method == 'GET':
    return render_template('addNewMenuItem.html' ,title='Add New Menu Item',form=form)


@app.route('/editMenuItem/',methods=['GET'])
@app.route('/editMenuItem/<int:data>/',methods=['GET','POST'])
@login_required
def editMenuItem(data=None):
  item_id = data
  if data==None:
    return redirect(url_for('selectItem',url='editMenuItem'))

  form = AddorEditMenuItemForm()
  item = MenuItem.query.get(item_id)
  
  if request.method == 'POST':
    
    if form.remove.data:
      db.session.delete(item)
      db.session.commit()
      flash(item.item_name + 'removed from Database')
      return redirect(url_for('index'))
    
    if form.ppItemSubmit.data:      
    
      item.updateItem(form.item_id.data,
                      form.item_name.data,
                      form.price.data,
                      form.short_description.data,
                      form.long_description.data,
                      form.availability.data,
                      form.ingrediants.data,
                      form.allergens.data)
      db.session.commit()
    
      flash(item.item_name + " successfully edited, database modified ")

    return render_template('editMenuItem.html',title='Edit Menu Item',form=form,item=item)

  form.item_id.data = item.item_id
  form.item_name.data = item.item_name
  form.price.data = item.price
  form.short_description.data = item.short_description
  form.long_description.data = item.long_description
  form.availability.data = item.availability
  form.ingrediants.data = item.ingrediants
  form.allergens.data = item.allergens
  return render_template('editMenuItem.html' ,title='Edit Menu Item',form=form,item=item)



@app.route('/displayMenu',methods=['GET','POST'])
@login_required
def displayMenus():
  form = SelectMenuForm()
  menu = Menu.query.get(1)
  form.menu.choices=[(g.id,g.menu_name) for g in Menu.query.order_by('menu_name')]
  
  if request.method == 'POST' and form.validate():
    menu = Menu.query.get(form.menu.data)
    return render_template('displayMenu.html',title='Display Menu: {}'.format(menu.menu_name),menu=menu,form=form)

  return render_template('displayMenu.html',title='Display Menu',menu=menu,form=form)


@app.route('/displayMenu/<menu_name>')
def displayMenu(menu_name):
  form=SelectMenuForm()
  form.menu.choices=[(g.id,g.menu_name) for g in Menu.query.order_by('menu_name')]
  menu=Menu.query.filter_by(menu_name = menu_name).first()
  form.menu.data = menu.id
  return render_template('displayMenu.html',
                          title = 'Display Menu: {}'.format(menu_name),
                          menu=menu,
                          form=form)


"""-------------------ORDERING METHODS ---------------------------------"""

#Ordering methods are note going to be part of the form based UI
#Ordering is to be done by the Restful API only for the time being

"""--------------- PERSONAL PAGES METHODS ------------------------------"""


@app.route('/')
@app.route('/index')
@login_required
def index():
  user = g.user
  return render_template('index.html',title='Index',user=user)

@app.route('/profile')
@login_required
def profile():    
    user = g.user    
    return render_template('profile.html', user = user , title=user.employee_id + "'s Profile")


      
@app.route('/editProfile')
@login_required
def editProfile():
    #TODO
    return render_template('editProfile.html', title = 'Edit Profile', form = None)
    
    

"""---------------------LOGIN/PASSWORD METHODS--------------------------"""

#Login/Password login methods
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', title = 'Signup',form=form)
    else:  
      newUser = User(form.firstname.data,
                     form.lastname.data,
                     form.mobile_number.data,
                     form.clearance.data,
                     form.email.data,
                     form.password.data)

      db.session.add(newUser)
      db.session.commit()
            
      session['employee_id'] = newUser.employee_id
      flash('Successful Signup')
      flash("This is Your User ID: %s \n You Must Remember this and use it to Log In from now on" % newUser.employee_id)
      return redirect(url_for('login'))
   
  elif request.method == 'GET':
    return render_template('signup.html', title = 'Signup' ,form=form)

@lm.user_loader
def load_user(id):
  return User.query.get(int(id))

@app.before_request
def before_request():
  g.user = current_user 
                 

@app.route('/login', methods=['GET', 'POST'])
def login():

  if g.user is not None and g.user.is_authenticated():
    return redirect(url_for('profile'))  

  form = SigninForm()
   
  if form.validate_on_submit():

    user = User.query.filter_by(employee_id = form.employee_id.data.lower()).first()
    
    #Successful Login 
    if user is not None and user.check_password(form.password.data):
      session ['employee_id'] = form.employee_id.data
      login_user(user)
      flash("Successful Login")
      return redirect(request.args.get('next') or url_for('profile'))
    
    #Unsuccessful Login
    else:
      flash("Unsuccessful Login")
      form.employee_id.errors.append("Invalid ID or password")

  return render_template('login.html', title = 'login',form=form)




@app.route('/removeUser')
@login_required
def removeUser():
  user = g.user 
  db.session.delete(user)
  db.session.commit()
  flash("Removed Successfully")
  return redirect(url_for('signout'))




@app.route('/signout')
@login_required
def signout():
  logout_user()
  flash("You were logged out")
  return redirect(url_for('login'))




