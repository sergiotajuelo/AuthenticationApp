from flask import Flask
from app import app
from user.models import User

@app.route('/user/register', methods=['POST'])
def register():
    return User().register()

@app.route('/user/login', methods=['POST'])
def login():
    return User().login()

@app.route('/user/signout')
def signout():
    return User().signout()
