from eth_wallet import Wallet
from eth_wallet.utils import generate_entropy
import json
import requests
from web3 import Web3
from decimal import Decimal
import datetime
from flask import current_app as app
import math
from lynx.wallet.helper import getW3, getContractAddress, getContractAbiJson, getContract, getChainId, convertAmountToWei, convertAmountFromWei

# Create a new wallet and save wallet info to db
def generateWallet(uid):
    # 128 strength entropy
    ENTROPY = generate_entropy(strength=128)
    w3 = getW3()
    acc = w3.eth.account.create(ENTROPY) #, 12, 'english', "m/44''/60'/0'/0/0")
    # print(acc)
    
    # return wallet info to be saved to db
    # wallet = UserWallet(id=uid, mnemonic='xxx yyy zzz', privateKey=str(acc._key_obj), publicKey='pbkey', address=acc.address, createdBy='lynx')
    return str(acc._key_obj), acc.address  #wallet

# get balance of a specified ERC20 token in a wallet
def getWalletTokenBalance(addr, erc20Token):
    w3 = getW3()
    contract_address = getContractAddress(erc20Token)
    abi_json = getContractAbiJson('ERC20')
    abi = abi_json
    erc20_token_contract = getContract(w3, abi, contract_address)

    raw_balance = erc20_token_contract.functions.balanceOf(addr).call()
    return convertAmountFromWei(erc20Token, raw_balance)

# get balance of Eths in a wallet
def getEthBalance(addr):
    w3 =getW3()
    bal = w3.eth.getBalance(addr)
    return w3.fromWei(bal, 'ether')

# Transfer Eth between wallets
def transferEth(fromAddr, toAddr, amt, key):
    try:
        w3 =getW3()
        nonce = w3.eth.getTransactionCount(fromAddr)
        tx = {
            'nonce': nonce,
            'to': toAddr,
            'value': w3.toWei(amt, 'ether'),
            'gas': 2000000,
            'gasPrice': w3.toWei('50', 'gwei'),
        }
        signed_tx = w3.eth.account.signTransaction(tx, key)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return w3.toHex(tx_hash)
    except Exception as ex:
        return str(ex)

# Transfer ERC20 tokens between wallets
def transferERCToken(fromAddr, toAddr, amt, key, symbol):
    try:
        w3 =getW3()
        
        availableBalance = getWalletTokenBalance(fromAddr, symbol)
        if amt > availableBalance:
            return 'Error: Not enough funds.'

        contract_address = getContractAddress(symbol)
        abi_json = getContractAbiJson('ERC20')
        abi = abi_json
        erc20_token_contract = getContract(w3, abi, contract_address)

        nonce = w3.eth.getTransactionCount(fromAddr)
        amount =  convertAmountToWei(symbol, amt)
        transfer_tx = erc20_token_contract.functions.transfer(toAddr, int(amount)).buildTransaction({
                'chainId': getChainId(), # 1 for mainnet, 3 for ropsten
                'gas': 500000,
                'gasPrice': w3.toWei('20', 'gwei'),
                'nonce': nonce
            })
        signed_txn = w3.eth.account.sign_transaction(transfer_tx, key)
        try:
            tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            return w3.toHex(tx_hash)
        except ValueError as err:
            return 'Error: ' + str(err)

    except Exception as ex:
        return 'Error: ' + str(ex)