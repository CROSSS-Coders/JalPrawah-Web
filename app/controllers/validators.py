from flask_inputs import Inputs
from wtforms.validators import DataRequired,Length


class UserInputs(Inputs):
    values= {
        'mobile': [DataRequired(),Length(min=10,max=10)],
    }


class UserOTPInputs(Inputs):
    values = {
        'mobile': [DataRequired(), Length(min=10, max=10)],
        'otp': [DataRequired(), Length(min=4, max=4)],
    }
