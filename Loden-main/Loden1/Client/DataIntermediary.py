
class Data():
    def __init__(self,data=None,playerName=None,activeSessions={},activeCommanders=[],boardType=''):
        self.data=data
        self.playerName=playerName
        self.activeSessions=activeSessions
        self.boardType=boardType
        self.activeCommanders=activeCommanders

    #needed because ive been using the json library to convert this object into a json dict. however, I need to regenerate an object from the dict to do transformations
    def convertToDataObj(self,data):
        return Data(data['data'],data['playerName'],data['activeSessions'],data['boardType'],data['activeCommanders'])
