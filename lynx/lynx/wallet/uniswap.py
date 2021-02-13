from flask import current_app as app
from web3 import Web3
from lynx.wallet.helper import getChainId, convertAmountToWei, getContractAddress, getW3, getContractAbiJson, getContract
from lynx.wallet.wallet import approve, isApproved
import datetime, time

def tradeToken(token_symbol, token_amount, userWall):

    return True