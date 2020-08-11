from app.extensions import db
from app.models.subscribe import Subscribe

class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(80), nullable=True)
    mobile = db.Column(db.String(80), unique=True, nullable=True)
    api_token = db.Column(db.String(180), nullable=True)
    role= db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    subscribe = db.relationship('Subscribe', backref='user')

    def __repr__(self):
        return "<User: {} >".format( self.role)
