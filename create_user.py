from app.models import User
from app import db

import random

def create_manager():
    manager = User(id=10000,email="abc@def.com", username='manager', password='bitcoin', user_type=User.MANAGER)
    db.session.add(manager)
    db.session.commit()

def create_clients():
    for i in range(0, 100):
        if i%350 == 0:
            goldStatus = True
        else:
            goldStatus = False

        client = User(username='abc' + str(i),
                      password='hacker',
                      user_type=User.CLIENT,
                      first_name='testfirst' + str(i),
                      last_name='testlast' + str(i),
                      phone_number='469422929' + str(i),
                      cell_number='469422929' + str(i),
                      email='testfirst' + str(i) + '@' + 'testlast.com',
                      street='742' + str(i) + 'frankford rd',
                      city='dallas',
                      state='texas',
                      zip_code='7525' + str(i),
                      gold_status=goldStatus,
                      btc_balance=random.uniform(1, 100),
                      fiat_balance=random.uniform(10000, 1000000))
        db.session.add(client)
        db.session.commit()

def create_traders():
    for i in range(0, 100):
        client = User(username='trader' + str(i),
                      password='hacker',
                      user_type=User.TRADER,
                      first_name='traderfirst' + str(i),
                      last_name='traderlast' + str(i),
                      phone_number='469422900' + str(i),
                      cell_number='469422900' + str(i),
                      email='traderfirst' + str(i) + '@' + 'traderlast.com',
                      street='111' + str(i) + 'frankford rd',
                      city='dallas',
                      state='texas',
                      zip_code='7525' + str(i),
                      gold_status=False,
                      btc_balance=random.uniform(1, 100),
                      fiat_balance=random.uniform(10000, 1000000))
        db.session.add(client)
        db.session.commit()
