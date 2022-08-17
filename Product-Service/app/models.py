from enum import unique
from unicodedata import category
from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(120), index=True, unique=True)
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    category = db.Column(db.String(50))
    rating = db.Column(db.Integer)
    no_of_ratings = db.Column(db.Integer)