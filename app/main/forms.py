from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


class EditMyHomebaseForm(FlaskForm):
    city = StringField('City', validators=[DataRequired()])
    submit = SubmitField('Update')
