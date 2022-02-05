from flask import Flask

#Create an app instance - or a singuar version of something 
app = Flask(__name__)

# The __name__ variable inside of the Flask function denotes the name of the current function 
# We can use __name__ to det if your code is being run from the command line or if it has been imported into another piece of code 
# Variables with underscores before and after them are called magic methods in Python 

#Create Flask Routes 
# We need to ID the starting point; the root 
@app.route('/') #This makes the base root for the app 

# Eric says it's normal to not know if your code is going to work until you run it in the terminal 

def hello_world(): 
    return 'Hello World'

# THe above code should have created the first Flask route
# Run a Flask App 
# You don't run Flask Apps like normal python files 
# You open powershell and navigate to your folder with the app and type "set FLASK_APP=app.py", run that line (nothing really happens), then type "flask run"
# You'll be given a url, put that into a new tab and search it 

# Set Up the Database and Flask
