import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'halo-sayang'
    host=os.environ.get('DB_HOST') or 'database-246.ch8tps0b4qd5.ap-southeast-1.rds.amazonaws.com'
    username=os.environ.get('DB_USERNAME') or 'stanley'
    password=os.environ.get('DB_PASSWORD') or 'tantysco'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://' + username + ':' + password + '@' + host + '/users'

    SQLALCHEMY_BINDS={
        'products': 'mysql+pymysql://' + username + ':' + password + '@' + host + '/products',
        'libraries' : 'mysql+pymysql://' + username + ':' + password + '@' + host + '/libraries',
        'transactions' : 'mysql+pymysql://' + username + ':' + password + '@' + host + '/transactions',
        'carts': 'mysql+pymysql://' + username + ':' + password + '@' + host + '/carts'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
