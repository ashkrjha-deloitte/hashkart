from crypt import methods
from curses.ascii import CAN
from app import app, db
from app.models import User
from flask import Flask, request, jsonify, make_response, Response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import uuid
import jwt
import datetime
import requests


CAN_NOT_PERFORM = "Can not perform that function!"
NO_USER_FOUND = "No user found!"


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            app.logger.error('Token is missing!')
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(
                public_id=data['public_id']).first()
        except Exception:
            app.logger.error('Token is invalid!')
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/admin', methods=['POST'])
def create_admin():

    app.logger.info('create_admin')
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_id = str(uuid.uuid4())
    new_user = User(public_id=new_id, username=data['username'],  email=data['email'], name=data['name'], password=hashed_password, admin=True)
    db.session.add(new_user)
    db.session.commit()
    requests.post('http://127.0.0.1:5002/user/' + new_id + '/cart')
    return jsonify({'message': 'Admin created!'}), 201


@app.route('/register', methods=['POST'])
def register_user():

    app.logger.info('register_user')
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_id = str(uuid.uuid4())
    print(new_id)
    new_user = User(public_id=new_id, username=data['username'],  email=data['email'], name=data['name'], password=hashed_password, admin=False)
    print(new_user)
    db.session.add(new_user)
    db.session.commit()
    requests.post('http://127.0.0.1:5002/user/' + new_id + '/cart')
    response = jsonify({'message': 'New user created!'}), 201
    return response


@app.route('/login', methods=['POST'])
def login():

    app.logger.info('login')
    auth = request.authorization
    username = auth.username
    password = auth.password
    response = None
    if not username or not password:
        app.logger.error('Could not verify, Incorrect username or password')
        response = make_response('Could not verify, Incorrect username or password', 401, {
                                 'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=username).first()

    if not user:
        app.logger.error('Could not verify')
        response = make_response('Could not verify', 401, {
                                 'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=120)}, app.config['SECRET_KEY'])

        response = jsonify({'token': token.decode('UTF-8')})

    return response


@app.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):

    app.logger.info('get_all_users')
    if not current_user.admin:
        app.logger.error(CAN_NOT_PERFORM)
        return jsonify({'message': CAN_NOT_PERFORM})

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['name'] = user.name
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    response = jsonify({'users': output})
    return response


@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):

    app.logger.info('get_one_user')
    if not current_user.admin:
        return jsonify({'message': CAN_NOT_PERFORM}), 401

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': NO_USER_FOUND}), 404

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['email'] = user.email
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user': user_data})


@app.route('/create_user', methods=['POST'])
@token_required
def create_user(current_user):

    app.logger.info('create_user')
    if not current_user.admin:
        app.logger.error(CAN_NOT_PERFORM)
        return jsonify({'message': CAN_NOT_PERFORM}), 401

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4(
    )), username=data['username'],  email=data['email'], name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'}), 201


@app.route('/currentuser', methods=['GET'])
@token_required
def get_user(current_user):

    app.logger.info('get_user')
    user_data = {}
    user_data['id'] = current_user.id
    user_data['public_id'] = current_user.public_id
    user_data['username'] = current_user.username
    user_data['email'] = current_user.email
    user_data['name'] = current_user.name
    response = jsonify(user_data)
    return response


@app.route('/user', methods=['PUT'])
@token_required
def update_user(current_user):

    app.logger.info('update_user')
    data = request.get_json()
    app.logger.info(data, current_user.public_id)

    user = User.query.filter_by(public_id=current_user.public_id).first()

    user.email = data["email"]
    user.name = data["name"]

    db.session.commit()

    response = jsonify({'message': 'The user has been updated!'})
    return response, 202


@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):

    app.logger.info('promote_user')
    if not current_user.admin:
        app.logger.error(CAN_NOT_PERFORM)
        return jsonify({'message': CAN_NOT_PERFORM}), 201

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        app.logger.error(NO_USER_FOUND)
        return jsonify({'message': NO_USER_FOUND}), 404

    user.admin = True
    db.session.commit()

    return jsonify({'message': 'The user has been promoted!'}), 202


@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):

    app.logger.info('delete_user')
    if not current_user.admin:
        app.logger.error(CAN_NOT_PERFORM)
        return jsonify({'message': CAN_NOT_PERFORM}), 401

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        app.logger.error(NO_USER_FOUND)
        return jsonify({'message': NO_USER_FOUND}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'The user has been deleted!'})


@app.route('/product', methods=['POST'])
@token_required
def create_product(current_user):

    if not current_user.admin:
        app.logger.error(CAN_NOT_PERFORM)
        return jsonify({'message': CAN_NOT_PERFORM}), 401
    app.logger.info('create_product')
    res = requests.post('http://127.0.0.1:5001/product',
                        json=request.get_json())
    return res.json(), 201


@app.route('/products', methods=['GET'])
@token_required
def get_all_products(current_user):

    app.logger.info('get_all_products')
    res = requests.get('http://127.0.0.1:5001/products')
    return res.json()


@app.route('/products/category', methods=['GET'])
@token_required
def get_product_by_categories(current_user):

    app.logger.info('get_product_by_categories')
    res = requests.get('http://127.0.0.1:5001/products/category')
    return res.json()


@app.route('/product/<product_id>/rating', methods=['PUT'])
@token_required
def add_rating(current_user, product_id):

    app.logger.info('add_rating')
    res = requests.put('http://127.0.0.1:5001/product/' + str(product_id) + '/rating', json=request.get_json())
    return res.json(), 202


@app.route('/products/price/increasing', methods=['GET'])
@token_required
def sort_by_increasing_price(current_user):

    app.logger.info('sort_by_increasing_price')
    res = requests.get('http://127.0.0.1:5001/products/price/increasing')
    return res.json()


@app.route('/products/price/decreasing', methods=['GET'])
@token_required
def sort_by_decreasing_price(current_user):

    app.logger.info('sort_by_decreasing_price')
    res = requests.get('http://127.0.0.1:5001/products/price/decreasing')
    return res.json()

@app.route('/products/rating/decreasing', methods=['GET'])
@token_required
def sort_by_rating(current_user):

    app.logger.info('sort_by_rating')
    res = requests.get('http://127.0.0.1:5001/products/rating/decreasing')
    return res.json()

@app.route('/products/no_of_ratings/decreasing', methods=['GET'])
@token_required
def sort_by_no_of_ratings(current_user):

    app.logger.info('sort_by_no_of_ratings')
    res = requests.get('http://127.0.0.1:5001/products/no_of_ratings/decreasing')
    return res.json()

@app.route('/product/<product_id>/<quantity>', methods=['POST'])
@token_required
def add_to_cart(current_user, product_id, quantity):

    app.logger.info('add_to_cart')
    res = requests.post('http://127.0.0.1:5001/add_to_cart', json={ 'public_id': current_user.public_id, 'product_id' : product_id, 'quantity': quantity})
    return res.json()


@app.route('/checkout', methods = ['POST'])
@token_required
def checkout(current_user):

    app.logger.info('checkout')
    res = requests.post('http://127.0.0.1:5002/checkout/'+ str(current_user.public_id))
    return res.json()

@app.route('/orders', methods=['GET'])
@token_required
def orders(current_user):

    app.logger.info('orders')
    res = requests.get('http://127.0.0.1:5002/orders')
    return res.json()