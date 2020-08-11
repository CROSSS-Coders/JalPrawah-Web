from app.extensions import db

class Subscribe(db.Model):

    __tablename__ = 'subscription'

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.Boolean(), nullable=True)
    mobile = db.Column(db.Boolean(), nullable = True)
    push = db.Column(db.Boolean(), nullable=True)
    dam_id = db.Column(db.Integer, db.ForeignKey('dam.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return "<Subscribe: {} >".format( self.dam_id)
