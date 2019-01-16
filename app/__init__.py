# app/__init__.py

# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from dateutil.relativedelta import *
import sqlalchemy as sa
from sqlalchemy import func,desc
from sqlalchemy.sql.expression import and_

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()


# after the db variable initialization
login_manager = LoginManager()

def updateClientStatus():
    import logging

    log = logging.getLogger('apscheduler.executors.default')
    log.setLevel(logging.INFO)  # DEBUG

    fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    h = logging.StreamHandler()
    h.setFormatter(fmt)
    log.addHandler(h)

    from models import User, Order
    with db.app.app_context():
        clients = User.query.filter_by(user_type=User.CLIENT)

        currentDate = datetime.now()
        fromDate = currentDate + relativedelta(months=-1)

        for client in clients:
            ordersByMonth = Order.query.filter(and_(Order.timestamp <= currentDate, Order.timestamp >= fromDate)).filter_by(clientId=client.id)
            if ordersByMonth.count() > 20:
                client.gold_status = 1
            else:
                client.gold_status = 0

        db.session.commit()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.app = app
    db.init_app(app)

    #@app.route('/')
    #def hello_world():
    #    return 'Under construction'

    login_manager.init_app(app)
    #login_manager.login_message("You must be logged in to access this page.")
    login_manager.login_view = "auth.login"

    migrate = Migrate(app, db)

    Bootstrap(app)

    from app import models

    from .manager import manager as manager_blueprint
    app.register_blueprint(manager_blueprint, url_prefix='/manager')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .client import client as client_blueprint
    app.register_blueprint(client_blueprint)

    #vsampath
    from .trader import trader as trader_blueprint
    app.register_blueprint(trader_blueprint)
    #vsampath

    scheduler = BackgroundScheduler()
    scheduler.add_job(updateClientStatus, 'cron', month='1-12', day='last', hour='23', minute='55')
    scheduler.start()

    return app
