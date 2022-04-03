from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField
from wtforms.validators import InputRequired


class TimeForm(FlaskForm):
    name = StringField('Swimmer Name', validators=[InputRequired()])
    gender = RadioField('Swimmer Gender', choices=[('m', 'Male'), ('f', 'Female')], validators=[InputRequired()])
    event = SelectField('Event', choices=[('100bk', '100 Back'), ('100bt', '100 Breast'),
                                          ('100fy', '100 Fly'), ('50fe', '50 Free'),
                                          ('100fe', '100 Free'), ('200fe', '200 Free'),
                                          ('500fe', '500 Free'), ('200im', '200 IM')],
                        validators=[InputRequired()])
