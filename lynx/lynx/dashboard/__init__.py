from flask import Blueprint

bpDasboard = Blueprint('dashboard', __name__)

from lynx.dashboard import routes
