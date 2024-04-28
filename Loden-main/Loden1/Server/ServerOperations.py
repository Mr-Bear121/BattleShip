import sys
sys.path.append('../')
from Abstractions.Client_Server.ABCCRUDSOperations import CRUDS
class Operations(CRUDS):

    def __init__(self,message):
        self.message = message
    @staticmethod
    def getResponseCode(self,connection):
        pass
    @staticmethod
    def sendMessage(self,message):
        pass
    
    @staticmethod
    def create(self,req):
        pass

    @staticmethod
    def read(self,req):
        pass
    
    @staticmethod
    def update(self,req):
        pass

    @staticmethod
    def delete(self,req):
        pass

    @staticmethod
    def search(self,req):
        pass
    
