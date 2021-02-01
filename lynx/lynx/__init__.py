from flask import Flask, render_template, request, redirect, url_for, flash, session, redirect
from lynx.config import Config
import logging
import logging.handlers
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from lynx.services.mail_api import send_email

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = app.config['SECRET_KEY']

    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from lynx.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from lynx.dashboard import bpDasboard as dashboard_bp
    app.register_blueprint(dashboard_bp)

    from lynx.auth import bpAuth as auth_bp
    app.register_blueprint(auth_bp)

    from lynx.public import bp as public_bp
    app.register_blueprint(public_bp)

    from lynx.products import bpProducts as products_bp
    app.register_blueprint(products_bp)

    #setup logger
    app.logger = logging.getLogger(__name__)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(user)s : %(message)s [in %(pathname)s:%(lineno)d in %(funcName)s]')
    
    #write to error file (lynx.log) handler
    app.logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler('lynx.log', maxBytes=1024 * 1024, backupCount=3)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    #email the error (see SUPPORT key in config.py)
    emailHandler = EmailLogHandler(app.config['SUPPORT'])
    emailHandler.setLevel(logging.ERROR)
    emailHandler.setFormatter(formatter)
    app.logger.addHandler(emailHandler)

    with app.app_context():
	    db.create_all()

    return app

class EmailLogHandler(logging.Handler):
    def __init__(self, supportEmail):
        logging.Handler.__init__(self)
        self.supportEmail = supportEmail

    def emit(self, record):
        try:
            msg = self.format(record)
            if (str(msg).find('***SEND EMAIL FAILED***') == -1): #send email failed, dont try again
                htmlBody = '<h4 style="color:red;">' + msg + '</hr>'
                send_email('LynX - ERROR', self.supportEmail, '', htmlBody)
        except Exception as ex:
            print(ex)

