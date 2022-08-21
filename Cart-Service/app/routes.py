from crypt import methods
import imp
from itertools import product
import json
from math import prod
from unittest import result
from urllib import response
from app import app, db
from app.models import Cart, CartItems
from flask import Flask, request, jsonify, make_response, Response, send_from_directory
from sqlalchemy import literal_column, func, desc, select


@app.route('/user/<user_id>/cart', methods=['POST'])
def create_admin(user_id):

    app.logger.info('create_cart')
    new_cart = Cart(public_id=user_id, total = 0)
    print(new_cart)
    db.session.add(new_cart)
    db.session.commit()
    return jsonify({'message': 'Cart created!'}), 201


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():

    app.logger.info('add_to_cart')
    data = request.get_json()
    cart = Cart.query.filter(Cart.public_id == data['public_id']).first()
    print(cart)
    cart_item = CartItems(cart_id=cart.id, product_id=data['product_id'], quantity=data['quantity'])
    db.session.add(cart_item)
    db.session.commit()
    return jsonify({'message' : 'Product has been added to the cart'})
    