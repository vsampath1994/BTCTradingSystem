# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Required

from ..models import User

import sys


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    client_info = RadioField('Label', choices=[('Trader', 'Trader'),('Client', 'Client')], default='Client', validators=[Required()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    cell_number = StringField('Cell Number')
    street = StringField('Street');
    city = StringField('City');
    state = StringField('State');
    zip_code = StringField('Zip');
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    #def validate_email(self, field):
    #    if User.query.filter_by(email=field.data).first():
    #        raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')


class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
