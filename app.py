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
#### QUESTION #### 

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
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

#### Precipitation Route #### 

