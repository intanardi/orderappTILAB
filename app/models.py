from app import create_app, db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    phone_number = db.Column(db.String(128))
    address = db.Column(db.String(128))
    pin = db.Column(db.String(128))

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128))
    price = db.Column(db.Integer)
    