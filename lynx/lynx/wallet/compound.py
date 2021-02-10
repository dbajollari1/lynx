from eth_wallet import Wallet
from eth_wallet.utils import generate_entropy
from lynx.wallet.models import CompoundData
from lynx.dashboard.models import UserTransaction
import json
import requests
from web3 import Web3
from decimal import Decimal
import os
import datetime
from flask import current_app as app
import math
from lynx.wallet.helper import *

def getCompaundBalance(addr, erc20Token):
    cdata = CompoundData
    cdata.current_balance = 0
    cdata.interest_accrued = 0
    cdata.ctoken_balance = 0
    symbol = 'c' + erc20Token.upper()

    w3 =getW3()
    contract_address = getContractAddress(symbol)
    abi_json = getContractAbiJson(symbol)
    abi = abi_json[symbol]
    compound_token_contract = getContract(w3,abi,contract_address) 

    user_underlyingbalance = compound_token_contract.functions.balanceOfUnderlying(addr).call()

    cdata.symbol = symbol.replace('c', '', 1) # underlying symbol (not compound symbol)
    cdata.current_balance = convertAmountFromWei(cdata.symbol, user_underlyingbalance)
    cdata.interest_accrued = 0

    return cdata

# Using etherscan API to get user transactions
def getUserTransactions(addr, erc20Token):
    addr = addr.lower()
    if app.config['NET'] == 'mainnet':
        apiEndPoint = 'https://api.etherscan.io/api?module=account&action=tokentx&address=' + addr + '&startblock=0&endblock=999999999&sort=asc&apikey=' + app.config['ETHSCANM']
    else:
        apiEndPoint = 'https://api-ropsten.etherscan.io/api?module=account&action=tokentx&address=' + addr + '&startblock=0&endblock=999999999&sort=asc&apikey=' + app.config['ETHSCANR']
    
    headers = {
        'User-Agent': 'chrome'  
    }
    trans = requests.get(apiEndPoint, headers=headers) # headers required for ropsten as it fails !!!
    jsonData = trans.json()

    transactionList=[]
    compTokenContract = getContractAddress('c' + erc20Token).lower()

    for transaction in jsonData['result']:
        if transaction['tokenSymbol'] == erc20Token: # or transaction['tokenSymbol'] == 'c' + erc20Token:
            userTran = UserTransaction()
            show = False

            if transaction['from'].lower() == addr.lower() and transaction['to'].lower() == compTokenContract: # from user to contract
                userTran.transactionType = "Deposit"
                show = True
            elif transaction['from'].lower() == compTokenContract and transaction['to'].lower() == addr: # from contract to user
                userTran.transactionType = "Withdraw"
                show = True

            if show == True:
                ts = transaction['timeStamp']
                userTran.transactionDate = str(datetime.datetime.utcfromtimestamp(int(ts))) + ' UTC'
                tokenDecimal = transaction['tokenDecimal']
                amt = Decimal(transaction['value']) / 10 ** Decimal(tokenDecimal)
                userTran.transactionAmt = str(round(amt, 2))
                transactionList.append(userTran)

    return transactionList

# Deposit to Compound
def mintErcToken(amt, symbol, wallFrom):
    w3 =getW3()
    contract_address = getContractAddress('c' + symbol)
    abi_json = getContractAbiJson('c' + symbol)
    abi = abi_json['c' + symbol]
    compound_token_contract = getContract(w3, abi, contract_address)
    nonce = w3.eth.getTransactionCount(wallFrom.address)

    amount = convertAmountToWei(symbol, amt) # convert in underlying token balance (USDT and not cUSDT)
    mint_tx = compound_token_contract.functions.mint(int(amount)).buildTransaction({
        'chainId': getChainId(), # 1 for mainnet, 3 for ropsten
        'gas': 500000,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': nonce
    })
    signed_txn = w3.eth.account.sign_transaction(mint_tx, wallFrom.PrivateKey)
    try:
        tx = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return tx.hex()
    except ValueError as err:
        #return (json.loads(str(err).replace("'", '"')), 402, {'Content-Type': 'application/json'})
        return 'Error: ' + str(err)

# Withdraw from Compound
def redeemErcToken(amt, symbol, wallFrom):
    w3 =getW3()
    contract_address = getContractAddress('c' + symbol)
    abi_json = getContractAbiJson('c' + symbol)
    abi = abi_json['c' + symbol]
    compound_token_contract = getContract(w3, abi, contract_address)
    nonce = w3.eth.getTransactionCount(wallFrom.address)

    amount =  convertAmountToWei(symbol, amt)
    redeem_tx = compound_token_contract.functions.redeemUnderlying(int(amount)).buildTransaction({
        'chainId': getChainId(), # 1 for mainnet, 3 for ropsten
        'gas': 500000,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': nonce
    })

    signed_txn = w3.eth.account.sign_transaction(redeem_tx, wallFrom.PrivateKey)
    try:
        tx = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return tx.hex()
    except ValueError as err:
        #return (json.loads(str(err).replace("'", '"')), 402, {'Content-Type': 'application/json'})
        return 'Error: ' + str(err)

# Compound APY
def getTokenAPR(erc20Token):
    symbol = 'c' + erc20Token.upper()
    w3 =getW3()
    contract_address = getContractAddress(symbol)
    abi_json = getContractAbiJson(symbol)
    abi = abi_json[symbol]
    compound_token_contract = getContract(w3,abi,contract_address) 

    Rate = compound_token_contract.functions.supplyRatePerBlock().call()
    ETH_Mantissa = 1 * 10 ** 18 # (ETH has 18 decimal places)
    BlocksPerDay = 4 * 60 * 24 # (based on 4 blocks occurring every minute)
    DaysPerYear = 365

    APY = (((Rate / ETH_Mantissa * BlocksPerDay + 1) ** DaysPerYear) - 1) * 100 # not same as compound website formula!!!
    #APY = (((math.pow((Rate / ETH_Mantissa * BlocksPerDay) + 1, DaysPerYear - 1))) - 1) * 100
    return APY