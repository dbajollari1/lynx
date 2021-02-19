from lynx.wallet.helper import getContractAddress, getContract, getContractAbiJson, getChainId, convertAmountToWei
from web3 import Web3
from lynx.wallet.wallet import approve
class Aave:

    def __init__(self, web3, symbol):
        self.web3 = web3
        self.symbol = symbol
        self.lending_pool_addr_provider = getContract(
            self.web3, 
            getContractAbiJson("AAVE")["lending_pool_address_provider"],
            getContractAddress("LPAP")
        )
        self.lending_pool = getContract(
            self.web3,
            getContractAbiJson("AAVE")["lending_pool"],
            self.lending_pool_addr_provider.functions.getLendingPool().call()
        )
        self.erc20Token = getContract(
            self.web3,
            getContractAbiJson("ERC20"),
            getContractAddress(symbol)
        )

    def get_account_data(self, wall_address):
        return self.lending_pool\
            .functions\
            .getUserAccountData(wall_address)\
            .call()

    def approve(self, user_address, amount_to_appove, private_key):
        nonce = self.web3.eth.getTransactionCount(user_address)
        transaction_to_approve = self.erc20Token\
            .functions\
            .approve(
                self.lending_pool_addr_provider\
                    .functions\
                    .getLendingPool()\
                    .call(),
                int(convertAmountToWei(self.symbol, amount_to_appove))
            )\
            .buildTransaction({
                'chainId': getChainId(), 
                'gas': 500000,
                'gasPrice': self.web3.toWei('20', 'gwei'),
                'nonce': nonce
            })
        singed_transaction = self.web3\
            .eth\
            .account\
            .signTransaction(transaction_to_approve, private_key)
        self.web3\
            .eth\
            .sendRawTransaction(singed_transaction.rawTransaction)

    def allowance(self, wall, amount):
        allowed = self.erc20Token\
            .functions\
            .allowance(
                wall.address, 
                self.lending_pool_addr_provider\
                    .functions\
                    .getLendingPool()\
                    .call()
            )\
            .call()
        return True if allowed >= amount else False

    def deposit(self, wall, amount, referal_code=0):
        if not self.allowance(wall, amount):
            self.approve(wall.address, amount, wall.privateKey)
        nonce = self.web3.eth.getTransactionCount(wall.address)
        transaction_to_approve = self.lending_pool\
            .functions\
            .deposit(
                Web3.toChecksumAddress(getContractAddress(self.symbol)),
                int(convertAmountToWei(self.symbol, amount)), 
                wall.address, 
                int(referal_code)
            )\
            .buildTransaction({
                'chainId': getChainId(), 
                'gas': 500000,
                'gasPrice': self.web3.toWei('20', 'gwei'),
                'nonce': nonce
            })
        
        singed_transaction = self.web3\
            .eth\
            .account\
            .signTransaction(transaction_to_approve, wall.privateKey)
        self.web3\
            .eth\
            .sendRawTransaction(singed_transaction.rawTransaction)


    def withdraw(self, wall, amount):
        if not self.allowance(wall, amount):
            self.approve(wall.address, amount, wall.privateKey)
        nonce = self.web3.eth.getTransactionCount(wall.address)
        transaction_to_approve = self.lending_pool\
            .functions\
            .withdraw(
                Web3.toChecksumAddress(getContractAddress(self.symbol)),
                int(convertAmountToWei(self.symbol, amount)),
                wall.address
            )\
            .buildTransaction({
                'chainId': getChainId(), 
                'gas': 500000,
                'gasPrice': self.web3.toWei('20', 'gwei'),
                'nonce': nonce
            })     
        singed_transaction = self.web3\
            .eth\
            .account\
            .signTransaction(transaction_to_approve, wall.privateKey)
        self.web3\
            .eth\
            .sendRawTransaction(singed_transaction.rawTransaction)