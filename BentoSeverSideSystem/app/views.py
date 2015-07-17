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
      return redirect(url_for('aftersignup'))
   
  elif request.method == 'GET':
    return render_template('signup.html', title = 'Signup' ,form=form)

@app.route('/aftersignup')
def afterSignup():
    if 'employee_id' not in session:
      return redirect(url_for('signin'))
  
    user = User.query.filter_by(employee_id = session['employee_id']).first()

    if user is None:
      return redirect(url_for('signin'))
    else: render_template('afterSignup.html',user=user,title = 'Details')
  
@app.route('/profile')
def profile():
    if 'employee_id' not in session:
      return redirect(url_for('signin'))
    
    user = User.query.filter_by(employee_id = session['employee_id']).first()

    if user is None:
      return redirect(url_for('signin'))
    else:
      return render_template('profile.html', user = user , title=user.employee_id + "'s Profile")


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





"""
OpenID Login Methods

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():

    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])

    return render_template('login.html', 
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@oid.after_login
def after_login(resp):

    user = User.query.filter_by(email=resp.email).first()

    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()

    remember_me = False

    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)

    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.before_request
def before_request():
    g.user = current_user

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
"""


