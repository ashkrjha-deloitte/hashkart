import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #DB
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'cart.db')
    #Swagger
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'

    discounts={
        "DISCOUNT5":0.05,
        "DISCOUNT10":0.1
    }