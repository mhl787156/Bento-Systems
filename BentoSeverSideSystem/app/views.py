from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import SignupForm,SigninForm
from .models import User


"""---------------  MENU METHODS -----------------------------------"""







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
      flash("This is Your User ID: %s\nYou Must Remember this and use it to Log In from now on")
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
      return redirect(request.args.get('next') or url_for('profile'))
    
    #Unsuccessful Login
    else:
      form.employee_id.errors.append("Invalid ID or password")

  return render_template('login.html', title = 'login',form=form)


@app.route('/removeUser')
@login_required
def removeUser():
  users = g.user 
  db.session.delete(user)
  db.session.commit()
  return redirect(url_for('signout'))

@app.route('/signout')
@login_required
def signout():
  logout_user()
  return redirect(url_for('login'))
