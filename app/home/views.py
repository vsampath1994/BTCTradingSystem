# app/home/views.py

from flask import render_template, abort, redirect, url_for
from flask_login import current_user, login_required

from . import home
from ..models import User

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")

@home.route('/client/dashboard')
@login_required
def client_dashboard():
    """
    Render the client dashboard template on the /client/dashboard route
    """
    #return render_template('client/client_home.html', title="Dashboard")
    return redirect(url_for('client.home'))
