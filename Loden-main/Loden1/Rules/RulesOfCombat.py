import sys
import time
sys.path.append('..')
from Commander.GUIGridCommander import Commander

class CombatRules():

    def __init__(self,phase=1,placedShips=0,shipsHit=0):
            self.phase=phase
            self.placedShips=placedShips
            self.shipsHit=shipsHit
            self.endTurn = False
            self.response = "None available"
            
    def getResponse(self):
        return self.response
    
    def findOpponent(self,client):
        try:
            client.openConnection()
            return True
        except:
            return False
    def ifHit(self,attackResult):
        if attackResult == 'ship hit!':
            self.shipsHit+=1
            return True
        return False
    def victoryCondition(self):
        if self.shipsHit == self.placedShips:
            return True
        return False
    '''the placement phase is phase 1 of the game.'''
    def populateBoard(self,shipsCell,commander):
        phase=0
        if self.placedShips<5:
            commander.placeShip(shipsCell)
            self.placedShips+=1
            #return phase 1
            phase=1
        if self.placedShips==5:
            #return phase 2
            phase=2
        return phase

    
    '''the action phase is phase 2 of the game.'''
    def __actionPhase(self,commander,shipsCell,opponentCell):
        #if you are in phase 2 of the game
        attackResult = ''
        '''false, its his turn hasnt ended'''
        if commander.commanderTurn == False:
            #when you attack return the result 
            attackResult=commander.Attack(opponentCell)
            self.ifHit(attackResult)
            return attackResult
        else:
            attackResult=commander.Attack(shipsCell)
            #for some reason it is not correctly incrementing unless I have this here
            self.ifHit(attackResult)
            print('Your Turn has started')                     
            return attackResult            

            
    # this logic is being used in "_init_win" method of the "BattleField.py" logic. referenced to each button on the board
    def actionRules(self,activeCommander,opponentCell,playerCell,boardType):
        response=''
        #While you are still in phase one you are allowed to place 5 ships
        if boardType=='battlefield':
            if self.phase==1:
                self.phase=self.populateBoard(playerCell,activeCommander)
                response='ship placed'
                if self.phase==2:
                    response='all ships placed'
        elif boardType=='attack grid':
            if self.phase==2:
                response = self.__actionPhase(activeCommander,playerCell,opponentCell)
                if self.victoryCondition() == True:
                    print('congratulations you won!!')
                    response='congratulations you won!!'
        return response
