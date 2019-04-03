import os
from app import app
from flask import render_template, request, redirect

events = [{"event_name":"Guitar Recital", "event_date":"2019-15-04"},
    {"event_name":"Poetry Slam Competition", "event_date":"2019-04-05"},
    {"event_name":"Community Board Meeting", "event_date":"2019-23-06"}]

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
        # new_event = dict(request.form)
        new_event = request.form.to_dict()
        events.append(new_event)
        return redirect('/')
