from app.extensions import db

class Values(db.Model):
    __tablename__ = 'values'

    id = db.Column(db.Integer(), primary_key=True)
    value = db.Column(db.Float(),nullable=True)
    datatype = db.Column(db.String(80),nullable=True)
    datatime = db.Column(db.DateTime,nullable=True)
    dam_id = db.Column(db.Integer, db.ForeignKey('dam.id'),nullable=False)

    def __repr__(self):
        return "<value: {} , {} ,{}>".format(self.value, self.dam_id,self.datatime)
    
