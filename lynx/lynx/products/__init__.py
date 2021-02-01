from flask import Blueprint

bpProducts = Blueprint('products', __name__)

from lynx.products import routes
