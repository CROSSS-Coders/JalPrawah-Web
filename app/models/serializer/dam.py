from app.models.dam import Dam
from app.models.values import Values
from app.models.weather import Weather
from app.models.iot import Iot
from app.models.forecast import Forecast
from app.models.user import User
from app.models.subscribe import Subscribe
from app.extensions import ma
from marshmallow_sqlalchemy.fields import Nested
from marshmallow import fields, pre_dump
from datetime import datetime


class ValuesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Values
        include_fk = True

    date = fields.Method("date_from_datatime")

    def date_from_datatime(self, obj):
        return obj.datatime.strftime("%d-%b")


class WeatherSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Weather
        include_fk = True


class IotSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Iot
        include_fk = True

    date = fields.Method("date_from_datatime")

    def date_from_datatime(self, obj):
        return obj.created_at.strftime("%H:%M:%S")


class ForecastSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Forecast
        include_fk = True

    date = fields.Method("date_from_createdat")
    datatime = fields.Method("date_from_datatime")

    def date_from_createdat(self, obj):
        return obj.created_at.strftime("%H:%M:%S")

    def date_from_datatime(self, obj):
        return obj.created_at.strftime("%d-%b")


class DamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Dam

    # values=Nested(ValuesSchema,many=True)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class UsersSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    mobile = ma.auto_field()
    email = ma.auto_field()
    role = ma.auto_field()


class SubscribeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Subscribe
        include_fk = True

    dam_name = fields.Method("dam_name")

    def dam_name(self, obj):
        print('sdjd')
        return Dam.query.filter_by(dam_id=obj.dam_id).first().name
