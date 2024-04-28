import tkinter as tk
from BattleFieldShips.BattleShip import BattleShip

#this is convoluted and i`m vaguely sure why it works. im using this in tandem with a callback function in my battlefield.py file in order to-- 
#->transfer my data through this program and back into the global variables. I have to do this because for some reason when I populate my global variables with--
#->the values I want to do transformation on. they always get rest to their default values. somehow this mess with function properly transmits 
# the data I need back to the variables.
class GridActions():
    def __init__(self):
        self.update=None

    def returnWindowData(self,data):
        self.update=data

    def endWindow(self,rootWindow):
        rootWindow.close()

    def victoryWindow(self,Commander):
        #rootWindow=rootWindow.zpane
        popUp=tk.Tk()
        popUp.geometry('750x250')
        popUp.title('Victory Window')
        label=tk.Label(popUp,text=f'{Commander.commanderName} {Commander.returnIntel()}')
        closeButton=tk.Button(popUp,text='Exit Game',command=popUp.destroy,relief='raised')
        label.pack()
        closeButton.pack()
        #popUp.mainloop
        
    def switchPlayerWindows(self,player,opponent,activeSessions):
        activeSessions[f'{player}'][f'{player} battlefield'].windowAction('hide')
        activeSessions[f'{player}'][f'{player} attack grid'].windowAction('hide')
        activeSessions[f'{opponent}'][f'{opponent} battlefield'].windowAction('show')
        activeSessions[f'{opponent}'][f'{opponent} attack grid'].windowAction('show')

    '''once you get the 'intel' from your players action then evaluate it and update the board'''
    def evaluateIntel(self,player,playerCell,opponentCell):
        intel = player.returnIntel()
        match intel:
            case 'ship placed':
                player.gatherIntel('ship placed')
            case 'congratulations you won!!':
                player.gatherIntel('Winner')
            case 'all ships placed':
                player.gatherIntel('all ships placed')
            case 'ship missed!':
                player.assessDamage(intel,opponentCell)
                player.assessDamage(intel,playerCell)
            case 'ship hit!':
                player.assessDamage(intel,opponentCell)
                player.assessDamage(intel,playerCell)
            case '':
                player.gatherIntel('rules rejected')
            case other:
                #if you didnt hit him and you didnt miss him... he must have been both hit and missed.. it`s Schrödinger`s boat!
                player.gatherIntel('Schrödinger')
        return player

    #action logic:
    def playerAction(self,player,opponent,playerBoards,rules,cellValue,boardType):
        battleShip = BattleShip()
        playerboard=playerBoards[player.commanderName]
        opponentBoard=playerBoards[opponent.commanderName]
        playerCell=''
        opponentCell=''
        if boardType=='battlefield':
            playerCell=playerboard[f'{player.commanderName} {boardType}'].getCell(cellValue)
            opponentCell=None
            if playerCell['text']==battleShip.shipChar:
                player.gatherIntel('Cell is Occupied')
                return player
        elif boardType=='attack grid':
            playerCell=playerboard[f'{player.commanderName} {boardType}'].getCell(cellValue)
            opponentCell=opponentBoard[f'{opponent.commanderName} battlefield'].getCell(cellValue)
            if playerCell['text']=='X':
                player.gatherIntel('Cell is Occupied')
                return player
        player.gatherIntel(rules.actionRules(player,opponentCell,playerCell,boardType))
        player=self.evaluateIntel(player,playerCell,opponentCell)
        return player
        
    #wait for both players to place their ships before attacking
    def waitBothPlaceShips(self,player,opponent,playerSession,activeSessions):
        if playerSession.returnIntel()=='all ships placed':
            self.switchPlayerWindows(player,opponent,activeSessions)

    def playerActionLogic(self,commander,opponent,activeSessions,boardType,rules,value):
        #if it`s false, 'his turn hasnt ended' and you pressed the battlefield window
        if commander.commanderTurn==False and boardType.lower()=='battlefield':
            actionResult = self.playerAction(commander,opponent,activeSessions,rules,value,boardType.lower())
            if actionResult.returnIntel() == 'Cell is Occupied':
                return commander,opponent
            self.waitBothPlaceShips(commander.commanderName,opponent.commanderName,commander,activeSessions)
        if (commander.commanderTurn==False and boardType.lower()=='attack grid'):
            actionResult = self.playerAction(commander,opponent,activeSessions,rules,value,boardType.lower())
            if actionResult.returnIntel() == 'Cell is Occupied':
                return commander,opponent
            #if you performed an operation that was rejection by the rules of the game then dont do anything and try again
            if actionResult.returnIntel()!='rules rejected':
                #end turn by hiding the window and showing player 2`s window
                self.switchPlayerWindows(commander.commanderName,opponent.commanderName,activeSessions)
                #its true that his turn has ended
                commander.commanderTurn=True
                #it is false that player_2`s turn has ended
                opponent.commanderTurn=False
        return commander,opponent

    def endGame(self,activeSessions):
        self.endWindow(activeSessions['player_1']['player_1 battlefield'])
        self.endWindow(activeSessions['player_1']['player_1 attack grid'])
        self.endWindow(activeSessions['player_2']['player_2 battlefield'])
        self.endWindow(activeSessions['player_2']['player_2 attack grid'])

    #main grid logic:
    # update passes data that can be used as an, 'intermediaryData' object. I am using it to have a reference to my active sessions and current commanders 
    @staticmethod
    def gridActions(player,boardType,value,update,rules):
        #if I wanted to pause the game so that people can see the board before its the other players turn I can use a popup window instead of 'time'.
        activeSessions=update.activeSessions
        activeCommanders=update.activeCommanders
        actionResult=''
        if player=='player_1':
            activeCommanders[0],activeCommanders[1]=GridActions.playerActionLogic(activeCommanders[0],activeCommanders[1],activeSessions,boardType.lower(),rules,value)    
        elif player=='player_2':
            activeCommanders[1],activeCommanders[0]=GridActions.playerActionLogic(activeCommanders[1],activeCommanders[0],activeSessions,boardType.lower(),rules,value)
        #if a player has won then display the victory window and end the game
        if activeCommanders[0].returnIntel()=='Winner':
                GridActions.victoryWindow(activeCommanders[0])
                GridActions.endGame(activeSessions)
        elif activeCommanders[1].returnIntel()=='Winner':
            GridActions.victoryWindow(activeCommanders[1])
            GridActions.endGame(activeSessions)
        return actionResult



class LanGridActions(GridActions):

    def __init__(self):
        super().__init__()

    @staticmethod
    def returnBattleCell(playerboard,player,cellValue):
        playerboard=playerboard[player.commanderName]
        playerCell=[f'{player.commanderName} battlefield'].getCell(cellValue)
        return playerCell

    def waitBothPlaceShips(self,commander):
        if commander.returnIntel()=='all ships placed':
            #because I only have a reference to 1 player I need to change up the logic to account for that.
            pass
            #self.switchPlayerWindows(player,activeSession)

    def playerActionLogic(self,commander,opponentCell,playerBoard,boardType,rules,value):
        #if it`s false, 'his turn hasnt ended' and you pressed a cell on the battlefield window
        if commander.commanderTurn==False:
            commander = self.playerAction(commander,opponentCell,playerBoard,rules,value,boardType.lower())
            #if the cell is occupied then return the commander unmodified
            if commander.returnIntel() == 'Cell is Occupied':
                return commander
            # need to give this a check for if all ships have not been placed then wait for both to place ships
            if rules.placedShips!=5:
                self.waitBothPlaceShips(commander)
            #if you performed an operation that was rejection by the rules of the game. then dont do anything, 'try again'.
            if commander.returnIntel()!='rules rejected':
            #end turn by hiding the window and showing player 2`s window:EDIT: need to replace with a method to wait for a turn instead of hiding a window
                pass
        #its True that his turn has ended
        '''commander.commanderTurn=True'''
        return commander

    #action logic:
    def playerAction(self,player,opponentCell,playerBoard,rules,playerCellValue,boardType):
        battleShip = BattleShip()
        '''playerboard=playerBoards[player.commanderName]'''
        #opponentBoard=playerBoards[opponentCell.commanderName]
        playerCell=''
        #CAN SIMPLIFY BY SIMPLY GETTING THE CELL THEN CHECKING THE BOARD TYPE:
        if boardType=='battlefield':
            #gets the actual cell button
            '''playerCell=playerBoard[f'{player.commanderName} {boardType}'].getCell(playerCellValue)'''
            playerCell=playerBoard.getCell(playerCellValue)
            #opponentCell=None
            pass
            if playerCell['text']==battleShip.shipChar:
                #player.gatherIntel('Cell is Occupied')
                return player
        elif boardType=='attack grid':
            '''playerCell=playerBoard[f'{player.commanderName} {boardType}'].getCell(playerCellValue)'''
            playerCell=playerBoard.getCell(playerCellValue)
            #opponentCell=opponentBoard[f'{opponentCell.commanderName} battlefield'].getCell(cellValue)
            if playerCell['text']=='X':
                player.gatherIntel('Cell is Occupied')
                return player
        player.gatherIntel(rules.actionRules(player,opponentCell,playerCell,boardType))
        player=self.evaluateIntel(player,playerCell,opponentCell)
        return player


    #main logic
    @staticmethod
    def gridActions(player,boardType,value,playerBoard,rules,opponentCell=None):
        #going to need to 'handshake' to figure out who is which player
        #if I wanted to pause the game so that people can see the board before its the other players turn I can use a popup window instead of 'time'.
        '''activeSessions=update.activeSessions'''
        #activeCommanders=update.activeCommanders
        #actionResult=''
        playerCommander=LanGridActions().playerActionLogic(commander=player,opponentCell=opponentCell,playerBoard=playerBoard,boardType=boardType.lower(),rules=rules,value=value) 
        #if a player has won then display the victory window and end the game
        if playerCommander.returnIntel()=='Winner':
                LanGridActions.victoryWindow(playerCommander)
                #need to re-figure the logic because active sessions is not supposed to be valid... I could probably return a 'winner' value to the main logic thread
                LanGridActions.endGame(playerBoard)
                actionResult='end game'
        return playerCommander
    

    
