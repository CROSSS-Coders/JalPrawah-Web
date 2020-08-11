from app.extensions import db
from app.models.values import Values
from app.models.weather import Weather
from app.models.subscribe import Subscribe

class Dam(db.Model):
    __tablename__ = 'dam'

    id = db.Column(db.Integer(), primary_key=True)
    station_code = db.Column(db.String(80), unique=True, nullable=True)
    date_of_establishment = db.Column(db.Date(),nullable=True)
    district = db.Column(db.String(80), nullable=True)
    name = db.Column(db.String(80), nullable=True)
    office = db.Column(db.String(80), nullable=True)
    warning_level= db.Column(db.Float(),nullable=True)
    frl_level= db.Column(db.Float(),nullable=True)
    danger_level = db.Column(db.Float(), nullable=True)
    status = db.Column(db.String(80), nullable=True)
    flood_level_prediction = db.Column(db.String(80), nullable=True)
    hfl_level= db.Column(db.Float(),nullable=True)
    hfl_level_date = db.Column(db.Date(), nullable=True)
    meteorologicadivision = db.Column(db.String(80), nullable=True)
    mwl_level= db.Column(db.Float(),nullable=True) 
    river = db.Column(db.String(80), nullable=True)
    lat= db.Column(db.Float(),nullable=True)
    lon = db.Column(db.Float(), nullable=True)
    catchmentarea = db.Column(db.Integer(), nullable=True)
    created_at = db.Column(db.DateTime(), nullable=True)
    values = db.relationship('Values', backref='dam')
    weather = db.relationship('Weather', backref='dam')
    iot = db.relationship('Iot', backref='dam')
    subscribe = db.relationship('Subscribe', backref='dam')


    def __repr__(self):
        return "<Dam: {} , {}>".format(self.name, self.station_code)

