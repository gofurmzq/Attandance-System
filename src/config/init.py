"""Flask configuration."""
from datetime import timedelta
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(path.dirname(path.dirname(basedir)), '.env'))

class Config(object):
    """Set Flask config variables."""
    TEMPLATE_FOLDER 		        = '../Templates'
    STATIC_URL 				        = '/static'
    STATIC_ROOT 			        = '../static'

    DATEFORMAT		                = '%Y-%m-%d'
    TIMEFORMAT 		                = '%H:%M'
    DATETIMEFORMAT                  = '%Y/%m/%d %H:%M'

    CACHE_DEFAULT_TIMEOUT 		    = environ.get('CACHE_DEFAULT_TIMEOUT')
    CACHE_TYPE 				        = environ.get('CACHE_TYPE')
    
    JWT_COOKIE_SECURE               = environ.get('JWT_COOKIE_SECURE')
    JWT_ACCESS_TOKEN_EXPIRES        = timedelta(hours=1)
    JWT_SECRET_KEY			        = environ.get('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION		        = ["headers", "cookies", "json", "query_string"]

    SQLALCHEMY_TRACK_MODIFICATIONS  = False
    
    SECRET_KEY 	       		        = environ.get('SECRET_KEY')
    SALT_KEY 				        = environ.get('SALT_KEY')

class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get('PROD_DATABASE_URI')

class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI')