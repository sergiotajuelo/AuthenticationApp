from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid, re

class User:

    def start_session(self, user):
        session['logged-in'] = True
        session['user'] = user
        return jsonify(user), 200

    def register(self):
        print(request.form)

        # Create the object with JSON format
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
            "remember": True if request.form.get('remember_me') else False
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        # Check if email and password are valid
        if self.check_email(user['email']) is False:
            return jsonify({"error": "Email is not valid."}), 400
        
        elif self.check_password(user['password']) is False:
            return jsonify({"error": "Password is not valid."}), 400

        # Check if any field is empty
        elif (len(user["email"]) == 0) or (len(user["name"]) == 0) or (len(user["password"]) == 0):
            return jsonify({"error": "Fields must not be empty!"}), 400

        # Check for existing email address
        elif db.users.find_one({ "email": user['email'] }):
            return jsonify({"error": "Email address already in use."}), 400
        
        elif db.users.insert_one(user):
            return self.start_session(user)
        
        return jsonify({"error": "Signup failed!"}), 400
    
    def login(self):
        print(request.form)

        user = db.users.find_one({ "email": request.form.get('email')})

        # Check if any field is empty
        if (len(request.form.get('email')) == 0) or (len(request.form.get('password')) == 0):
            return jsonify({"error": "Fields must not be empty!"}), 400
        
        # Check if the object exists
        elif user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)
        
        
        return jsonify({"error": "Invalid login credentials"}), 400
        
    def signout(self):
        session.clear()
        return redirect('/')
    
    def check_email(self, email):
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return True
        else:
            return False
        
    def check_password(self, password):
        if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', password):
            return True
        else:
            return False
    