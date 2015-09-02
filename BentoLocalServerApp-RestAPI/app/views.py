from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import SignupForm,SigninForm,CreateMenuForm,AddMenuSectionForm,AddMenuItemForm
from .models import User,Menu,MenuSection,MenuItem


"""---------------  MENU METHODS -----------------------------------"""

@app.route('/createMenu',methods=['GET','POST'])
@login_required
def createMenu():
  form = CreateMenuForm()

  if request.method == 'POST':
    if not form.validate_on_submit():
      flash("Validation failed")
      return render_template('createNewMenu.html',title='Create New Menu',form=form)

    newMenu = Menu(form.menuName.data)

    db.session.add(newMenu)
    db.session.commit()
    flash('New Menu Created')
  
  #Redirect to menu display page so user can view menu
    return redirect(url_for('displayMenu'))

  if request.method == 'GET':
    return render_template('createNewMenu.html',title='Create New Menu',form=form)


@app.route('/addMenuSection',methods=['GET','POST'])
@login_required
def addMenuSection():
  form = AddMenuSectionForm()
  form.menu.choices=[(g.id,g.menu_name) for g in Menu.query.order_by('menu_name')]
  print form.menu.choices

  if request.method == 'POST':
    if not form.validate_on_submit():
      print "form not validated: menu.data=%r  , sectionName.data=%r" %(form.menu.data,form.sectionName.data)
      flash("validation failed")
      return render_template('addNewMenuSection.html',title='Add New Menu Section',form=form)

    newMenuSection = MenuSection(form.sectionName.data)

    chosenmenu = Menu.query.get(form.menu.data)
    chosenmenu.menu_sections.append(newMenuSection)
    chosenmenu.updateMenu()

    db.session.add(newMenuSection)
    db.session.commit()

    flash("New Section added Successfully")
    return redirect(url_for('displayMenu'))

  if request.method == 'GET':
    return render_template('addNewMenuSection.html',title='Add New Menu Section',form=form)



#TODO - TEST
@app.route('/addMenuItem',methods=['GET','POST'])
@login_required
def addMenuItem():
  form = AddMenuItemForm()
  form.menu.choices=[(g.id,g.menu_name) for g in Menu.query.order_by('menu_name')]
  form.section.choices=[]

  if request.method == 'POST':
    if form.menu.data and not form.section.data:
      chosenMenu = Menu.query.get(form.menu.data)
      form.section.choices=[(g.id,g.section_name) for g in chosenMenu.menu_sections.order_by('section_name')]
      return render_template('addNewMenuItem.html',title='Add New Menu Item',form=form)
    if form.validate()==False:
      return render_template('addNewMenuItem.html', title='Add New Menu Item',form=form)

    newMenuItem = None #MenuItem('yadayadayadayada')
    
    chosenMenu = Menu.query.get(form.menu.data)
    chosenSection = MenuSection.query.get(form.section.data)
    chosenSection.section_items.append(newMenuItem)
    chosenMenu.updateMenu()

    db.session.add(newMenuItem)
    db.session.commit()

    flash("New Item added Successfully")
    return redirect(url_for('displayMenu'))

  if request.method == 'GET':
    return render_template('addNewMenuItem.html' ,title='Add New Menu Item',form=form)



@app.route('/editMenu',methods=['Get','Post'])
@login_required
def editMenu():
  #TODO
  return


@app.route('/editMenuSection',methods=['Get','Post'])
@login_required
def editMenuSection():
  #TODO
  return



@app.route('/editMenuItem',methods=['GET','POST'])
@login_required
def editMenuItem():
  #TODO
  return



@app.route('/displayMenu')
@login_required
def displayMenu():
  #TODO
  return render_template('displayMenu.html')

"""-------------------ORDERING METHODS ---------------------------------"""





"""--------------- PERSONAL PAGES METHODS ------------------------------"""


@app.route('/')
@app.route('/index')
@login_required
def index():
  user = g.user
  return render_template('index.html',
                           title='Index',
                           user=user)

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




