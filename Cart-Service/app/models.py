from enum import unique
from itertools import product
from app import db
import sqlalchemy
from sqlalchemy.orm import relationship


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    total = db.Column(db.Integer)
    items = db.relationship('CartItems', backref='cart')


class CartItems(db.Model):
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), primary_key=True)
    product_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)