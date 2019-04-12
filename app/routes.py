import os
from app import app
from flask import render_template, request, redirect
from flask_pymongo import PyMongo

# name of database
app.config['MONGO_DBNAME'] = 'database-name' 

# URI of database
app.config['MONGO_URI'] = 'mongo-uri' 

mongo = PyMongo(app)

# CONNECT TO DB

@app.route('/add')

def add():
    user = mongo.db.users
    user.insert({'name':'Your Name'})
    return 'Added User!'

# Check collection for new user(s)

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

# INDEX ROUTE

@app.route('/')
@app.route('/index')

def index():
    collection = mongo.db.events
    events = collection.find({})

    return render_template('index.html', events = events)


