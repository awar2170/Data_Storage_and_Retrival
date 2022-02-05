#Set Up the Flask Weather App 
# Import Dependences 

import datetime as dt 
import numpy as np 
import pandas as pd 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify 
# You want to import flask after your SQLAlchemy Dependencies 

#### Set Up the Database #### 
engine = create_engine("sqlite:///hawaii.sqlite") # This connects to our database 

Base = automap_base()
# This reflects teh database into our classes.
# I don't know what this means 
#### QUESTION #### https://docs.sqlalchemy.org/en/14/orm/extensions/automap.html
# schema = the layout of the table; what is a primary key; how the table is built 
# table = the dataframe  

# Reflect your code into the database: 
Base.prepare(engine, reflect=True)
# Now we can save our references to each table 

Measurement = Base.classes.measurement 
Station = Base.classes.station 

# create a session link 
session = Session(engine)

#### Set Up Flask #### 
app = Flask(__name__)
# The __name__ variable is a special variable in python. __name__ is replaced by the name of the file
# For example, __name__ right now is called "app", but if the file was named "example.py", then __name__ would hold the value "example"

#### Create the Welcome Route #### 
# First: Define what our route will be
# We want welcome route to be the root, which is basically the homepage 

## IMPORTANT NOTE: ALL ROUTES SHOULD GO AFTER THE APP=FLASK(__NAME__) LINE OF CODE 

@app.route("/") # This is the welcome root, it's the first route 
# We now want routing infomration for each of the other routes 
#First: Create a function with a return statement 
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API! <br/>
    Available Routes: <br/>
    /api/v1.0/precipitation <br/>
    /api/v1.0/stations <br/>
    /api/v1.0/tobs <br/>
    /api/v1.0/temp/start/end <br/>
    ''') # Ask on thursday why I can't get this to be separate lines
# Treat this as HTML(the string), not python 

#### Precipitation Route #### 
@app.route("/api/v1.0/precipitation")

def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# The code above defines a function precipitation(): 
    # This calculates the date one year ago from the most recent date in the database 
        # This querys the date and precipitation from the Measurement table 
    # This creates a dictionary that has the date and the percipiation 
    # Returns the precip variable in a json format

#### Stations Route #### 
@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# This code above defines the app.route for stations 
    # the results object allows us to get all the stations in our databse 
    # This stations variable puts our results into a 1D array, then into a list 
    # We then return the information as a json object

#### Monthly Tempearture Route #### 
@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# This code creates a new app.route called temp_monthly() 
    # This finds the previous year, based on 8/23/2017
    # This queries the results on the Measurement table, for tobs 
        # Thie filters teh query for the specific measurement station 
        # Further filters for teh dat to be greater than the previous year (so it's onl getting the things from the last year total)
    # THis makes a list of the results from teh query 
    # This returns the list in a json format

#### Statistics Route #### 
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

# This defines a new app route called stats: 
    # The sel object querys and selects the min, max and average from our SQLite databse 
    # if not end 
        # Query the database for the list we just made, then unravel the results into a one d array, then make it a list 
    # Results gets the stats data 
