from abc import ABC, abstractmethod
import socket

class ABCClient(ABC):
    
    def __init__(self,address,port,connection):
        self.address = address
        self.port = port
        self.connection = connection

    @abstractmethod
    def openConnection(self):
        pass

    @abstractmethod
    def closeConnection(self,connection):
        pass

    @abstractmethod
    def sendMessage(self,message, client):
        pass

    @abstractmethod
    def receiveMessage(self,connection):
        pass
    
    
