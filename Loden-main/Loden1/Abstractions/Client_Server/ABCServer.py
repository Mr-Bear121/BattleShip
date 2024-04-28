from abc import ABC, abstractmethod
import socket

class ABCServer(ABC):

    def __init__(self, address, port):
        self.address = address
        self.port = port

    @abstractmethod
    def startServer():
        pass
    @abstractmethod
    def two_PlayerSession():
        pass
    @abstractmethod
    def getResponseCode(connection):
        pass
