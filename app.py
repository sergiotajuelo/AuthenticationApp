from flask import Flask, render_template, redirect, session
from functools import wraps
import pymongo

app = Flask(__name__)
app.secret_key = b'\n\xdc\xe6\n\x93g+P\x82\xb5]\xe9\xd8;\x1dO'

# Database
client = pymongo.MongoClient('localhost', 27017)
db = client.user_login_system

def login_required(f):
    @wraps(f)
    def wrap(*arg, **kwargs):
        #If user is logged in, it will redirect to the dashboard, otherwise will be redirected to home page.
        if 'logged-in' in session: 
            return f(*arg, **kwargs)
        else:
            return redirect('/')
        
    return wrap

# Routes
from user import routes

@app.route('/')
def home():
    return render_template('signup.html')

@app.route('/login')
def logIn():
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')