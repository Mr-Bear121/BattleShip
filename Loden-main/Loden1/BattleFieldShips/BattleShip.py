#!/Loden-main/Loden1

class BattleShip:
    
    def __init__(self, size=1,shipType="Corvette"):
        self.size = size
        self.shipType = shipType
        self.shipChar='\U0001F6A2'

    #could have a built in property to which cell they are and maybe even which player owns them
    def shipHit(self,shipsCell):
        shipColor = '#ff0000'
        #logic ment for the attack grid: if shipcell doesn not contain a boat then place one in it
        if shipsCell!='\U0001F6A2':
            shipsCell['text'] = self.shipChar
        shipsCell.config(fg= shipColor)
        #return shipColor
        return shipsCell
        
        
    def shipMissed(self,shipsCell):
        shipCharacter = 'X'
        shipsCell['text'] = shipCharacter
        shipsCell.config(bg='#808080')
        return shipsCell
