import imp
from itertools import product
import json
from math import prod
from unittest import result
from urllib import response
from app import app, db
from app.models import Product
from flask import Flask, request, jsonify, make_response, Response, send_from_directory
from sqlalchemy import literal_column, func, desc, select


@app.route('/product', methods=['POST'])
def create_product():

    app.logger.info('create_product')
    data = request.get_json()
    new_product = Product(product_name=data['product_name'], price=data['price'],
                          quantity=data['quantity'], category=data['category'], rating=None, no_of_ratings=None)
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': "Product added!"}), 201


@app.route('/products', methods=['GET'])
def get_all_products():

    app.logger.info('get_all_products')
    products = Product.query.all()

    output = []

    for product in products:
        product_data = {}
        product_data['id'] = product.id
        product_data['product_name'] = product.product_name
        product_data['price'] = product.price
        product_data['quantity'] = product.quantity
        product_data['category'] = product.category
        product_data['rating'] = product.rating
        product_data['no_of_ratings'] = product.no_of_ratings
        output.append(product_data)

    response = jsonify({'products': output})

    return response


@app.route('/products/category', methods=['GET'])
def get_product_by_category():

    app.logger.info('get_product_by_category')
    query = db.session.query(Product.category, func.group_concat(
        Product.product_name), func.group_concat(Product.quantity)).group_by(Product.category).all()
    results = {}
    for row in query:
        temp = {}
        product_list = row[1].split(",")
        price_list = row[2].split(",")
        for (product, price) in zip(product_list, price_list):
            temp[product] = price
        results[row[0]] = temp
    response = jsonify({'result': results})
    return response


# @app.route('/product/<product_id>/rating', methods=['PUT'])
# def add_rating(product_id):

#     app.logger.info('add_rating')
#     data = request.get_json()
#     product = Product.query.filter_by(product_id=Product.id).first()
#     # product.rating = (data["rating"] + (product.rating*product.no_pf_ratings))/(product.no_of_ratings+1)
#     product.no_of_ratings = product.no_of_ratings + 1
#     db.session.commit()

#     rresponse = jsonify({'message': 'The rating has been added!'})
#     return response, 202

@app.route('/product/<product_id>/rating', methods=['PUT'])
def add_rating(product_id):

    app.logger.info('add_rating')
    data = request.get_json()
    product = Product.query.get(product_id)
    product.rating = (data["rating"] + (Product.rating *
                      Product.no_of_ratings))/(Product.no_of_ratings + 1)
    product.no_of_ratings = Product.no_of_ratings + 1

    db.session.commit()

    return jsonify({'message': 'Rating has been added!'}), 202


@app.route('/products/price/increasing', methods=['GET'])
def sort_by_increasing_price():

    app.logger.info('sort_by_increasing_price')
    products = Product.query.order_by(Product.price).all()

    output = []

    for product in products:
        product_data = {}
        product_data['id'] = product.id
        product_data['product_name'] = product.product_name
        product_data['price'] = product.price
        product_data['quantity'] = product.quantity
        product_data['category'] = product.category
        product_data['rating'] = product.rating
        product_data['no_of_ratings'] = product.no_of_ratings
        output.append(product_data)

    response = jsonify({'products': output})

    return response


@app.route('/products/price/decreasing', methods=['GET'])
def sort_by_decreasing_price():

    app.logger.info('sort_by_decreasing_price')
    products = Product.query.order_by(Product.price.desc()).all()

    output = []

    for product in products:
        product_data = {}
        product_data['id'] = product.id
        product_data['product_name'] = product.product_name
        product_data['price'] = product.price
        product_data['quantity'] = product.quantity
        product_data['category'] = product.category
        product_data['rating'] = product.rating
        product_data['no_of_ratings'] = product.no_of_ratings
        output.append(product_data)

    response = jsonify({'products': output})

    return response

@app.route('/products/rating/decreasing', methods=['GET'])
def sort_by_rating():

    app.logger.info('sort_by_rating')
    products = Product.query.order_by(Product.rating.desc()).all()

    output = []

    for product in products:
        product_data = {}
        product_data['id'] = product.id
        product_data['product_name'] = product.product_name
        product_data['price'] = product.price
        product_data['quantity'] = product.quantity
        product_data['category'] = product.category
        product_data['rating'] = product.rating
        product_data['no_of_ratings'] = product.no_of_ratings
        output.append(product_data)

    response = jsonify({'products': output})

    return response

@app.route('/products/no_of_ratings/decreasing', methods=['GET'])
def sort_by_no_of_ratings():

    app.logger.info('sort_by_no_of_ratings')
    products = Product.query.order_by(Product.no_of_ratings.desc()).all()

    output = []

    for product in products:
        product_data = {}
        product_data['id'] = product.id
        product_data['product_name'] = product.product_name
        product_data['price'] = product.price
        product_data['quantity'] = product.quantity
        product_data['category'] = product.category
        product_data['rating'] = product.rating
        product_data['no_of_ratings'] = product.no_of_ratings
        output.append(product_data)

    response = jsonify({'products': output})

    return response
