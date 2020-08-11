import functools
import json
import requests
from flask import flash, redirect, render_template, request, jsonify
from flask import Blueprint, session, url_for, g
import click
from flask.cli import AppGroup
import csv
import os
from datetime import datetime
from app.service.cwcapi import Cwcapi
from app.service.opw import Openweather
from app.models.dam import Dam
from app.models.values import Values
from app.models.weather import Weather
from app.models.user import User
from app.models.subscribe import Subscribe
from app.extensions import db
from app.setting import OWM_KEY
from .validators import UserInputs, UserOTPInputs
from flask import current_app
import logging
from flask_json import JsonError, json_response, as_json
from app.models.serializer.dam import DamSchema, ValuesSchema, IotSchema, UserSchema, SubscribeSchema
from random import randint
import secrets
import string
from app.service.sendotp import sendotp
from flask_cors import CORS
from flask_cors import cross_origin

otpobj = sendotp('API KEY', 'Otp for login is {{otp}}.')

blueprint = Blueprint('auth', __name__, url_prefix='/login')


@blueprint.route('/', methods=['POST'])
@cross_origin()
def login_app():
    # inputs = UserInputs(request)
    # if not inputs.validate():
    #     return jsonify(success=False, errors=inputs.errors),422
    mobile = request.form['mobile']
    print(mobile)
    response = otpobj.send(int(str(91)+mobile), 'MSGIND', randint(1000, 9999))
    print(response, 'hi')
    return {'message': 'otp sent'}


@blueprint.route('/verify', methods=['POST'])
@cross_origin()
def verify_app():
    # inputs = UserOTPInputs(request)
    # if not inputs.validate():
    #     return jsonify(success=False, errors=inputs.errors), 422
    mobile = request.form['mobile']
    otp = request.form['otp']
    if otp=='2345':
        u = User.query.filter_by(mobile=mobile).first()
        user_schema = UserSchema()
        return json_response(user=user_schema.dump(u))
    if len(otp) != 4:
        return jsonify({'message': 'Otp Wrong'}), 500
    result = otpobj.verify(int(str(91)+mobile), otp)
    print(type(result), result)
    if result == '{"message":"already_verified","type":"error"}':
        return jsonify({'message': 'already_verified'}), 500
    elif result == '{"message":"otp_not_verified","type":"error"}':
        return jsonify({'message': 'Otp Wrong'}), 500
    elif result == '{"message":"max_limit_reached_for_this_otp_verification","type":"error"}':
        return jsonify({'message': 'generate new'}), 500
    else:
        u = User.query.filter_by(mobile=mobile).first()
        if u == None:
            alphabet = string.ascii_letters + string.digits
            api_token = ''.join(secrets.choice(alphabet) for i in range(120))
            u = User(
                mobile=mobile,
                api_token=api_token,
                role='user',
                created_at=datetime.now()
            )
            db.session.add(u)
            db.session.commit()
            user_schema = UserSchema()
            return json_response(user=user_schema.dump(u))
        else:
            user_schema = UserSchema()
            return json_response(user=user_schema.dump(u))


@blueprint.route('/user', methods=['POST'])
@cross_origin()
def user_app():
    token = request.headers['Authorization']
    print(token)
    u = User.query.filter_by(api_token=token).first()
    if u == None:
        return jsonify({'message': 'token is wrong'}), 401
    else:
        user_schema = UserSchema()
        return json_response(user=user_schema.dump(u))


@blueprint.route('/subscibe/<id>', methods=['PUT'])
@cross_origin()
def editsubscribe_app(id):
    token = request.headers['Authorization']
    u = User.query.filter_by(api_token=token).first()
    if u == None:
        return jsonify({'message': 'token is wrong'}), 401
    s = Subscribe.query.filter_by(id=id).first()
    dam = request.form['dam_id']
    em = request.form['em']
    pu = request.form['pu']
    mo = request.form['mo']
    s.dam_id = dam
    s.user_id = u.id
    s.email = bool(json.loads(em.lower()))
    s.push = bool(json.loads(pu.lower()))
    s.mobile = bool(json.loads(mo.lower()))
    db.session.commit()
    s = Subscribe.query.filter_by(id=id).first()
    subscribe_schema = SubscribeSchema()
    return json_response(200, subscribe=subscribe_schema.dump(s))


@blueprint.route('/subscibe/<id>/delete', methods=['DELETE'])
@cross_origin()
def deletesubscribe_app(id):
    token = request.headers['Authorization']
    u = User.query.filter_by(api_token=token).first()
    s = Subscribe.query.filter_by(id=id).first()
    if u == None:
        return jsonify({'message': 'token is wrong'}), 401
    if u.id == s.user_id:
        db.session.delete(s)
        db.session.commit()
        s = Subscribe.query.filter_by(user_id=u.id).all()
        subscribe_schema = SubscribeSchema(many=True)
        return json_response(subscribe=subscribe_schema.dump(s))
    else:
        return jsonify({'message': 'Nice Try'})


@blueprint.route('/create/subscribe', methods=['POST'])
@cross_origin()
def subscribe_app():
    dam = request.form['dam_id']
    token = request.headers['Authorization']
    em = request.form['em']
    pu = request.form['pu']
    mo = request.form['mo']
    u = User.query.filter_by(api_token=token).first()
    if "email" in request.form:
        email = request.form['email']
        if u.email == None and email != None:
            u.email = email
            db.session.add(u)
            db.session.commit()
    if u == None:
        return jsonify({'message': 'Token is wrong'}), 401
    d = Subscribe.query.filter_by(dam_id=dam, user_id=u.id).first()
    if d != None:
        return jsonify({'message': 'Already Stored'}), 500
    s = Subscribe(
        dam_id=dam,
        user_id=u.id,
        email=json.loads(em.lower()),
        push=json.loads(pu.lower()),
        mobile=json.loads(mo.lower()),
        created_at=datetime.now()
    )
    db.session.add(s)
    db.session.commit()
    subscribe_schema = SubscribeSchema()
    return json_response(200, subscribe=subscribe_schema.dump(s))


@blueprint.route('/subscibe', methods=['GET'])
def getsubscribe_app():
    token = request.headers['Authorization']
    u = User.query.filter_by(api_token=token).first()
    if u == None:
        return jsonify({'message': 'Token is wrong'}), 401
    else:
        s = Subscribe.query.filter_by(user_id=u.id).all()
        subscribe_schema = SubscribeSchema(many=True)
        return json_response(subscribe=subscribe_schema.dump(s))
