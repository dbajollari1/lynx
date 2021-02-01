from lynx.dataaccess.db_helper import execute_sql
from lynx.dashboard.models import Dashboard, UserTransaction
from lynx.wallet.models import LynxWall
import datetime

def getDashboardData():
    dashboardData = Dashboard(1, 5723.54, 223.54, 26.53)
    return dashboardData

def getTransactiondData(userId):
    transactionList=[]
    sql = "SELECT usertran.transactionId, usertran.transactionAmt, usertran.transactionType, usertran.transactionDate FROM usertran WHERE usertran.userId = ? ORDER BY usertran.transactionDate"
    userTrans = execute_sql (sql, (userId,), False, False)

    for row in userTrans:
        userTran = UserTransaction()
        userTran.transactionId = int(row['transactionId'])
        userTran.transactionAmt = row['transactionAmt']
        userTran.transactionType = row['transactionType']
        userTran.transactionDate = row['transactionDate']
        transactionList.append(userTran)
        
    return transactionList

def saveWallet(wall): 
    sql = 'INSERT into lynxwall (userId, mnemonic, privateKey, publicKey, address, createdBy, createdOn) VALUES (?, ?, ?, ?, ?, ?, ?)'
    execute_sql (sql, (wall.UserId, wall.Mnemonic, wall.PrivateKey, 
    wall.PublicKey, wall.Address, 'sys',datetime.datetime.utcnow()), True)


def getWalletInfo(uid):
    # sql = 'SELECT * from event where id = ?'
    # row = execute_sql (sql, (event_id,), False, True)
    sql = 'Select lynxwall.mnemonic, lynxwall.privateKey, lynxwall.publicKey, lynxwall.address FROM lynxwall WHERE lynxwall.userId = ?'
    row = execute_sql (sql,(uid,), False, True)
    if not row == None:
        event = LynxWall()
        event.Mnemonic = row['mnemonic']
        event.PrivateKey = row['privateKey']
        event.PublicKey = row['publicKey']
        event.Address = row['address']
        return event
