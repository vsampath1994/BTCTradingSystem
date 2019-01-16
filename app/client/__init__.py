from flask import Blueprint

client = Blueprint('client', __name__)

from . import views

client.mock_transaction_list = [
    {'type': 'buy', 'status':'closed' , 'amount':1.0 , 'commission': 0.05, 'time': '2015-10-10 09:00', 'exchange': 6310.00},
    {'type': 'sell', 'status':'pending' , 'amount':1.2 , 'commission': 0.08, 'time': '2015-10-10 09:15', 'exchange': 6350.00},
    {'type': 'buy', 'status':'cancelled' , 'amount':1.1 , 'commission': 0.10, 'time': '2015-10-10 09:20', 'exchange': 6200.00},
]

client.mock_deposit_list = [
    { 'status':'closed' , 'amount':1000 , 'time': '2015-10-10 09:00' },
    {'status':'cancelled' , 'amount':500 ,  'time': '2015-10-10 09:15' },
    {'status':'pending' , 'amount':2200 , 'time': '2015-10-10 09:20'},
]

client.account = { 'btc_balance' : 2.0,  'fiat_balance' : 2000, 'status' : 'gold', 'commish' : 5.00}
