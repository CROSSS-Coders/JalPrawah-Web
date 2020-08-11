import functools
import json
import requests
from flask import flash, redirect, render_template, request, jsonify
from flask import Blueprint, session, url_for, g
import click
from flask.cli import AppGroup
from app.models.dam import Dam
from app.models.values import Values
from app.models.weather import Weather
from app.models.forecast import Forecast
from app.extensions import db,rq
from app.setting import OWM_KEY
from flask import current_app
import logging
from flask_json import JsonError, json_response, as_json
from app.models.serializer.dam import DamSchema, ValuesSchema
from app.service.prediciton import make_forecast
from app.models.serializer.dam import ForecastSchema
from datetime import datetime, timedelta
from flask.cli import with_appcontext

blueprint = Blueprint('forecasts', __name__, url_prefix='/forecast')

@blueprint.route('/<int:dam_id>', methods=['GET'])
def get_value_from_dam_id(dam_id):
    values = Forecast.query.filter(
        Forecast.dam_id == dam_id).all()
    forecast_schema = ForecastSchema(many=True)
    return json_response(values=forecast_schema.dump(values))

def _daterange(start_date, end_date):
    delta = timedelta(hours=1)
    start_date += delta
    while start_date <= end_date:
        yield start_date
        start_date += delta

def get_station_values(station_code, _id, window_size=3):
    '''
    Returns water values vs time dictionary
    '''

    start_date = datetime.now() - timedelta(days=window_size)
    result=Values.query.filter(Values.dam_id==_id).filter(Values.datatime>start_date).filter(Values.datatype=="HHS")
    water_values = {'water_level': [], 'time': []}
    new_start = start_date
    for entry in result:
        dt_time = entry.datatime
        water_values['water_level'].extend(
            [entry.value for _ in _daterange(new_start, dt_time)])
        water_values['time'].extend(
            [new_date.strftime('%Y-%m-%d:%H') for new_date in _daterange(new_start, dt_time)])
        new_start = dt_time

    water_values['water_level'].extend(
        [entry.value for _ in _daterange(new_start, datetime.now())])
    water_values['time'].extend([new_date.strftime('%Y-%m-%d:%H')
                                 for new_date in _daterange(new_start, datetime.now())])
    return water_values

@blueprint.cli.command('dam')
@click.argument("station_id")
def fetch_weather(station_id):
    ''' Forecast Dam prediction and store in database'''
    dam= Dam.query.filter_by(station_code=station_id).first()
    _id=dam.id
    info = {
        'hfl': dam.hfl_level,
        'warning': dam.warning_level,
        'mwl': dam.mwl_level,
        'frl': dam.frl_level
    }
    water_values = get_station_values(station_id, _id)
    forecast, levels = make_forecast(
        info['hfl'], info['danger'], info['warning'], water_values['water_level'], water_values['time'])
    # Levels are in float, not percentage!
    print({'forecast': forecast, 'levels': levels})

def get_status(level):
    if level['normal']==1.0:
        return 'Normal'
    if level['warning']==1.0:
        return 'Warning'
    if level['danger']==1.0:
        return 'Danger'
    if level['hfl']==1.0:
        return 'Highest Flood Level'
    return 'Normal'


@blueprint.cli.command('dams')
def forecast_value():
    ''' Forecast Dam prediction and store in database'''
    return forecast_values()


@rq.job
@with_appcontext
def forecast_values():
    dams = Dam.query.all()
    for dam in dams:
        if dam.name != 'IOT':
            _id = dam.id
            info = {
                'hfl': dam.hfl_level,
                'danger':dam.danger_level,
                'warning': dam.warning_level,
                'mwl': dam.mwl_level,
                'frl': dam.frl_level
            }
            water_values = get_station_values(dam.station_code, _id)
            forecast, levels = make_forecast(
                info['hfl'], info['danger'], info['warning'], water_values['water_level'], water_values['time'])
            print(forecast['values'][2])
            status=get_status(levels)
            dam.status=status
            db.session.commit()
            Forecast.query.filter_by(dam_id=dam.id).delete()
            db.session.commit()
            for value in range(len(forecast['values'])):
                water_level=forecast['values'][value]
                date=datetime.strptime(forecast['time'][value], "%Y-%m-%d:%H")
                f=Forecast(
                    water_level=float("{:.4f}".format(water_level)),
                    dam_id=dam.id,
                    created_at=date
                )
                db.session.add(f)
            db.session.commit()
            print({'dam': forecast, 'levels':levels })
        else:
            continue
