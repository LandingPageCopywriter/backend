from flask import jsonify, session
import uuid

def hash_pass(passw):
    return bcrypt.generate_password_hash(passw).decode('utf-8')

def check_pass(presenedPassw, savedPasswHash):
    return bcrypt.check_password_hash(savedPasswHash, presenedPassw) 

class User:
    def isLoggedIn(self):
        return 'logged_in' in session

    def start_session(self):
        session['logged_in'] = True
        return '{"success": "Session started!"}', 200

    def register(self, email, password):
        user = {
            "_id": uuid.uuid4().hex,
            "email": email,
            "password": hash_pass(password),
        }

        if db.users.find_one({"email": email}):
            return jsonify({"error": "User with email already exists!"}), 400

        if db.users.insert_one(user):
            return self.start_session()

        return jsonify({"error": "Registration failed!"}), 400
    
    def login(self, email, presentedPass):
        user = db.users.find_one({"email": email})
        if user and check_pass(presentedPass, user['password']):
            return self.start_session()

        return jsonify({"error": "Invalid login credentials!"}), 401

    def logout(self):
        session.clear()

from app import bcrypt, db