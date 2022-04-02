from datetime import datetime
from flask import render_template, session, redirect, request, jsonify
from . import main
from .. import db
from ..models import User, Product
from ..utils import generate_token, verify_token
import uuid

@main.route('/info', methods=['GET', 'POST'])
def info():
    response = {}
    if request.method == 'POST':
        response['status'] = 'HELLO'
        return response
    response['info'] = 'information'
    return "hello"

@main.route('/product', methods=['GET', 'POST'])
def product():
    response = []
    product = Product.query.all()
    for i in product:
        response.append({
                'name': i.name,
                'price': i.price,
            })
    return jsonify(response)

@main.route('/topup', methods=['GET', 'POST'])
def topup():
    if request.method == 'POST':
        response = {}
        form = request.get_json()
        header = request.headers['token']
        verify = verify_token(header)
        if not verify:
            response['message'] = "“Unauthenticated"
            return response
        uuid_obj = uuid.uuid4().hex
        balance = mongo.db.balance
        get_data = balance.aggregate([{ "$match" : {"user_id":verify['user_id']}}, {"$group":{"_id":"$amount", "total": {"$sum":"$amount"}}}])
        amount_before = list(get_data)[0]['total']
        response['balance_before'] = amount_before
        response['balance_after'] = int(amount_before) + int(form['amount'])
        balance.insert_one({"top_up_id": uuid_obj, "user_id": verify['user_id'], "amount":form['amount'],})
        response['status'] = 'SUCCEESS'
        return response
    return "hello"

@main.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        response = {}
        form = request.get_json()
        header = request.headers['token']
        verify = verify_token(header)
        if not verify:
            response['message'] = "“Unauthenticated"
            return response
        uuid_obj = uuid.uuid4().hex
        balance = mongo.db.balance
        get_data = balance.aggregate([{ "$match" : {"user_id":verify['user_id']}}, {"$group":{"_id":"$amount", "total": {"$sum":"$amount"}}}])
        # get_payment = balance.aggregate([{ "$match" : {"user_id":verify['user_id']}}, {"$group":{"_id":"$amount", "total": {"$sum":"$amount"}}}])
        current_balance = list(get_data)[0]['total']
        print(current_balance)
        if int(current_balance) < int(form['amount']):
            response['message'] = "Balance is not enough"
            return response
        payment = mongo.db.payment
        # print(current_balance)
        balance_after = int(current_balance) - int(form['amount'])
        result = {"payment_id": uuid_obj, "remarks": form['remarks'], "amount":form['amount'], "balance_before": current_balance, "balance_after": balance_after}
        payment.insert_one({"payment_id": uuid_obj, "user_id": verify['user_id'], "amount":form['amount']})
        response['result'] = result
        response['status'] = 'SUCCEESS'
        return response
    return "hello"