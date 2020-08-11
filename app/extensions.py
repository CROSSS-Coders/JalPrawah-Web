from pyfcm import FCMNotification
from flask_sqlalchemy import SQLAlchemy
from flask_crontab import Crontab
from flask_json import FlaskJSON
from flask_apscheduler import APScheduler
from flask_marshmallow import Marshmallow
import tweepy
from .setting import ACCESS_SECRET,ACCESS_TOKEN,CONSUMER_API,CONSUMER_SECRET,FIREBASE_API
from . import setting
from flask_rq2 import RQ
from pyfcm import FCMNotification
from flask_basicauth import BasicAuth
import telegram

rq = RQ()

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_API, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# Create API object
tweet_api = tweepy.API(auth)

#firebase
push_service = FCMNotification(api_key=FIREBASE_API)

db = SQLAlchemy()
basic_auth = BasicAuth()
crontab = Crontab()
json = FlaskJSON()
scheduler = APScheduler()
ma =Marshmallow()

bot = telegram.Bot(token='token')




