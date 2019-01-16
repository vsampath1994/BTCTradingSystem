from flask import abort, flash, redirect, render_template, request, url_for, session, current_app, Flask
from flask_login import current_user, login_required

from . import manager
from forms import SearchForm, ClientTraderForm
from .. import db
from ..models import User, Order, Payment


import sqlalchemy as sa
from sqlalchemy import func,desc
from sqlalchemy.sql.expression import and_

from ..utils import calculateAverage, convertToDailyHistogramData, convertToWeeklyHistogramData, convertToMonthlyHistogramData
from datetime import datetime, timedelta
from dateutil.relativedelta import *

import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

def check_manager():
    if current_user.user_type != User.MANAGER:
        abort(403)

@manager.route('/clients', methods=['GET','POST'])
@login_required
def list_clients():
    check_manager()
    clients = User.query.filter_by(user_type=User.CLIENT)

    return render_template('manager/clients/clients.html', clients=clients, title="Clients")

@manager.route('/traders', methods=['GET', 'POST'])
@login_required
def list_traders():
    check_manager()
    traders = User.query.filter_by(user_type=User.TRADER)

    return render_template('manager/traders/traders.html', traders=traders, title='Traders')

@manager.route('/add_client', methods=['GET', 'POST'])
@login_required
def add_client():
    check_manager()
    add_client = True

    form = ClientTraderForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                      password=form.password.data,
                      user_type=User.CLIENT,
                      first_name=form.first_name.data,
                      last_name=form.last_name.data,
                      phone_number=form.phone_number.data,
                      cell_number=form.cell_number.data,
                      email=form.email.data,
                      street=form.street.data,
                      city=form.city.data,
                      state=form.state.data,
                      zip_code=form.zip_code.data,
                      gold_status=False,
                      btc_balance=0,
                      fiat_balance=0)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Successfully added a new client')
        except:
            flash('Error: client already exists')
        return redirect(url_for('manager.list_clients'))

    return render_template('manager/clients/client.html', action='Add', add_client=add_client, form=form, title="Add Client")

@manager.route('/add_trader', methods=['GET','POST'])
@login_required
def add_trader():
    check_manager()
    add_client = True

    form = ClientTraderForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                      password=form.password.data,
                      user_type=User.TRADER,
                      first_name=form.first_name.data,
                      last_name=form.last_name.data,
                      phone_number=form.phone_number.data,
                      cell_number=form.cell_number.data,
                      email=form.email.data,
                      street=form.street.data,
                      city=form.city.data,
                      state=form.state.data,
                      zip_code=form.zip_code.data,
                      gold_status=False,
                      btc_balance=0,
                      fiat_balance=0)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Successfully added a new trader')
        except:
            flash('Error: trader already exists')
        return redirect(url_for('manager.list_traders'))

    return render_template('manager/traders/trader.html', action='Add', add_trader=add_trader, form=form, title="Add Trader")


@manager.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    """
    Render the dashboard template of manager
    """
    if current_user.user_type != User.MANAGER:
        abort(403)

    orders = db.session.query(Order).order_by(desc(Order.timestamp)).limit(25).all()
    payments = db.session.query(Payment).order_by(desc(Payment.timestamp)).limit(25).all()

    return render_template('manager/home.html', title='Dashboard', orders=orders, payments=payments)

@manager.route('/search', methods=['GET'])
@login_required
def search():
    """
    Render transactions search list
    """
    if current_user.user_type != User.MANAGER:
        abort(403)

    data = request.args

    startDate = data['Start Date']
    startDate = startDate + ' 00:00:00'

    endDate = data['End Date']
    endDate = endDate + ' 23:59:59'

    orderResults = db.session.query(Order).filter(and_(Order.timestamp <= endDate, Order.timestamp >= startDate)).order_by((Order.timestamp))
    depositResults = db.session.query(Payment).filter(and_(Payment.timestamp <= endDate, Payment.timestamp >= startDate)).order_by((Payment.timestamp))

    avgDict = calculateAverage(startDate, endDate, orderResults.count() + depositResults.count())
    dailyVolume = convertToDailyHistogramData(endDate, startDate, orderResults, depositResults)
    weeklyVolume = convertToWeeklyHistogramData(startDate, dailyVolume)
    monthlyVolume = convertToMonthlyHistogramData(startDate, weeklyVolume)

    return render_template('manager/search_results.html', title='Search Results',
                           orders=orderResults, payments=depositResults,
                           averages=avgDict,
                           dailyVolume=dailyVolume,
                           weeklyVolume=weeklyVolume,
                           monthlyVolume=monthlyVolume)

def updateClientStatus():
    import logging

    log = logging.getLogger('apscheduler.executors.default')
    log.setLevel(logging.INFO)  # DEBUG

    fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    h = logging.StreamHandler()
    h.setFormatter(fmt)
    log.addHandler(h)

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


def triggerScheduler():
    #clients = User.query.filter_by(user_type=User.CLIENT)

    #currentDate = datetime.now()
    #fromDate = currentDate + relativedelta(months=-1)

    #for client in clients:
        #ordersByMonth = Order.query.filter(and_(Order.timestamp <= currentDate, Order.timestamp >= fromDate)).filter_by(clientId=client.id)
        #if ordersByMonth.count() > 20:
            #client.gold_status = 1
        #else:
            #client.gold_status = 0

    #db.session.commit()
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=updateClientStatus)
    scheduler.start()

@manager.route('/update_client_status', methods=['POST'])
@login_required
def update_client_status():
    triggerScheduler()
    return redirect(url_for('manager.home'))

