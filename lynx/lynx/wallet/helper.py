import json
from web3 import Web3
from decimal import Decimal
import os
import datetime
from flask import current_app as app
import math
from sys import platform

# Using Infura to connect to eth network


def getW3():
    network = app.config['NET']
    if network == 'mainnet':
        w3 = Web3(Web3.HTTPProvider(
            'https://mainnet.infura.io/v3/6e6af88eebca48fa8bb3ed125e554281'))
    elif network == 'kovan':
        w3 = Web3(Web3.HTTPProvider(
            'https://kovan.infura.io/v3/6e6af88eebca48fa8bb3ed125e554281'))
    else:  # ropsten
        w3 = Web3(Web3.HTTPProvider(
            'https://ropsten.infura.io/v3/6e6af88eebca48fa8bb3ed125e554281'))
    return w3


def getTokenAddress(symbol, protocol=''):

    if protocol == '':
        protocolName = app.config['PROTOCOL']
    else:
        protocolName = protocol

    if protocolName == "COMP":
        addressFile = "comp.json"
    elif protocolName == "AAVE":
        addressFile = "aave.json"
    else:
        addressFile = "uniswap.json"

    chainId = getChainId()

    if platform == "win32":
        fileName = os.getcwd() + "\\lynx\\wallet\\address\\" + addressFile
    else:
        fileName = os.getcwd() + "/lynx/wallet/address/" + addressFile

    with open(fileName) as f:
        addresses = json.load(f)

    for addr in addresses['tokens']:
        if addr['chainId'] == chainId:
            if addr['symbol'] == symbol:
                return addr['address']

    raise Exception("address not found!!!")


def getContractAbiJson(contractABI):

    # abi_url = "https://raw.githubusercontent.com/compound-finance/compound-protocol/master/networks/mainnet-abi.json"
    # abi_url = "https://raw.githubusercontent.com/compound-finance/compound-protocol/master/networks/ropsten-abi.json"
    # abi = requests.get(abi_url)

    cwd = os.getcwd()
    abiFileName = ''
    # runenv = app.config['RUNENV'] # W-Windows or L-Linux
    if platform == "win32":
        runenv = 'W'
    else:
        runenv = 'L'

    if contractABI == 'UNI':
        if runenv == 'W':
            abiFileName = cwd + "\\lynx\\wallet\\abi\\uni-abi.json"
        else:
            abiFileName = cwd + "/lynx/wallet/abi/uni-abi.json"
    elif contractABI == 'AAVE':  # https://github.com/aave/aave-protocol/tree/master/abi
        if runenv == 'W':
            abiFileName = cwd + "\\lynx\\wallet\\abi\\aave-abi.json"
        else:
            abiFileName = cwd + "/lynx/wallet/abi/aave-abi.json"
    elif contractABI == 'ERC20':  # any erc20 token
        if runenv == 'W':
            abiFileName = cwd + "\\lynx\\wallet\\abi\\erc20-abi.json"
        else:
            abiFileName = cwd + "/lynx/wallet/abi/erc20-abi.json"
    elif contractABI == 'COMP':
        if runenv == 'W':
            abiFileName = cwd + "\\lynx\\wallet\\abi\\comp-abi.json"
        else:
            abiFileName = cwd + "/lynx/wallet/abi/comp-abi.json"
    elif contractABI == 'ATOKEN':
        if runenv == 'W':
            abiFileName = cwd + "\\lynx\\wallet\\abi\\atoken-abi.json"
        else:
            abiFileName = cwd + "/lynx/wallet/abi/atoken-abi.json"
    else:
        abiFileName = 'missing...'

    with open(abiFileName) as f:
        abi_json = json.load(f)

    return abi_json


def getContract(w3, abi, contract_address):
    contract = w3.eth.contract(
        abi=abi, address=Web3.toChecksumAddress(contract_address))
    return contract


def convertAmountToWei(tokenSymbol, amt):
    if tokenSymbol == 'cUSDT':  # // cToken always 8 decimals
        symbolDecimals = 8
    elif tokenSymbol == 'cUSDC':
        symbolDecimals = 8
    elif tokenSymbol == 'cDAI' or tokenSymbol == 'cBAT':
        symbolDecimals = 8
    elif tokenSymbol == 'USDC':
        symbolDecimals = 6
    elif tokenSymbol == 'USDT':
        symbolDecimals = 6
    elif tokenSymbol == 'DAI' or tokenSymbol == 'BAT':
        symbolDecimals = 18
    else:
        symbolDecimals = 18

    return Decimal(amt) * (10 ** Decimal(symbolDecimals))


def convertAmountFromWei(tokenSymbol, amt):
    if tokenSymbol == 'cUSDT':
        symbolDecimals = 8
    elif tokenSymbol == 'cUSDC':
        symbolDecimals = 8
    elif tokenSymbol == 'cDAI' or tokenSymbol == 'cBAT':
        symbolDecimals = 8
    elif tokenSymbol == 'USDC':
        symbolDecimals = 6
    elif tokenSymbol == 'USDT':
        symbolDecimals = 6
    elif tokenSymbol == 'DAI' or tokenSymbol == 'BAT':
        symbolDecimals = 18
    else:
        symbolDecimals = 18

    return amt / 10 ** symbolDecimals


def getChainId():
    # 1 for mainnet, 3 for ropsten
    if app.config['NET'] == 'mainnet':
        return 1
    elif app.config['NET'] == 'kovan':
        return 42
    else:
        return 3  # ropsten
