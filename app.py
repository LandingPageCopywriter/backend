import json
from flask import Flask, jsonify, request, session
from sqlalchemy import true
from main_service import grab_content
from flask_cors import CORS
from models import User
from flask_bcrypt import Bcrypt
import pymongo
import redis

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = b'\x96\xb8\x84\xc7\xf8\xcf\x03\xe1\x1fC\xa1U0\xa1\x9e\xba'

bcrypt = Bcrypt(app)
client = pymongo.MongoClient('localhost', 27017)
db = client.landingpagecopy
redisDb = redis.Redis(host='localhost', port=6379, db=0)

def hasUsed():
    return redisDb.exists(str(request.remote_addr))

def assignUsageOfTheDay():
    redisDb.set(str(request.remote_addr), str(True), ex=86400)

@app.route("/is_loggedIn", methods=["GET"])
def is_loggedIn():
    return jsonify({'isLoggedIn': User().isLoggedIn()}), 200

@app.route("/logout", methods=["POST"])
def logout():
    User().logout()
    return 'Logged out', 200

@app.route("/register", methods=['POST'])
def register():
    email = request.form.get("email")
    password = request.form.get("password")
    checkout = request.args.get("checkout")

    # check for checkout sesh

    return User().register(email=email, password=password)

@app.route("/login", methods=["POST"])
def login():
    resp = request.get_json(force=True)
    email = resp['email']
    password = resp['password']
    
    return User().login(email, password)

@app.route("/", methods=['GET'])
def copywrite_my_landing_page():
    startup_name = request.args.get('startup_name')
    and_its = request.args.get('and_its')

    if startup_name == None or and_its == None:
        return '{"error": "Missing information!"}', 400

    if not startup_name.strip() or not and_its.strip():
        return '{"dull": "Empty result!"}', 200

    if not User().isLoggedIn():
        if hasUsed(): return '{"reached_max_usage": "Upgrade your account to have infinty usages of this app!"}'
        else: assignUsageOfTheDay()

    copywrite_result = grab_content(startup_name, and_its)

    return copywrite_result

if __name__ == "__main__":
    app.run(debug=True)