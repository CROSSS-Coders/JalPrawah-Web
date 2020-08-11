from app.extensions import db

class Forecast(db.Model):

    __tablename__ = 'forecast'

    id = db.Column(db.Integer(), primary_key=True)
    water_level = db.Column(db.Float(), nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    dam_id = db.Column(db.Integer, db.ForeignKey('dam.id'), nullable=False)

    def __repr__(self):
        return "<Forecast: {} , {}>".format(self.dam_id)
