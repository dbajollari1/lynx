import os


class Config(object):
    SECRET_KEY = 'vfr'
    ADMINS = 'abajollari@yahoo.com'
    MJ_APIKEY_PUBLIC = '077fc21857d31f1f416fbf1ab7477164'
    MJ_APIKEY_PRIVATE = '03caddedf8edb44156d03585242e359a'
    MJ_EMAIL = 'arianb1@hotmail.com'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/lynx.sqlite'
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:Sdav@1234@localhost:3306/lynx'  # ***must run:  pip install mysqlclient
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SUPPORT = 'abajollari@yahoo.com'
    ETHSCANR = 'ASFQIXUSZJRKFICTNWYVX8G7TI11WZ9FDD'
    ETHSCANM = 'WIUA9D4APWKWMKDQGTW7BXSPMRN9EEA1DQ'
    # RUNENV = 'W' # W-Windows; L-Linux
    NET = 'kovan'  # kovan ropsten
    SYMB = 'DAI'  # 'USDT'
    PROTOCOL = 'AAVE'  # COMP - Compound / AAVE - Aave / ...

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
        'MKR': 'Maker Token'
    }
