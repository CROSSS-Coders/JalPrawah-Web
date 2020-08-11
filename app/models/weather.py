from app.extensions import db

class Weather(db.Model):

    __tablename__ = 'weather'

    id = db.Column(db.Integer(), primary_key=True)
    rain = db.Column(db.Float(), nullable=True)
    temperature = db.Column(db.Float(), nullable=True)
    humidity = db.Column(db.Float(), nullable=True)
    pressure = db.Column(db.Float(), nullable=True)
    windspeed = db.Column(db.Float(), nullable=True)
    wind_degree = db.Column(db.Float(), nullable=True)
    dew_point = db.Column(db.Float(), nullable=True)
    datatype = db.Column(db.String(80), nullable=True)
    datatime = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    dam_id = db.Column(db.Integer, db.ForeignKey('dam.id'), nullable=False)

    def __repr__(self):
        return "<weather: {} , {}>".format(self.datatime, self.dam_id)
