from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import SignupForm,SigninForm
from .models import User


@app.route('/')
@app.route('/index')
#@login_required
def index():
    if 'employee_id' not in session:
      return redirect(url_for('signin'))
    #If statement on clearance, 
    
       
    user = User.query.filter_by(employee_id = session['employee_id']).first()
    if user is None:
      return redirect(url_for('signin'))
    else:
      return render_template('index.html',
                           title='Index',
                           user=user)


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
      return redirect(url_for('profile'))
   
  elif request.method == 'GET':
    return render_template('signup.html', title = 'Signup' ,form=form)


  
@app.route('/profile')
def profile():
    if 'employee_id' not in session:
      return redirect(url_for('signin'))
    
    user = User.query.filter_by(employee_id = session['employee_id']).first()

    if user is None:
      return redirect(url_for('signin'))
    else:
      return render_template('profile.html', user = user , title=user.employee_id + "'s Profile")


      
@app.route('/editProfile')
def editProfile():
    #TODO
    return render_template('editProfile.html', title = 'Edit Profile', form = None)



@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', title = 'signin',form=form)
    else:
      session['employee_id'] = form.employee_id.data
      return redirect(url_for('profile'))
                 
  elif request.method == 'GET':
    return render_template('signin.html',title = 'signin', form=form)




@app.route('/signout')
def signout():
 
  if 'employee_id' not in session:
        redirect(url_for('signin'))
  
  session.pop('employee_id', None)
    
  return redirect(url_for('signin'))



