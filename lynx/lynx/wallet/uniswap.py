from lynx.wallet.models import UniswapData
from web3 import Web3
from lynx.wallet.helper import *
import datetime

def tradeToken(token_symbol, token_amount, userWall):
    w3 =getW3()
    contract_address = getContractAddress('UNI')
    abi_json = getContractAbiJson('UNI')
    abi = abi_json['UNI']
    uniswap_contract = getContract(w3, abi, contract_address)
    nonce = w3.eth.getTransactionCount(userWall.address)

    udata = UniswapData
    udata.amountOut = token_amount

    amount = convertAmountToWei(token_symbol, token_amount) # convert in underlying token balance (USDT and not cUSDT)
    swap = uniswap_contract.functions.swapTokensForExactTokens()
    signed_txn = w3.eth.account.sign_transaction(swap, userWall.PrivateKey)
    try:
        tx = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return tx.hex()
    except ValueError as err:
        #return (json.loads(str(err).replace("'", '"')), 402, {'Content-Type': 'application/json'})
        return 'Error: ' + str(err)
    return 0
