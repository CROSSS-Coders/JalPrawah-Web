import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv('FLASK_ENV', default='production')
DEBUG = ENV == 'development'

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

OWM_KEY = os.getenv('OWM_KEY')

SENTRY_URL=os.getenv('SENTRY_URL')
#twitter credentials
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
CONSUMER_API = os.getenv('CONSUMER_API')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')

# https: // flask-sqlalchemy.palletsprojects.com/en/2.x/config /?highlight = mysql
SQLALCHEMY_DATABASE_URI = "sqlite:////"+os.getcwd()+"/app/models/db.sqlite"
# SQLALCHEMY_DATABASE_URI = 'mysql://admin:crosscoders@jalpravahproduction.czbefh8finsp.ap-south-1.rds.amazonaws.com:3306/newjalpravah'
SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_POOL_RECYCLE=1

FLASK_ADMIN_SWATCH = 'flatly'
SECRET_KEY="sihflodddetecttion1122212app"

SCHEDULER_API_ENABLED = True

MAILGUN_KEY = os.getenv('MAILGUN_KEY')
MAILGUN_URL= os.getenv('MAILGUN_URL')

RQ_REDIS_URL='redis://localhost:6379/0'

FIREBASE_API = os.getenv('FIREBASE_API')

MSG91_KEY = os.getenv('MSG91_KEY')

RQ_DASHBOARD_REDIS_URL = 'redis://localhost:6379/0'
RQ_DASHBOARD_USERNAME = 'rq'
RQ_DASHBOARD_PASSWORD = 'rq'

BASIC_AUTH_USERNAME="admin"
BASIC_AUTH_PASSWORD="admin"
