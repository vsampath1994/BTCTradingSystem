from flask import Blueprint

manager = Blueprint('manager', __name__)

from . import views

manager.mock_transaction_list = [
    {'xid': 1, 'isBuy': True, 'status':'closed' , 'btc_amount':1.0 , 'commission': 0.05, 'timestamp': '2015-10-10 09:00', 'xchange': 6310.00, 'fiatAmount': 2000.00},
    {'xid': 2, 'isBuy': False, 'status':'pending' , 'btc_amount':1.2 , 'commission': 0.08, 'timestamp': '2015-10-10 09:15', 'xchange': 6350.00, 'fiatAmount': 2000.00},
    {'xid': 3, 'isBuy': True, 'status':'cancelled' , 'btc_amount':1.1 , 'commission': 0.10, 'timestamp': '2015-10-10 09:20', 'xchange': 6200.00, 'fiatAmount': 2000.00},
]

manager.mock_deposit_list = [
    {'xid': 1, 'status':'closed' , 'fiatAmount':1000 , 'timestamp': '2015-10-10 09:00' },
    {'xid': 2, 'status':'cancelled' , 'fiatAmount':500 ,  'timestamp': '2015-10-10 09:15' },
    {'xid': 3, 'status':'pending' , 'fiatAmount':2200 , 'timestamp': '2015-10-10 09:20'},
]

manager.mock_order_searches = [
    {'xid': 3, 'isBuy': True, 'status':'cancelled' , 'btc_amount':1.1 , 'commission': 0.10, 'timestamp': '2015-10-10 09:20', 'xchange': 6200.00, 'fiatAmount': 2000.00},
]

manager.mock_deposit_searches = [
    {'xid': 2, 'status':'cancelled' , 'fiatAmount':500 ,  'timestamp': '2015-10-10 09:15' },
]

