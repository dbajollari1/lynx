from abc import ABC, abstractmethod

class Savings(ABC):
    
    def __init__(self, userWallet, tokenSymbol):
        self.userWallet = userWallet
        self.tokenSymbol = tokenSymbol

    @abstractmethod 
    def doDeposit(self):
        pass

    @abstractmethod
    def getDepositData(self):
        pass

    @abstractmethod
    def doWithdraw(self):
        pass    

    @abstractmethod
    def getUserTransactions(self):
        pass

    @abstractmethod
    def getTokenAPY(self):
        pass

# class SavingsFactory:

#     def __init__(self):
#         self._savingPlatforms = {}

#     def register_saving_platform(self, platformName, savingObject):
#         self._savingPlatforms[platformName] = savingObject

#     def get_saving_platform(self, platformName):
#         savingObject = self._savingPlatforms.get(platformName)
#         if not savingObject:
#             raise ValueError(platformName)
#         return savingObject()

# factory = SavingsFactory()
# factory.register_saving_platform('AAVE', SavingsAave)
# factory.register_saving_platform('COMP', SavingsCompound)
