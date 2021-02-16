from flask import current_app as app
from web3 import Web3
from lynx.wallet.helper import getChainId, convertAmountToWei, getContractAddress, getW3, getContractAbiJson, getContract
from lynx.wallet.wallet import approve, isApproved
import datetime, time

def tradeToken(token_symbol, token_amount, userWall):

    userToken = app.config['SYMB'] # token user owns
    uni_contract_address = getContractAddress('UNI')
    amount = convertAmountToWei(userToken, token_amount) # convert in underlying token balance

    if not isApproved(userWall.address, userToken, uni_contract_address, amount ):
        approve(userWall.address, userToken, uni_contract_address, amount, userWall.privateKey)

    w3 = getW3()
    abi_json = getContractAbiJson('UNI')
    abi = abi_json['abi']
    uniswap_contract = getContract(w3, abi, uni_contract_address)
    nonce = w3.eth.getTransactionCount(userWall.address)

# function swapExactTokensForTokens
    # uint amountIn,
    # uint amountOutMin,
    # address[] calldata path,
    # address to,
    # uint deadline
    # ) external returns (uint[] memory amounts);
    
    amountOutMin = int(amount) * 0.0098 # __convertAmountToWei('DAI', amt/2)
    addressPaths = [Web3.toChecksumAddress(getContractAddress(userToken)), Web3.toChecksumAddress(getContractAddress(token_symbol))]

    # current_time = datetime.datetime.now(datetime.timezone.utc)
    # unix_timestamp = current_time.timestamp() # works if Python >= 3.3
    # deadline = int(unix_timestamp + (20 * 60)) # 20 minutes
    deadline = int(time.time()) + 10000

    trade_tx = uniswap_contract.functions.swapExactTokensForTokens(int(amount),
                            int(amountOutMin),
                            addressPaths,
                            userWall.address, 
                            deadline).buildTransaction({
        'chainId': getChainId(),
        'gas': 5000000,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': nonce
    })
    signed_txn = w3.eth.account.sign_transaction(trade_tx, userWall.privateKey)
    try:
        tx = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        #return tx.hex()
        try:
            txn_receipt = w3.eth.waitForTransactionReceipt(tx, timeout=300)
        except Exception:
            return {'status': 'failed', 'error': 'timeout'}
        else:
            return {'status': 'success', 'receipt': txn_receipt}

    except ValueError as err:
        #return (json.loads(str(err).replace("'", '"')), 402, {'Content-Type': 'application/json'})
        return 'Error: ' + str(err)