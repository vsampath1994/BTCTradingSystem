# app/models.py

from flask_login import UserMixin
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class User(UserMixin, db.Model):
    """
    Create a User Table
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    email = db.Column(db.String(255))
    user_type = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    cell_number = db.Column(db.String(255))
    street = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zip_code = db.Column(db.String(255))
    btc_balance = db.Column(db.Float, default=0)
    fiat_balance = db.Column(db.Float, default=0)
    gold_status = db.Column(db.Boolean, default=False)

    MANAGER = 1
    CLIENT = 2
    TRADER = 3


    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)


    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Payment(db.Model):
    """
    Create Payments table
    """
    __tablename__ = 'payments'
    xid = db.Column(db.Integer, primary_key=True);
    status = db.Column(db.String(255), nullable=False)
    fiatAmount = db.Column(db.Float(), default=0)
    clientId = db.Column(db.Integer, ForeignKey('users.id'))
    traderId = db.Column(db.Integer, ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Payment: {}>'.format(self.xid)

class Order(UserMixin, db.Model):
    """
    Create Orders table
    """
    __tablename__ = 'orders'
    xid = db.Column(db.Integer, primary_key=True);
    status = db.Column(db.String(255), nullable=False)
    isBuy = db.Column(db.Boolean, default=False, nullable=False)
    btc_amount = db.Column(db.Float, default=0, nullable=False)
    xchange = db.Column(db.Float)
    comm_type = db.Column(db.String(255), nullable=False)
    comm_amount = db.Column(db.Float, nullable=False)
    clientId = db.Column(db.Integer, ForeignKey('users.id'))
    traderId = db.Column(db.Integer, ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Order: {}>'.format(self.xid)

class ChangeLog(UserMixin, db.Model):
    """
    Create log table
    """
    __tablename__ = 'changelog'
    lid = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    xid = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(255), nullable=False)
    xid_type = db.Column(db.String(255), nullable=False)
    clientId = db.Column(db.Integer)
    traderId = db.Column(db.Integer)

    def __repr__(self):
        return '<Change Log: {}>'.format(self.lid)
