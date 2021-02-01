from flask import Blueprint

bp = Blueprint('errors', __name__)

from lynx.errors import handlers
