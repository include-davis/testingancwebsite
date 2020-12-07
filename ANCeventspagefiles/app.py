from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
#from waitress import serve


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = '_5#y2L"F4Q8z\n\xec]/'
db = SQLAlchemy(app)

class Event(db.Model):
    eventname = db.Column(db.String(150), primary_key=True)
    datetime = db.Column(db.String(50))
    location = db.Column(db.String(50))
    host = db.Column(db.String(50))
    category = db.Column(db.String(50))
    description = db.Column(db.String(1250))
    link = db.Column(db.String(200))

def __init__(self, eventname, datetime, location, host, category, description, link):
   self.eventname = eventname
   self.datetime = datetime
   self.location = location
   self.host = host
   self.category = category
   self.description = description
   self.link = link

@app.route('/')
def show_all():
   return render_template('ANCeventspage.html', events = Event.query.all())

@app.route('/delete/<eventname>', methods = ['GET', 'POST'])
def verification_delete(eventname):
   if request.method == 'POST':
       if not request.form['passcode']:
           flash('Please enter the passcode', 'error')
       else:
            if request.form['passcode'] == app.config['SECRET_KEY']:
                return redirect(url_for(".delete", eventname=eventname))
            else:
                flash('Wrong passcode: Please check your spelling', 'error')
   return render_template('verification.html')

@app.route('/remove/<eventname>', methods = ['GET','POST'])
def delete(eventname):
    event = Event.query.filter_by(eventname=eventname).first()
    if event is None: 
        return f'Could not find event'
    db.session.delete(event)
    db.session.commit()
    return redirect("http://127.0.0.1:5000/", code=302)


@app.route('/new', methods = ['GET','POST'])
def verification_new():
    if request.method == 'POST':
       if not request.form['passcode']:
           flash('Please enter the passcode', 'error')
       else:
            if request.form['passcode'] == app.config['SECRET_KEY']:
                return redirect("http://127.0.0.1:5000/newevent", code=302)
            else:
                flash('Wrong passcode: Please check your spelling', 'error')
    return render_template('verification.html')

@app.route('/newevent', methods = ['GET','POST'])
def new():
    if request.method == 'POST':
        if not request.form['eventname'] or not request.form['datetime'] or not request.form['location'] or not request.form['host'] or not request.form['category'] or not request.form['description'] or not request.form['link']:
            flash('Please enter all the fields', 'error')
        else:
            event = Event(eventname=request.form['eventname'], datetime=request.form['datetime'], location=request.form['location'], host=request.form['host'], category=request.form['category'], description=request.form['description'], link=request.form['link'])
            db.session.add(event)
            db.session.commit() 
            flash('Record was successfully added')
            return redirect("http://127.0.0.1:5000/", code=302)
    return render_template('events.html')

from app import db
if __name__ == "__main__":
   db.create_all()
   app.run(debug = True, host='0.0.0.0')
   #serve(app, host='0.0.0.0')
"""cd flask"""
"""source bin/activate"""
"""flask run"""
"""sqlite3 db.sqlite3"""
"""select * from event;"""

