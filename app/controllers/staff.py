from functools import wraps
import functools
import json
import requests
from flask import flash, redirect, render_template, request, jsonify,abort
from flask import Blueprint, session, url_for, g
import click
from flask.cli import AppGroup
import csv
import os
from datetime import datetime
from app.service.cwcapi import Cwcapi
from app.service.opw import Openweather
from app.models.dam import Dam
from app.models.user import User
from app.models.values import Values
from app.models.weather import Weather
from app.models.forecast import Forecast
from app.models.iot import Iot
from app.extensions import db, rq
from app.setting import OWM_KEY
from flask import current_app
import secrets
import string
from app.models.serializer.dam import DamSchema,UsersSchema
from flask_cors import CORS
from flask_cors import cross_origin
from app.controllers import staff

blueprint = Blueprint('staff', __name__, url_prefix='/staff')


def require_api_key(api_method):
    @wraps(api_method)
    def check_api_key(*args, **kwargs):
        if "Authorization" in request.headers:
            apikey = request.headers.get('Authorization')
            u = User.query.filter_by(api_token=apikey).first()
            print('smss')
            if u != None :
                if u.role=='user':
                    print('sm')
                    abort(401)
                else:
                    return api_method(*args, **kwargs)
            else:
                abort(401)
        else:
            abort(401)
    return check_api_key


@blueprint.cli.command('create')
@cross_origin()
def create_staff():
    alphabet = string.ascii_letters + string.digits
    api_token = ''.join(secrets.choice(alphabet) for i in range(120))
    u = User(
        mobile=8080808080,
        api_token=api_token,
        role='staff',
        created_at=datetime.now()
    )
    db.session.add(u)
    db.session.commit()


@blueprint.route('/user', methods=['GET'])
@require_api_key
def get_user():
    user=User.query.all()
    user_schema = UsersSchema(many=True)
    return jsonify(user=user_schema.dump(user))


@blueprint.route('/status/<int:id>', methods=['POST'])
@cross_origin()
@require_api_key
def change_status(id):
    dam=Dam.query.get(id)
    dam.status = request.form['status']
    db.session.commit()
    dam_schema = DamSchema()
    return jsonify(dam=dam_schema.dump(dam))


@blueprint.route('/sendnotification', methods=['GET'])
@require_api_key
def notify_user():
    staff.send_tweet.queue()
    staff.send_emails.queue()
    staff.send_push.queue()
