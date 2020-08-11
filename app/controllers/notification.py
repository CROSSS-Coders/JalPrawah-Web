import functools
import json
import requests
from flask import flash, redirect, render_template, request, jsonify
from flask import Blueprint, session, url_for, g, current_app
import click
from flask.cli import AppGroup
import csv
import os
from datetime import datetime
from app.service.sendsms import send_sms
from app.service.cwcapi import Cwcapi
from app.service.opw import Openweather
from app.models.dam import Dam
from app.models.values import Values
from app.models.weather import Weather
from app.models.user import User
from app.models.subscribe import Subscribe
from app.extensions import db, tweet_api, rq,bot
from .validators import UserInputs, UserOTPInputs
from flask.cli import with_appcontext
from flask_rq2 import RQ
from datetime import timedelta
from flask.cli import with_appcontext
from app.service.sendmail import send_mail
from app.extensions import push_service
from twilio.rest import Client
from telegram import ParseMode


blueprint = Blueprint('notification', __name__)


@rq.job
def add(x, y):
    print(x+y)
    return x + y


@blueprint.cli.command('call')
def call():
    account_sid = 'ACbeee45299cff89a919cbd01293f3ec9a'
    auth_token = '03b03ae58290384bf7333c8c7195e5c0'
    client = Client(account_sid, auth_token)
    call = client.calls.create(
        url='https://api.pushpak1300.me/answer',
        to='+919967464745',
        from_='+12025194004'
    )

    print(call.sid)


@blueprint.cli.command('telegram')
def telegram():
    Dams = Dam.query.filter(Dam.status.in_(['Danger', 'Warning'])).all()
    for dam in Dams:
        value = Values.query.filter_by(dam_id = dam.id,datatype = 'HHS').order_by(Values.id.desc()).first()
        message = '<b>'+dam.status+'</b>!\n \nBe Safe !\nThere is a high chance of flooding near '+dam.name + \
            ' area in the next 3 days.\nCurrent water level: <b>' + \
            str(value.value)+' m </b> \nToll-Free Helpline Number: <b> +919711077372.</b>\nVisit https://jalpravah.pushpak1300.me/ for live flood status.'
        bot.send_message(chat_id='@jalpravah', text=message, parse_mode=ParseMode.HTML )


@rq.job
@with_appcontext
def push_iot(status):
    result = push_service.notify_topic_subscribers(
        topic_name="iot", message_body="Warning! Be Safe! "+status+" in IOT dam.")
    return result


@blueprint.cli.command('push')
def push_status():
    ''' send status of flood on push'''
    result = push_service.notify_topic_subscribers(
        topic_name="iot", message_body="Warning! Be Safe! Warning in IOT dam.")
    return result


@blueprint.cli.command('pushes')
def pushes_status():
    ''' send status of flood on push'''
    Dams = Dam.query.filter(Dam.status.in_(['Danger', 'Warning'])).all()
    for dam in Dams:
        result = push_service.notify_topic_subscribers(
            topic_name=str(dam.id), message_body="Warning! Be Safe! Warning in "+dam.name+" dam.")
        return result


@blueprint.cli.command('tweet')
def tweet_status():
    ''' send status of flood on twitter'''
    send_tweet()
    return 'DONE'


@blueprint.cli.command('sms')
def send_sms_of_warning():
    ''' send status of flood on sms'''
    send_message()
    return 'DONE'


@rq.job
@with_appcontext
def send_message_iot(status):
    users = User.query.all()
    for user in users:
        message = status+' \n!Be Safe! There is a high chance of flooding near IOT' \
            ' area in the next 3 days. Toll-Free Helpline Number: +91-9711077372.Visit https://jalpravah.pushpak1300.me/ for live flood status.'
        send_sms(message, user)


@rq.job
@with_appcontext
def send_message():
    ''' send status of flood on sms'''
    Dams = Dam.query.filter(Dam.status.in_(['Danger', 'Warning'])).all()
    for dam in Dams:
        subs = Subscribe.query.filter_by(dam_id=dam.id).all()
        for sub in subs:
            user = User.query.filter_by(id=sub.user_id).first()
            if user is None:
                continue
            # us = {
            #     "mobiles": "91"+user.mobile,
            #     "status": dam.status,
            #     "dam": str(dam.name),
            #     "helpline": "+91-9711077372",
            #     "url": "https://pushpak1300.github.io/jalpravah",
            #     "flood status": str(dam.status)
            # }
            message = dam.status+'!Be Safe! There is a high chance of flooding near '+dam.name + \
                ' area in the next 3 days. Toll-Free Helpline Number: +91-9711077372.Visit https://pushpak1300.github.io/jalpravah for live flood status.'
            # userlist.append(us)
            send_sms(message, user)


@rq.job
@with_appcontext
def send_tweet():
    ''' send status of flood on twitter'''
    Dams = Dam.query.filter(Dam.status.in_(['Danger', 'Warning'])).all()
    for dam in Dams:
        message = dam.status+'! \nBe Safe! There is a high chance of flooding near '+dam.name + \
            ' area in the next 3 days. \nToll-Free Helpline Number: +91-9711077372.\nVisit https://pushpak1300.github.io/jalpravah for live flood status.'
        tweet_api.update_status(message)


@rq.job
@with_appcontext
def send_mails():
    ''' send status of flood on mail'''
    Dams = Dam.query.filter(Dam.status.in_(['Danger', 'Warning'])).all()
    for dam in Dams:
        subs = Subscribe.query.filter_by(dam_id=dam.id).all()
        userlist = []
        print(subs)
        for sub in subs:
            print(sub.user_id)
            user = User.query.filter_by(id=sub.user_id).first()
            print(user)
            if user is None:
                continue
            userlist.append(user.email)
        print(userlist)
        message = dam.status+'! There is high chance of flooding near '+dam.name + \
            ' area in next 3 days.Be Safe!.Contact Toll Free Helpline Number:+91-9711077372.and visit https://pushpak1300.github.io/jalpravah for live flood status.'
    return send_mail(userlist, 'Flood Notification', message)


@blueprint.cli.command('mail')
def send_simple_message():
    job = send_mails.queue()
    print(job)  # "text": tweet_message})
