import json
from web3 import Web3
from decimal import Decimal
import os
import datetime
from flask import current_app as app
import math

# Using Infura to connect to eth network
def getW3():
    network = app.config['NET']
    if network == 'mainnet':
        w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/6e6af88eebca48fa8bb3ed125e554281'))
    elif network == 'kovan':
        w3 = Web3(Web3.HTTPProvider('https://kovan.infura.io/v3/6e6af88eebca48fa8bb3ed125e554281'))
    else: # ropsten
        w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/6e6af88eebca48fa8bb3ed125e554281'))   
    return w3

def getContractAddress(symbol):

    #tokens = requests.get("https://api.compound.finance/api/v2/ctoken?network=ropsten")
    #contract_address = [t['token_address'] for t in tokens.json()['cToken'] if t['underlying_symbol'] == symbol][0]

    network = app.config['NET']
    address = {
        "mainnet": { 
            "cUSDC": "0x39AA39c021dfbaE8faC545936693aC917d5E7563",
            "cUSDT": "0xf650C3d88D12dB855b8bf7D11Be6C55A4e07dCC9",
            "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "cDAI": "0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643",
            "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "cBAT": "0x6C8c6b02E7b2BE14d4fA6022Dfd6d75921D90E4E",
            "BAT": "0x0D8775F648430679A709E98d2b0Cb6250d2887EF",
            "cETH": "0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5",
            "UNI": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
            },
        "ropsten": {
            "cUSDC": "0x8aF93cae804cC220D1A608d4FA54D1b6ca5EB361",
            "cUSDT": "0x135669c2dcBd63F639582b313883F101a4497F76",
            "USDC": "0x0D9C8723B343A8368BebE0B5E89273fF8D712e3C",
            "USDT": "0x516de3a7A567d81737e3a46ec4FF9cFD1fcb0136",
            "cDAI": "0xdb5Ed4605C11822811a39F94314fDb8F0fb59A2C",
            "DAI": "0xc2118d4d90b274016cB7a54c03EF52E6c537D957",
            "cBAT": "0x9E95c0b2412cE50C37a121622308e7a6177F819D",
            "BAT": "0x443Fd8D5766169416aE42B8E050fE9422f628419",
            "cETH": "0xBe839b6D93E3eA47eFFcCA1F27841C917a8794f3",
            "UNI": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
        }
    }

    #     raise Exception("Invalid symbol")

    return address[network][symbol]

def getContractAbiJson(symbol):

    # abi_url = "https://raw.githubusercontent.com/compound-finance/compound-protocol/master/networks/mainnet-abi.json"
    # abi_url = "https://raw.githubusercontent.com/compound-finance/compound-protocol/master/networks/ropsten-abi.json"
    # abi = requests.get(abi_url)

    cwd = os.getcwd()
    abiFileName = ''
    runenv = app.config['RUNENV'] # W-Windows or L-Linux

    if symbol != 'ERC20':   # symbol == 'cUSDT' or symbol == 'cUSDC' or symbol == 'cDAI': ...
        if runenv == 'W':
            abiFileName = cwd + "\\lynx\\wallet\\abi\\comp-abi.json"
        else:
            abiFileName = cwd + "/lynx/wallet/abi/comp-abi.json"
    elif symbol == 'ERC20': # any erc20 token
        if runenv == 'W':
            abiFileName = cwd + "\\lynx\\wallet\\abi\\erc20-abi.json"
        else:
            abiFileName = cwd + "/lynx/wallet/abi/erc20-abi.json"    
    elif symbol == 'UNI':
        if runenv == 'W':
            abiFileName = cwd + "\\lynx\\wallet\\abi\\IUniswapV2Router02.json"
        else:
            abiFileName = cwd + "/lynx/wallet/abi/IUniswapV2Router02.json"  
    else:
        abiFileName = 'missing...'
 
    with open(abiFileName) as f:
        abi_json = json.load(f)

    return abi_json

def getContract(w3, abi, contract_address):
    contract = w3.eth.contract(abi=abi, address=Web3.toChecksumAddress(contract_address))
    return contract

def convertAmountToWei(tokenSymbol, amt):
    if tokenSymbol == 'cUSDT': # // cToken always 8 decimals
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
        return 3 #ropsten
