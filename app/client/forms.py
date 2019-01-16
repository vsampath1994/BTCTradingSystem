from flask_wtf import FlaskForm
from wtforms import IntegerField, RadioField, SubmitField, ValidationError, HiddenField
from wtforms import FloatField
from flask_login import current_user
from wtforms.validators import DataRequired, Email, EqualTo, Required, NumberRange
import json
import urllib2


from ..models import User


class BuyForm(FlaskForm):
    """
    Form for clients to buy bitcoins
    """
    btc_amount = IntegerField('Number of bitcoins', validators=[DataRequired()])
    comm_type = RadioField('Commission Type', choices=[('value', 'Bitcoins'),('value2', 'Fiat')], default='value2')
    
    submit = SubmitField('Buy')

    #def validate_buy(self, field):


class PaymentForm(FlaskForm):
    """
    Form for clients to initiate deposit
    """
    fiat_amount = FloatField('Deposit Amount ($)',validators=[
                        DataRequired(),
                        NumberRange(min=1.00, message="Message must deposit at least $1.00")
                    ])
    submit = SubmitField('Deposit')


class TradeForm(FlaskForm):
    """
    Form for clients to initiate trade
    """
    response = urllib2.urlopen('https://api.coinbase.com/v2/prices/BTC-USD/spot')
    data = json.load(response)
    exchange_rate = float(data['data']['amount'])
    is_buy = RadioField(choices=[('buy','Buy'),('sell','Sell')])
    btc_amount = FloatField("Trade Amount ( \u0E3F )",validators=[
                        DataRequired(),
                        NumberRange(min=0.01, message="Message must deposit at least \u0E3F0.01")
                    ])
    xchange = HiddenField(default=exchange_rate)
    commish_type = RadioField("Commission Method",choices=[('usd','USD'),('btc','BTC')])
    commish_amount = HiddenField()
    fiat_bal = HiddenField()
    btc_bal = HiddenField()
    submit = SubmitField('Trade')

    def validate(self):
        if not super(TradeForm, self).validate():
            return False

        result = True
        btc_total = 0.0
        usd_total = 0.0

        if self.is_buy.data == "buy":
            usd_total = float(self.btc_amount.data) * float(self.xchange.data)
        else:
            btc_total = float(self.btc_amount.data)

        if self.commish_type.data == 'usd':
            usd_total += float(self.commish_amount.data)
        else:
            btc_total += float(self.commish_amount.data) / float(self.xchange.data)

        if usd_total > float(self.fiat_bal.data):
            self.btc_amount.errors.append("You do not have enough USD to complete.")
            result = False

        if btc_total > float(self.btc_bal.data):
            self.btc_amount.errors.append("You do not have enough BTC to complete.")
            result = False

        print("%0.3f %0.3f %0.3f %0.3f" % (usd_total, btc_total,
                                           float(self.fiat_bal.data),
                                           float(self.btc_bal.data)))

        return result
