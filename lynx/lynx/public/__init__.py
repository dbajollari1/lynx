from flask import Blueprint

bp = Blueprint('public', __name__)

from lynx.public import routes
