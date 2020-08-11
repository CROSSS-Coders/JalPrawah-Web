from app.extensions import db

class Iot(db.Model):

    __tablename__ = 'iot'

    id = db.Column(db.Integer(), primary_key=True)
    temperature = db.Column(db.Float(), nullable=True)
    humidity = db.Column(db.Float(), nullable=True)
    pressure = db.Column(db.Float(), nullable=True)
    presureonwall = db.Column(db.Float(), nullable=True)
    door_open = db.Column(db.Boolean(), nullable = True)
    door_open_code = db.Column(db.Integer(), nullable = True)
    water_level = db.Column(db.Float(), nullable=True)
    forecast_value = db.Column(db.String(180), nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    dam_id = db.Column(db.Integer, db.ForeignKey('dam.id'), nullable=False)

    def __repr__(self):
        return "<Iot:  {}>".format( self.dam_id)
