import datetime

from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from sqlalchemy.sql.expression import and_
from sqlalchemy import func, desc

import sqlalchemy as sa

from . import trader
from .. import db
from ..models import Order,ChangeLog,User,Payment

@trader.route('/trader/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    ordersByMonth = Order.query.with_entities(sa.func.year(Order.timestamp), sa.func.month(Order.timestamp), func.count(Order.timestamp).label('count')).group_by(sa.func.year(Order.timestamp), sa.func.month(Order.timestamp)).filter_by(traderId = current_user.id)

    depositsByMonth = Payment.query.with_entities(sa.func.year(Payment.timestamp), sa.func.month(Payment.timestamp), func.count(Payment.timestamp).label('count')).group_by(sa.func.year(Payment.timestamp), sa.func.month(Payment.timestamp)).filter_by(traderId = current_user.id)

    monthlyOrderTransactions = []
    for order in ordersByMonth:
        monthTrasaction = [order[0], order[1], order[2]]
        monthlyOrderTransactions.append(order)

    
    monthlyDepositTransactions = []
    for deposit in depositsByMonth:
        monthTrasaction = [deposit[0], deposit[1], deposit[2]]
        monthlyDepositTransactions.append(deposit)

    return render_template('trader/dashboard.html', title="Dashboard", ordersByMonth=monthlyOrderTransactions, depositsByMonth=monthlyDepositTransactions)

@trader.route('/Pending_Orders', methods=['GET', 'POST'])
@login_required
def list_pendingOrders():
    pendingOrders = Order.query.filter_by(status='pending').order_by(desc(Order.timestamp))
    if pendingOrders.count() == 0:
        pendingOrders= None
    return render_template('trader/pendingOrders.html', title="Pending orders", pendingOrders=pendingOrders)

@trader.route('/Pending_Deposits', methods=['GET', 'POST'])
@login_required
def list_pendingDeposits():
    pendingDeposits = Payment.query.filter_by(status='pending').order_by(desc(Payment.timestamp))
    if pendingDeposits.count() == 0:
        pendingDeposits = None
    return render_template('trader/pendingDeposits.html', title="Pending deposits", pendingDeposits=pendingDeposits)

@trader.route('/TraderAction_Order/<string:action>/<int:xid>', methods=['GET', 'POST'])
@login_required
def traderAction_order(action, xid):
    order = Order.query.get_or_404(xid)
    client = User.query.get_or_404(order.clientId)
    if order.status == 'pending':
        btcPrice        = order.btc_amount * order.xchange
        order.traderId  = current_user.id
        if action == 'Approve' :
            if order.isBuy:
                if current_user.btc_balance >= order.btc_amount:
                    current_user.btc_balance  -= order.btc_amount
                    current_user.fiat_balance += btcPrice
                    client.btc_balance += order.btc_amount
                    client.fiat_balance -= btcPrice
                else:
                    flash("You don't have enough bitcoin!")
                    return redirect(url_for('trader.list_pendingOrders'))
            else:
                if current_user.fiat_balance >= btcPrice:
                    current_user.btc_balance  += order.btc_amount
                    current_user.fiat_balance -= btcPrice
                    client.btc_balance -= order.btc_amount
                    client.fiat_balance += btcPrice
                else:
                    flash("You don't have enough fiat amount!")
                    return redirect(url_for('trader.list_pendingOrders'))
            
            order.status = 'approved'
            flashMessage = 'You have approved the order:' + str(xid)
        elif action == 'Cancel' :
            order.status = 'cancelled'
            flashMessage = 'You have canceled the order:' + str(xid)
        
        changeLogEntry = ChangeLog(timestamp = datetime.datetime.utcnow()
                                    ,xid = xid
                                    ,status = order.status
                                    ,xid_type = "Order"
                                    ,clientId = order.clientId
                                    ,traderId = current_user.id)
        db.session.add(changeLogEntry)
        db.session.commit()

        flash(flashMessage)
    else:
        flash("The selected order is not in pending status!")
    return redirect(url_for('trader.list_pendingOrders'))

@trader.route('/TraderAction_Deposit/<string:action>/<int:xid>', methods=['GET', 'POST'])
@login_required
def traderAction_deposit(action, xid):
    payment = Payment.query.get_or_404(xid)
    if payment.status == 'pending':
        payment.traderId = current_user.id
        if action == 'Approve' :
            payment.status      = 'approved'
            client              = User.query.get_or_404(payment.clientId)
            client.fiat_balance += payment.fiatAmount
            flashMessage        = 'You have approved the deposit ID:' + str(xid)
        elif action == 'Cancel' :
            payment.status = 'cancelled'
            flashMessage   = 'You have cancelled the deposit ID:' + str(xid)
        
        changeLogEntry = ChangeLog(timestamp = datetime.datetime.utcnow()
                                    ,xid = xid
                                    ,status = payment.status
                                    ,xid_type = "Deposit"
                                    ,clientId = payment.clientId
                                    ,traderId = current_user.id)
        db.session.add(changeLogEntry)
        db.session.commit()

        flash(flashMessage)
    else:
        flash("The selected deposit is not in pending status!")
    return redirect(url_for('trader.list_pendingDeposits'))

@trader.route('/Closed_Orders', methods=['GET', 'POST'])
@login_required
def list_closedOrders():
    closedOrders    = Order.query.filter(and_(Order.status!='pending', Order.traderId==current_user.id))
    if closedOrders.count() == 0:
	closedOrders= None
    return render_template('trader/closedOrders.html', title='Closed orders', closedOrders=closedOrders)

@trader.route('/Closed_Deposits', methods=['GET', 'POST'])
@login_required
def list_closedDeposits():
    closedDeposits  = Payment.query.filter(and_(Payment.status!='pending', Payment.traderId==current_user.id))
    if closedDeposits.count() == 0:
	closedDeposits= None
    return render_template('trader/closedDeposits.html', title='Closed orders', closedDeposits=closedDeposits)


@trader.route('/ClientSearch/<int:is_search>', methods=['GET','POST'])
@login_required
def client_search(is_search=0):
    if is_search:
        formData = request.args
        if formData['Condition']:
            clients         = User.query.filter(and_(getattr(User, formData['Field']).like('%' +formData['Condition']+ '%'), User.user_type==2))
        else:
            flash("Enter some value in search key!")
            return render_template('trader/clientSearch.html', title='Find clients', is_search=0)

        return render_template('trader/clientSearch.html', title='Find clients', clients=clients, is_search=1)
    else:
        return render_template('trader/clientSearch.html', title='Find clients', is_search=0)

@trader.route('/ClientInfo/<int:id>', methods=['GET','POST'])
@login_required
def client_info(id):
    client = User.query.filter_by(id=id)
    orders = Order.query.filter_by(clientId = id).order_by(desc(Order.timestamp))
    deposits = Payment.query.filter_by(clientId = id).order_by(desc(Payment.timestamp))
    return render_template('trader/clientInfo.html', title='Client information', client=client, payments = deposits, orders = orders)
