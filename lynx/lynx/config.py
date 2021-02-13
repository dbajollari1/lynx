import os

class Config(object):
    SECRET_KEY = 'vfr'
    ADMINS = 'abajollari@yahoo.com'
    MJ_APIKEY_PUBLIC = '077fc21857d31f1f416fbf1ab7477164'
    MJ_APIKEY_PRIVATE = '03caddedf8edb44156d03585242e359a'
    MJ_EMAIL = 'arianb1@hotmail.com'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/lynx.sqlite'
    #SQLALCHEMY_DATABASE_URI = 'mysql://root:Sdav@1234@localhost:3306/lynx'  # ***must run:  pip install mysqlclient
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ST_PBK = 'pk_test_DCZF4C9gpgFyjNJQYGOYiGmx00aE0ErF94'
    ST_PVK = 'sk_test_8OGNYcJKB0TWieGnYFTlrmd700h8t0ovw6'
    ST_WEBHK = 'whsec_wV0dI8let4lPZvO68yKA9XMhjwoK7ydE'
    HOME_PAGE = 'http://127.0.0.1:5000/home'
    SITE_LOGO = 'http://127.0.0.1:5000/static/images/lynx.jpg'
    DONATE_SUCCESS_URL = 'http://127.0.0.1:5000/thanks'
    SUPPORT = 'abajollari@yahoo.com'
    ETHSCANR = 'ASFQIXUSZJRKFICTNWYVX8G7TI11WZ9FDD'
    ETHSCANM ='WIUA9D4APWKWMKDQGTW7BXSPMRN9EEA1DQ'
    RUNENV = 'W' # W-Windows; L-Linux
    NET = 'ropsten' #kovan
    SYMB = 'USDT'
    
    LANGUAGES = {
        'en': 'English',
        'sq': 'Albanian',
        'it': 'Italian',
        'el': 'Greek',
        'fr': 'French'
    }

    TOKENS = {
        'MNFLX': 'Netflix Token',
        'USDT': 'USDT Token',
        'DAI': 'DAI Token',
	'USDC': 'USDC Token'
    }