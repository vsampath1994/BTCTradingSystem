# app/auth/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import User


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an user to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        print form.client_info.data
        if form.client_info.data == 'Client':
            user_tp = User.CLIENT
        else:
            user_tp = User.TRADER
        user = User(username=form.username.data,
                      password=form.password.data,
                      user_type=user_tp,
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

        # add user to the database
        db.session.add(user)
        # if user is client, add to client table
        print form.client_info.data
        # if user is trader, add to trader table
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an user in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether user exists in the database and whether
        # the password entered matches the password in the database
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(
                form.password.data):
            # log user in
            login_user(user)

            # redirect to the dashboard page after login
            if user.user_type == User.MANAGER:
                return redirect(url_for('manager.home'))
            else:
                # if user is client, redirect to client dashboard
                if user.user_type == User.CLIENT:
                    return redirect(url_for('client.home'))
                # if user is trader, redirect to trader dashboard
                else:
                    return redirect(url_for('trader.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid username or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an user out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))
