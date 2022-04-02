from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User
from .. import db
from ..utils import generate_token, verify_token
import uuid

@auth.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        response = {}
        form = request.get_json()
        user = mongo.db.user
        uuid_obj = uuid.uuid4()
        check = user.find_one({"phone_number" : form['phone_number']})
        if check is not None:
            response['message'] = "Phone number has been already registered"
            return response
        user.insert_one({"user_id": uuid_obj.hex,"first_name":form['first_name'], "last_name":form['last_name'], "phone_number": form['phone_number'], "address":form['address'], "pin":form['pin']})
        balance = mongo.db.balance
        balance.insert_one({"top_up_id": uuid_obj.hex, "user_id": uuid_obj.hex, "amount":0})
        response['status'] = 'SUCCESS'
        response['result'] = form
        return response
    return "register"

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        response = {}
        form = request.get_json()
        user = mongo.db.user
        get_user = user.find_one({"phone_number" : form['phone_number'], "pin": form['pin']})
        if not get_user:
            response['message'] = "Phone number and pin doesn’t match."
            return response
        token = generate_token(get_user['user_id'])
        access = {"access_token" : token, "refresh_token" : token}
        response['status'] = 'SUCCESS'
        response['result'] = access
        return response
    return "login"

@auth.route('/profile', methods=['POST'])
def update_profile():
    if request.method == 'POST':
        response = {}
        form = request.get_json()
        header = request.headers['token']
        verify = verify_token(header)
        if not verify:
            response['message'] = "“Unauthenticated"
            return response
        user = mongo.db.user
        user.updateOne({'user_id': verify['user_id']}, {'$set': {'first_name': form['first_name'], 'last_name': form['last_name'], 'address': form['address']}})
        response['status'] = 'SUCCESS'
        return response
    return "test"
