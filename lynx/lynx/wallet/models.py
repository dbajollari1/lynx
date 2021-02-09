class LynxWall:
  def __init__(self, UserId = 0, Mnemonic=None, PrivateKey=None, PublicKey=None, Address=None):
    self.UserId = UserId
    self.Mnemonic = Mnemonic
    self.PrivateKey = PrivateKey
    self.PublicKey = PublicKey
    self.Address = Address

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

class UniswapData:
  def __init__(self, amountOut = 0, amountInMax = 0, path = '', to = '', deadline = 0):
    self.amountOut = amountOut
    self.amountInMax = amountInMax
    self.path = path
    self.to = to
    self.deadline = deadline
 
    