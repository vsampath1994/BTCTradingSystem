from flask_wtf import FlaskForm
from wtforms import IntegerField, RadioField, SubmitField, StringField, PasswordField
from flask_login import current_user
from wtforms.validators import DataRequired, Required, Email, EqualTo
from wtforms.fields.html5 import DateField

from ..models import User

class SearchForm(FlaskForm):
    """
    Form for clients to buy bitcoins
    """

    fromDate = DateField('startDate', format="%Y-%d-%d")
    toDate = DateField('endDate', format="%Y-%d-%d")

    submit = SubmitField('Search')

    #def validate_buy(self, field):

class ClientTraderForm(FlaskForm):
    """
    Form to add new client
    """
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
    submit = SubmitField('Add')

    #def validate_email(self, field):
    #    if User.query.filter_by(email=field.data).first():
    #        raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')
