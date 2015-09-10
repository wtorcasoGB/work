#!/usr/bin/env python

# all the imports

import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

# configuration
SERVER_NAME="127.0.0.1:5001"
DATABASE = '/home/wtorcaso/work/hubway_flaskr/hubway_flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

if os.getenv("FLASKR_SETTINGS"):
    app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    print("connect_db() ENTRY.")
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        # BT question: why do this, when before_request() also opens the db?
        # why is it important to set g._database?
        db = g._database = connect_db()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def stations_list():
    """ get the list of station names, in order of 'id' """
    this_query = """select stations.name, count(docks.id) 
                    from stations, docks 
                    where docks.station = stations.id 
                    group by stations.id order by stations.id"""
    cursor = g.db.execute(this_query)
    result = [dict(name=row[0], docks=row[1]) for row in cursor.fetchall()]
    return result

@app.route('/')
def show_stations():
    stations = stations_list()
    print("stations:")
    for station in stations:
        print ("\t%r" % station) 

    this_query = """select stations.name as station,
                   "dock-" || docks.id as dock, 
                   "bike-" || bikes.id as bike
                    from stations, docks, bikes
                    where docks.station = stations.id
                    and bikes.dock = docks.id
                    union
                    select "in transit" as station_name, "---" as dock_name, "bike-"||bikes.id as bike
                    from bikes
                    where bikes.dock is NULL"""
    cursor = g.db.execute(this_query)
    bikes = [dict(station=row[0], dock=row[1], bike=row[2]) for row in cursor.fetchall()]
    ###print("bikes:")
    ###for bike in bikes:
        ###print ("\t%r" % bike) 

    return render_template('show_stations.html', stations=stations, bikes=bikes)

###@app.route('/')
###def index():
###    cur = get_db().cursor()

@app.route('/ride_choice', methods=['GET', 'POST'])
def ride_choice():
    print("ride_choice() ENTRY: method == %s" % request.method)
    print("\t%r" % request.form)

    if not session.get('logged_in'):
       abort(401)

    if request.method == 'POST':
        print("ride_choice() Doing POST")
        ride_from = request.form['ride_from']
        ride_to = request.form['ride_to']
        print("\tride_from == %r" % ride_from)
        print("\tride_to   == %r" % ride_to)
        return render_template('ride_action.html', 
                                ride_from=ride_from, 
                                ride_to=ride_to,
                                ride_result="Still Under Review")
    elif request.method == 'GET':
        # This is the first time through; a simple link does GET
        return render_template('ride_choice.html')
    else:
        print("Huhh? check the method in ride_choice")
        abort(401)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_stations'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_stations'))



def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def make_dicts(cursor, row):
    return dict((cur.description[idx][0], value)
                for idx, value in enumerate(row))

###db.row_factory = make_dicts

#####################################################################
if __name__ == '__main__':
    app.run()

