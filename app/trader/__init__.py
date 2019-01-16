from flask import Blueprint

trader = Blueprint('trader', __name__)

from . import views
