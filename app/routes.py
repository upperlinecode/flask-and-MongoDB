import os
from app import app
from flask import render_template, request, redirect
import pyrebase


events = [{"event_name":"Guitar Recital", "event_date":"4/15/2019"},
    {"event_name":"Poetry Slam Competition", "event_date":"5/4/2019"},
    {"event_name":"Community Board Meeting", "event_date":"6/23/2019"}]

config = {
  "apiKey": os.environ['FIREBASE_APIKEY'],
  "authDomain": "community-event-manager.firebaseapp.com",
  "databaseURL": "https://community-event-manager.firebaseio.com",
  "projectId": "community-event-manager",
  "storageBucket": "community-event-manager.appspot.com",
  "serviceAccount": "app/firebase-private-key.json",
  "messagingSenderId": "1052538486567"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html', events = events)

# NEW EVENT

@app.route('/events/new', methods=['GET', 'POST'])

def new_event():
    if request.method == "GET":
        return render_template('new_event.html')
    else:
        new_event = dict(request.form)
        events.append(new_event)
        return redirect('/')
