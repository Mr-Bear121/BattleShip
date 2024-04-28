from abc import ABC,abstractmethod

class CRUDS(ABC):

    
    @staticmethod
    @abstractmethod
    def create(self,req):
        pass

    @staticmethod
    @abstractmethod
    def read(self,req):
        pass
    
    @staticmethod
    @abstractmethod
    def update(self,req):
        pass

    @staticmethod
    @abstractmethod
    def delete(self,req):
        pass

    @staticmethod
    @abstractmethod
    def search(self,req):
        pass
    
