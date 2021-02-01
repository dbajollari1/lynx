from flask import current_app as app
import sqlite3
import gc
import datetime
from flask import g
#from passlib.hash import sha256_crypt

def open_connection():
    connection = getattr(g, '_connection', None)
    if connection == None:
        connection = g._connection = sqlite3.connect(app.config['SQLITE_PATH'])
    connection.row_factory = sqlite3.Row
    return connection

def execute_sql(sql, values=(), commit=False, single=False):
    connection = open_connection()
    cursor = connection.execute(sql, values)
    if commit == True:
        results = connection.commit()
    else:
        results = cursor.fetchone() if single else cursor.fetchall()

    cursor.close()
    return results

# ----- mysql db code-----------
# import MySQLdb #run '------> pip install mysqlclient' to add package
# def connection():
#     conn = MySQLdb.connect(host='localhost',
#                            user = 'root',
#                            passwd = 'ryan1111',
#                            db = 'arianb$fl')
#     c = conn.cursor()
#     return c, conn
# ---- end mysql db code----------