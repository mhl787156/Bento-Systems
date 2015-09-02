# Bento-Systems

1. Installing Api onto Sever

a) Go into BentoLocalServerApp-RestApi directory

b) Start up a command line interface and Install several things:
    i/ install python 2.7.* onto the server
    ii/ install virtualenv onto the server (package name: python-virtualenv)
    iii/ start a new virtual environment with:
            virtualenv flask
    iv/ then using the virtaul env version of pip (flask/bin/pip <module>) install the following
          flask
          flask-login
          flask-mail
          flask-sqlalchemy
          sqlalchemy-migrate
          flask-wooshalchemy
          flask-wtf
          flask-babel
          guess_language
          flipflop
          coverage
          flask-restful
          flask-httpauth
	
	Alternatively you can run the setup.sh inside the folder which should in theory work!
      ./setup.sh

c) in command line then start a new database by typing
      ./db_create.py

c) start server with ./run.py

2. Structure

  /BentoLocalServerApp-RestAPI
    
    /app
      -__init__.py

      /common
        -__init__.py
        -utils.py

      /resources
        # A set of http route implementations for RESTful API
        -__init__.py
        -orders.py

      /templates
        # Templates for the local server
        -lotsofdifferenttemplates.html
        -
                    .
                    .
                    .
                    
      -forms.py
          # A list of Form implementations for the local server
          +CreateMenuForm
          +SelectMenuForm
          +AddMenuSectionForm
          +AddMenuItemForm
          +SignupForm
          +editProfile
          +SigninForm

      -models.py
          # A list of Database Tables
          +User
          +Device
          +Menu
          +MenuSection
          +MenuItem
          +OrderCounter
          +OrderLogger
          +OrderItem

      -views.py
          # A list/implementation of the routes the local server app to take
      
      -routes.py
          # A list of the routes for the RESTful Api to take




    /sectionTests

    /db_repository

    /flask

    -config.py        # Configuration File
    -run.py           # Executable to run everything
    -unitTests.py     # Unit Tests
    -xmlunitTests.py  # Unit Tests with XML output
    
    (-db_*.py)
    -requirements.txt
    -setup.sh


