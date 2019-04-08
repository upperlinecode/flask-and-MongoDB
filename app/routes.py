import os
from app import app
from flask import render_template, request, redirect, url_for, session # added url_for, session

import bcrypt # added for password encryption

# set some random secret key for session
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
@app.route('/index')

def index():
    collection = mongo.db.events
    events = collection.find({})

    message = ''
    if 'username' in session:
        message = 'You are logged in as ' + session['username'] + '.'

    return render_template('index.html', events = events, message = message)


# Sign up for MongoDB Atlas Account
# in Terminal: pip install flask-pymongo
# in Terminal: pip install dnspython (for +srv)
# in Terminal: pip install bcrypt (for password handling)
# Click on cluster name > Collections > Create Database (give database a name, give first collection a name - can be a dummy name)
# Create a user: From Overview, "Add New User" (can autogenerate a password, save the password somewhere: AtIHE3q3O8HKWBOc)

from flask_pymongo import PyMongo

app.config['MONGO_DBNAME'] = 'test-mongo' # name of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:AtIHE3q3O8HKWBOc@jeffreylancaster-kxrbn.mongodb.net/test-mongo?retryWrites=true' # Command Line Tools, Connect Instructions, Secure Database (Whitelist IP), connection method (Connect Your Application) > Copy > replace password w/ password
# same for node.js > 3.0 and Python > 3.6

mongo = PyMongo(app)

# check for connection? (not sure)

# CONNECT TO DB

# @app.route('/add')

# def add():
#     user = mongo.db.users
#     user.insert({'name':'Alicia'})
#     return 'Added User!'

# Check collection for new user(s)


# NEW USER SIGN UP

@app.route('/signup', methods=['POST', 'GET'])

def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists! Try logging in.'

    return render_template('signup.html')

# can clear session cookie


# EXISTING USER LOGIN

@app.route('/login', methods=['POST'])

def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw((request.form['password']).encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'


# NEW EVENT

@app.route('/events/new', methods=['GET', 'POST'])

def new_event():
    if request.method == "GET":
        return render_template('new_event.html')
    else:
        user_name = request.form['user_name']
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        
        events = mongo.db.events
        events.insert({'event': event_name, 'date': event_date, 'user': user_name})
        return redirect('/')
