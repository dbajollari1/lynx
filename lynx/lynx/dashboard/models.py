class Dashboard:
  def __init__(self, accountId = 0, accountBalance=0, interestPaid=0, accruedInterest=0):
    self.accountId = accountId
    self.accountBalance = accountBalance
    self.interestPaid = interestPaid
    self.accruedInterest = accruedInterest

class UserTransaction:
  def __init__(self, transactionId = 0, userId = 0, transactionAmt=None, transactionType=None, transactionDate=None):
    self.transactionId = transactionId
    self.userId = userId
    self.transactionAmt = transactionAmt
    self.transactionType = transactionType
    self.transactionDate = transactionDate
