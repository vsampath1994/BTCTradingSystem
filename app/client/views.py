from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from forms import PaymentForm
from datetime import datetime
from ..models import Payment, Order
from .. import db

from . import client
from .. import db
from forms import TradeForm
from ..models import User

@client.route('/traders', methods=['GET', 'POST'])
@login_required
def list_traders():

    traders = User.query.filter_by(user_type=User.TRADER)

    return render_template('client/traders.html', traders=traders, title='Available Traders')

@client.route('/client/home')
@login_required
def home():
    """
    Render the home template of client
    """
    if current_user.user_type != User.CLIENT:
        abort(403)

    payments_ = Payment.query.filter_by(clientId=current_user.id)
    trades_ = Order.query.filter_by(clientId=current_user.id)
    account_x = User.query.filter_by(id=current_user.id).first()
    account_ = { 'btc_balance' : float(account_x.btc_balance),
                'fiat_balance' : float(account_x.fiat_balance),
                 'status' : account_x.gold_status,
                 'commish' : 5.00 if account_x.gold_status else 10.0
                }
    
    return render_template('client/client_home.html',
                           title='Client Home',
                           transactions= trades_,
                           deposits = payments_,
                           account= account_)

@client.route('/client/payment',methods=['GET', 'POST'])
@login_required
def payment():
    """
    Render the deposit form for client
    """
    if current_user.user_type != User.CLIENT:
        abort(403)

    form = PaymentForm()

    if form.validate_on_submit():
        payment = Payment(status='pending',
                          fiatAmount = form.fiat_amount.data,
                          clientId = current_user.id,
                          traderId = 0,
                          timestamp = datetime.now()
                        )

        db.session.add(payment)
        db.session.commit()
        flash('You have successfully submitted a payment request.  A trader will confirm shortly.'
              , 'success')
        return redirect(url_for('client.home'))

    return render_template('client/client_payment.html',
                           title='Client Payment',
                           account= client.account,
                           form=form)


@client.route('/client/trade',methods=['GET', 'POST'])
@login_required
def trade():
    """
    Render the deposit form for client
    """
    if current_user.user_type != User.CLIENT:
        abort(403)

    account_x = User.query.filter_by(id=current_user.id).first()
    account_ = { 'btc_balance' : float(account_x.btc_balance),
                'fiat_balance' : float(account_x.fiat_balance),
                 'status' : account_x.gold_status,
                 'commish' : 5.00 if account_x.gold_status else 10.0
                }

    form = TradeForm()

    if form.validate_on_submit():
        commish_ = float(form.commish_amount.data) if form.commish_type.data == 'usd'\
            else float(form.commish_amount.data) / float(form.xchange.data)

        trade = Order(status='pending',
                          btc_amount = form.btc_amount.data,
                          isBuy = (form.is_buy.data == 'buy'),
                          xchange = form.exchange_rate,
                          comm_type = form.commish_type.data,
                          comm_amount = commish_,
                          clientId = current_user.id,
                          timestamp = datetime.now()
                        )

        db.session.add(trade)
        db.session.commit()
        flash('You have successfully submitted a trade request.  A trader will confirm shortly.'
              , 'success')
        return redirect(url_for('client.home'))

    return render_template('client/client_trade.html',
                           title='Client Trade',
                           account= account_,
                           form=form)
