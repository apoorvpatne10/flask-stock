from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class RegisterForm(FlaskForm):
    phone_no = IntegerField('Phone number',
                             validators=[DataRequired()])
    threshold = IntegerField('Threshold',
                             validators=[DataRequired()])
    submit = SubmitField('Check stocks!')
