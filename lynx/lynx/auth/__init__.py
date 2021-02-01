from flask import Blueprint

bpAuth = Blueprint('auth', __name__)

from lynx.auth import routes