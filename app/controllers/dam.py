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
from app.models.forecast import Forecast
from app.models.iot import Iot
from app.extensions import db,rq
from app.setting import OWM_KEY
from flask import current_app
import logging
from flask_json import JsonError, json_response, as_json
from app.models.serializer.dam import DamSchema, ValuesSchema, IotSchema, ForecastSchema
import pusher
from flask.cli import with_appcontext
from .validators import UserInputs, UserOTPInputs
from app.controllers import notification
from flask_rq2 import RQ
from twilio.twiml.voice_response import VoiceResponse, Play


pusher_client = pusher.Pusher(
    app_id='app_id',
    key='app_key',
    secret='App_secret',
    cluster='ap2',
)

blueprint = Blueprint('dams', __name__, url_prefix='/')



@blueprint.route('/', methods=['GET'])
def hello_world():
    now = datetime.utcnow()
    return json_response(time=now)


@blueprint.route('/dams', methods=['GET'])
def get_dam_value():
    dams = Dam.query.all()
    dam_schema = DamSchema(many=True)
    return json_response(dams=dam_schema.dump(dams))


@blueprint.route('/dams/<int:dam_id>', methods=['GET'])
def get_value_from_dam_id(dam_id):
    values = Values.query.filter(
        Values.dam_id == dam_id, Values.datatype == 'HHS').all()
    values_schema = ValuesSchema(many=True)
    forecast = Forecast.query.filter(
        Forecast.dam_id == dam_id).all()
    forecast_schema = ForecastSchema(many=True)
    return json_response(values=values_schema.dump(values),forecast=forecast_schema.dump(forecast))


@blueprint.route('/iot', methods=['GET'])
def get_value_from_iot():
    values = Iot.query.filter().all()
    iot_schema = IotSchema(many=True)
    return json_response(values=iot_schema.dump(values))


@blueprint.route('/status/<int:dam_id>', methods=['GET'])
def get_status_from_dam(dam_id):
    dam=Dam.query.filter_by(id=dam_id).first()
    return jsonify({'status':dam.status})

@blueprint.route('/iot/store', methods=('GET', 'POST'))
@as_json
def store_iot_values():
    if request.method == 'POST':
        dam = Dam.query.filter_by(name='IOT').first()
        if(dam is None):
            dam = Dam(name='IOT')
            db.session.add(dam)
            db.session.commit()
        Fow = calcuate_pressure(float(request.form['water_level']))
        print(datetime.strptime(
            request.form['created_at'], "%Y-%m-%dT%H:%M:%S"))
        iot = Iot(
            water_level=request.form['water_level'],
            humidity=request.form['humidity'],
            temperature=request.form['temperature'],
            created_at=datetime.strptime(
                request.form['created_at'], "%Y-%m-%dT%H:%M:%S"),
            door_open_code=request.form['door_open'],
            forecast_value=request.form['forecast_string'],
            pressure=Fow,
            dam_id=dam.id
        )
        db.session.add(iot)
        iot_schema = IotSchema()
        pusher_client.trigger('iot', 'updated', {'message': iot_schema.dump(iot)})
        db.session.commit()
        if iot.water_level>20.5:
            notification.push_iot.queue('Danger')
            notification.send_message_iot.queue('Danger')
        elif iot.water_level > 17:
            notification.push_iot.queue('Warning')
            notification.send_message_iot.queue('Danger')
        return {'store': 'true'}
    else:
        return {'store': 'false'}


def calcuate_pressure(water_level):
    R = 1000
    g = 9.8
    t = 0.25
    pavg = (R*g*(water_level//2))/100
    # F = pavg*water_level*t
    return pavg


@blueprint.route("/answer", methods=['GET', 'POST'])
def answer_call():
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiMLs response
    response = VoiceResponse()
    response.play(
        'https://jalpravah-sound.s3.ap-south-1.amazonaws.com/Warning.mp3')
    return str(response)

@rq.job
def fetch_dams():
    click.secho("""

        ____                      __      _       _     _
        |  _ \  __ _ _ __ ___    / _| ___| |_ ___| |__ (_)_ __   __ _
        | | | |/ _` | '_ ` _ \  | |_ / _ \ __/ __| '_ \| | '_ \ / _` |
        | |_| | (_| | | | | | | |  _|  __/ || (__| | | | | | | | (_| |_ _ _
        |____/ \__,_|_| |_| |_| |_|  \___|\__\___|_| |_|_|_| |_|\__, (_|_|_)
                                                                |___/

        """,  fg='green')
    file_url = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'dam.csv')
    codelist = []
    with open(file_url, newline='') as csvfile:
        damreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in damreader:
            codelist.append(row[0].split(',')[1])
    cwc = Cwcapi()
    for code in codelist:
        if (Dam.query.filter_by(station_code=code).first() is not None):
            pass
        else:
            response = cwc.fetch_stations_info(code)
            doe = response['dateOfEstablishment']
            if doe is None:
                doe = '2000-01-01'
            dam = Dam(
                station_code=response['stationCode'],
                date_of_establishment=datetime.strptime(
                    doe, "%Y-%m-%d").date(),
                district=response['districtId']['name'],
                office=response['divisionalOffice']['name'],
                name=response['name'],
                danger_level=response['floodForecastStaticStationCode']['dangerLevel'],
                warning_level=response['floodForecastStaticStationCode']['warningLevel'],
                frl_level=response['floodForecastStaticStationCode']['frl'],
                hfl_level=response['floodForecastStaticStationCode']['highestFlowLevel'],
                meteorologicadivision=response['floodForecastStaticStationCode']['meteorologicalSubDivision'],
                mwl_level=response['floodForecastStaticStationCode']['mwl'],
                river=response['river']['name'],
                created_at=datetime.now(),
            )
            db.session.add(dam)
    db.session.commit()
    dams = Dam.query.all()
    for dam in dams:
        if dam.name != 'IOT':
            response = cwc.fetch_datatype_info(dam.station_code, 'HHS')
            for value in response:
                values = Values.query.filter_by(datatime=datetime.strptime(
                    value['id']['dataTime'], "%Y-%m-%dT%H:%M:%S"), value=value['dataValue'], datatype="HHS", dam_id=dam.id).first()
                print(values)
                if values is None:
                    values = Values(
                        value=float(value['dataValue']),
                        datatype='HHS',
                        datatime=datetime.strptime(
                            value['id']['dataTime'], "%Y-%m-%dT%H:%M:%S"),
                        dam_id=dam.id,
                    )
                    db.session.add(values)
                else:
                    click.secho("Value Alredy exists",  fg='red')
        else:
            continue
    db.session.commit()
    for dam in dams:
        if dam.name != 'IOT':
            response = cwc.fetch_datatype_info(dam.station_code, 'FIN')
            for value in response:
                values = Values.query.filter_by(datatime=datetime.strptime(
                    value['id']['dataTime'], "%Y-%m-%dT%H:%M:%S"), value=float(
                    value['dataValue']), datatype="FIN", dam_id=dam.id).first()
                if values is None:
                    values = Values(
                        value=float(value['dataValue']),
                        datatype='FIN',
                        datatime=datetime.strptime(
                            value['id']['dataTime'], "%Y-%m-%dT%H:%M:%S"),
                        dam_id=dam.id,
                    )
                    db.session.add(values)
                else:
                    click.secho("Value Alredy exists",  fg='red')
        else:
            pass
    db.session.commit()
    for dam in dams:
        if dam.name != 'IOT':
            response = cwc.fetch_datatype_info(dam.station_code, 'FOL')
            for value in response:
                values = Values.query.filter_by(datatime=datetime.strptime(
                    value['id']['dataTime'], "%Y-%m-%dT%H:%M:%S"), value=float(
                    value['dataValue']), datatype="FOL", dam_id=dam.id).first()
                if values is None:
                    values = Values(
                        value=float(value['dataValue']),
                        datatype='FOL',
                        datatime=datetime.strptime(
                            value['id']['dataTime'], "%Y-%m-%dT%H:%M:%S"),
                        dam_id=dam.id,
                    )
                    db.session.add(values)
                else:
                    click.secho("Value Alredy exists",  fg='red')
        else:
            pass
    db.session.commit()
    print(Dam.query.all())
    click.secho("""
        ____                     ___        __         ____  _                     _
        |  _ \  __ _ _ __ ___   |_ _|_ __  / _| ___   / ___|| |_ ___  _ __ ___  __| |
        | | | |/ _` | '_ ` _ \   | || '_ \| |_ / _ \  \___ \| __/ _ \| '__/ _ \/ _` |
        | |_| | (_| | | | | | |  | || | | |  _| (_) |  ___) | || (_) | | |  __/ (_| |
        |____/ \__,_|_| |_| |_| |___|_| |_|_|  \___/  |____/ \__\___/|_|  \___|\__,_|


        """,  fg='red')
    current_app.logger.info("run")

@blueprint.cli.command('fetch')
def fetch_dam():
    ''' Fetch Dam Info From Databse'''
    return fetch_dams()


@blueprint.cli.command('location')
def fetch_location():
    ''' Fetch Dam location Info From Databse'''
    cwc = Cwcapi()
    response = cwc.fetch_location_info()
    for value in response:
        station_code = value['stationCode']
        dam = Dam.query.filter_by(station_code=station_code).first()
        if dam is None:
            continue
        else:
            dam.lat = value['lat']
            dam.lon = value['lon']
            db.session.add(dam)
            click.secho("Value Fetched",  fg='green')
        db.session.commit()


@blueprint.cli.command('update')
def update_dam():
    cwc = Cwcapi()
    dams = Dam.query.all()
    for dam in dams:
        if dam.name != 'IOT':
            response = cwc.fetch_stations_info(dam.station_code)
            dam.danger_level = response['floodForecastStaticStationCode']['dangerLevel']
        else:
            continue
    db.session.commit()


@blueprint.cli.command('weather')
def fetch_weather():
    ''' Fetch Dam weather Info From Databse'''
    print(OWM_KEY)
    owm = Openweather(OWM_KEY)
    dams = Dam.query.all()
    for dam in dams:
        if dam.lat is None:
            continue
        else:
            response = owm.fetch_weather(dam.lat, dam.lon)
            current_response = response['current']
            if 'rain' not in current_response:
                rain = 0
            else:
                rain = current_response['rain']['1h']
            current_weather = Weather(
                rain=rain,
                windspeed=current_response['wind_speed'],
                wind_degree=current_response['wind_deg'],
                pressure=current_response['pressure'],
                humidity=current_response['humidity'],
                temperature=current_response['temp'],
                datatype='current',
                datatime=datetime.fromtimestamp(current_response['dt']),
                dew_point=current_response['dew_point'],
                created_at=datetime.now(),
                dam_id=dam.id
            )
            db.session.add(current_weather)
            for day in response['daily']:
                if 'rain' not in day:
                    rain = 0
                else:
                    rain = day['rain']
                weather = Weather(
                    rain=rain,
                    windspeed=day['wind_speed'],
                    wind_degree=day['wind_deg'],
                    pressure=day['pressure'],
                    humidity=day['humidity'],
                    temperature=day['temp']['day'],
                    datatype='daily',
                    datatime=datetime.fromtimestamp(day['dt']),
                    dew_point=day['dew_point'],
                    created_at=datetime.now(),
                    dam_id=dam.id
                )
                db.session.add(weather)
    db.session.commit()



