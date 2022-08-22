from enum import unique
from itertools import product
from app import db
import sqlalchemy
from datetime import datetime
from sqlalchemy.orm import relationship


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    total = db.Column(db.Integer)
    items = db.relationship('CartItems', backref='cart')


class CartItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

# class Order(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     public_id = db.Column(db.String(50))
#     total = db.Column(db.Integer)
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

class UserOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50))
    total = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)