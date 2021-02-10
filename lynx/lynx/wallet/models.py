class CompoundData:
  def __init__(self, userId = 0, symbol='', principal=0, current_balance=0, interest_accrued=0, 
  ctoken_balance=0, amount_ToMint=0, amount_Minted=0, Txid='', apy=0):
    self.userId = userId
    self.symbol = symbol
    self.principal = principal
    self.current_balance = current_balance
    self.interest_accrued = interest_accrued
    self.ctoken_balance = ctoken_balance
    self.amount_ToMint = amount_ToMint
    self.amount_Minted = amount_Minted
    self.Txid = Txid
    self.apy = apy
