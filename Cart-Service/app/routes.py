from crypt import methods
import imp
from itertools import product
import json
from config import Config
from math import prod
from unittest import result
from urllib import response
from app import app, db
from app.models import Cart, CartItems, UserOrder
from flask import Flask, request, jsonify, make_response, Response, send_from_directory
from sqlalchemy import literal_column, func, desc, select


@app.route('/user/<user_id>/cart', methods=['POST'])
def create_admin(user_id):

    app.logger.info('create_cart')
    new_cart = Cart(public_id=user_id, total=0)
    db.session.add(new_cart)
    db.session.commit()
    return jsonify({'message': 'Cart created!'}), 201


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():

    app.logger.info('add_to_cart')
    data = request.get_json()
    cart = Cart.query.filter(Cart.public_id == data['public_id']).first()
    cart.total = cart.total + int(data['quantity'])*int(data['price'])
    cart_item = CartItems(
        cart_id=cart.id, product_id=data['product_id'], quantity=data['quantity'])
    db.session.add(cart_item)
    db.session.commit()
    return jsonify({'message': 'Product has been added to the cart'})


@app.route('/checkout/<user_id>', methods=['POST'])
def checkout(user_id):

    app.logger.info('checkout')
    cart = Cart.query.filter(Cart.public_id == user_id).first()
    if cart.total > 1000 and cart.total < 2500:
        value = cart.total-(cart.total*Config.discounts["DISCOUNT5"])
    if cart.total > 2500:
        value = cart.total-(cart.total*Config.discounts["DISCOUNT10"])
    new_order = UserOrder(public_id=user_id, total=value)
    db.session.add(new_order)
    db.session.commit()
    cart.total = 0
    db.session.commit()
    return jsonify({'message': 'Order has been placed'})


@app.route('/orders', methods=['GET'])
def orders():

    app.logger.info('orders')
    Orders = UserOrder.query.all()

    output = []

    for order in Orders:
        order_data = {}
        order_data['id'] = order.id
        order_data['public_id'] = order.public_id
        order_data['total'] = order.total
        order_data['timestamp'] = order.timestamp
        output.append(order_data)

    response = jsonify({'Orders': output})
    return response
