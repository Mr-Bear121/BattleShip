import tkinter as tk
import time
import socket
import subprocess
import BattleField
from Commander.GUIGridCommander import Commander
from Client.DataIntermediary import Data
from Client.Client import Client
from Server.Server import Server
import sys
import os
#from Server.ThreadedServer import ServerThreader
from Rules.GridActions import *
from Rules.RulesOfCombat import CombatRules

activeSessions = None
update = Data()
windows=[]
client=Client().createClient()

#this is convoluted and i`m vaguely sure why it works. im using this in tandem with a callback function in my battlefield.py file in order to-- 
#->transfer my data through this program and back into the global variables. I have to do this because for some reason when I populate my global variables with--
#->the values I want to do transformation on. they always get rest to their default values. somehow this mess with function properly transmits 
# the data I need back to the variables.
def returnWindowData(data):
    global update
    update=data
    
def createStartUpScreen():
    global zhost
    global update
    x=0
    y=20
    host = tk.Tk()
    host.title("BattleShip")
    host.geometry("300x300")
    hotSeatButton=tk.Button(host,text="2 player hotseat", height=2,width=20,command=lambda :startGame('hotseat',2,host))
    x=host.winfo_reqheight()/2.65
    hotSeatButton.place(x=x,y=y)
    LANButton=tk.Button(host,text="LAN Session", height=2,width=20,command=lambda :startGame('LAN',2,host))
    LANButton.place(x=x,y=(y*2.5))
    hotSeatButton.pack()
    LANButton.pack
    return host

def switchPlayerWindows(player,opponent,activeSessions):
    activeSessions[f'{player}'][f'{player} battlefield'].windowAction('hide')
    activeSessions[f'{player}'][f'{player} attack grid'].windowAction('hide')
    activeSessions[f'{opponent}'][f'{opponent} battlefield'].windowAction('show')
    activeSessions[f'{opponent}'][f'{opponent} attack grid'].windowAction('show')

def playerWindow(gameType,playerName,host,rules,gridType):
    global windows
    params = BattleField.GridParams(7,7,rules=rules,player=playerName,gameType=gameType,hostWindow=host,gridType=gridType)
    params.font_wide = 3
    params.font_high = 1
    params.font_size = 28
    w = BattleField.GridT()
    w = w.Create(params)
    return w

def AttackGrid(gameType,playerName,host,rules,gridType):
    global windows
    params = BattleField.GridParams(7,7,rules=rules,player=playerName,gameType=gameType,hostWindow=host,gridType=gridType)
    params.font_wide = 3
    params.font_high = 1
    params.font_size = 28
    w = BattleField.GridT()
    w = w.Create(params)
    return w
        
def createCaptain(name):
    try:
        if int(name):
            return Commander(commanderName="player_{}".format(name))
        return "no named commander"
    except ValueError as cError:
        return Commander(commanderName=name)
    
def createPlayerSessions(numbSessions):
    playersCreated = 0
    players = {}
    while playersCreated < numbSessions:
        playersCreated+=1
        captain=createCaptain(playersCreated)
        players[captain]=[playerWindow,AttackGrid]
    return players


def startSessions(gameType,sessions,host):
    global update
    global activeSessions
    count = 0    
    activeSessions={}
    commanders=list(sessions.keys())
    for playerwindow in sessions.values():
        rules = CombatRules()
        playerSession={f'{commanders[count].commanderName} battlefield':playerwindow[0](gameType,commanders[count],host,rules=rules,gridType='Battlefield'),
        f'{commanders[count].commanderName} attack grid':playerwindow[1](gameType,commanders[count],host,rules=rules,gridType='Attack Grid')}
        activeSessions[commanders[count].commanderName]=playerSession
        if commanders[count].commanderName == 'player_2':
            playerSession['player_2 battlefield'].windowAction('hide')
            playerSession['player_2 attack grid'].windowAction('hide')
        count+=1
    playergame=playerSession['player_2 battlefield']
    update.activeSessions=activeSessions
    update.activeCommanders=commanders
    playergame.returnData(update)
    return playerSession

def startGame(gameType,numbSessions,host):
    global activeSessions
    sessions=None
    if gameType=='hotseat':
        playerSessions = createPlayerSessions(numbSessions)
        #was originally a string but then I decided to just pass the function to remove complications later on
        sessions = startSessions(hotSeatGame,playerSessions,host)
    elif gameType=='LAN':
        commander1=createCaptain(1)
        playerSessions = createPlayerSessions(numbSessions)
        #was originally a string but then I decided to just pass the function to remove complications later on
        sessions = startSessions(lanGame,playerSessions,host)
        #lanGame(player=commander1,boardType='battlefield',value='1',rules=CombatRules)
        #sessions = startSessions(lanGame,playerSessions,host)
    return sessions


def testConnection(client):
    response=''
    dataObj=Data()
    dataObj.data='testing connection'
        #it should work, im just using this in an unfamiliar way so i`ll have to test it.
    try:
        #client=client.Client()
        client.openConnection()
        client.sendMessage(dataObj)
        response= client.receiveMessage()
        #dataObj.data='close client connection'
        #client.sendMessage(dataObj)
        client.isClientConnected=True
        return client,response
    except Exception as e:
        print('client connection error:')
        #print(e)
        #could rename the server as, 'communications tower' and pass the commanders to them. it all comes down to client-side or server-side processing
        #server = Server()
        #server.startThreads()  
        #client.closeConnection()
        response='not connected'
        return client,response

#def lanGame(player,boardType,value,rules):
def lanGame(player,boardType,value,rules):
    global update
    global client
    global activeSessions
    if activeSessions==None:
        activeSessions=update.activeSessions
    playerSession=activeSessions[player.commanderName]
    playerBoard=playerSession[f'{player.commanderName} {boardType.lower()}']
    #client=Client(address='127.0.0.1',port=2004)
    #dataObj=Data()
    
    clientResponse=Data()
    playerCell=None
    while client.isClientConnected==False:
        if clientResponse==None or clientResponse.data==None:
            client,clientResponse=testConnection(client)
            print('clientTest response:',clientResponse)
        if clientResponse=='not connected':
            process=subprocess.Popen(f'python Server/Server.py')
            #to do this properly i`ll have to use the library subprocess
            #sys.executable helps find the python executable system path
            '''backGroundServer=subprocess.run([sys.executable, "-c",
            'from Server.Server import Server;server = Server();server.startThreads()'])'''
            clientResponse=None   
            #need to wait one second so that the server can get ready to listen to an input     
            time.sleep(1)  
        else: 
            clientResponse=Data(data='server ready')
            #client.isClientConnected=True

    '''if clientResponse.data=='server ready':
        update.data='requesting player number'
        #client.openConnection()
        client.sendMessage(update)
        clientResponse= client.receiveMessage()
        update=update.convertToDataObj(clientResponse)'''

#if this is player_1`s attack board then get the cell of your opponents battlefield. if this is player 2 then visa versa
    if boardType=='attack grid':
            #playerBoard=update.activeSessions[player.commanderName]
            #playerCell=playerBoard[f'{player.commanderName} attack grid'].getCell(value)
        update.data={'player cell value',value}
        client.sendMessage(update)
        #should receive a corresponding cell from opponents battlefield
        clientResponse= client.receiveMessage()
        print('client test response:',clientResponse)
        update=update.convertToDataObj(clientResponse)
    elif boardType=='Battlefield':
        commanderResult=LanGridActions.gridActions(player,boardType,value,playerBoard,rules,clientResponse)

    #update.data={'player cell value':value}
    client.sendMessage(update)
    #should receive a corresponding cell from opponents battlefield
    clientResponse= client.receiveMessage()
    update=update.convertToDataObj(clientResponse)

    #if clientResponse.data.keys()[0]=='player cell value':
    if update.data=='player cell value':
        #need logic to process the cell request.update.data should contain the cell information
        battleFieldCell=LanGridActions.returnBattleCell(update.activeSessions,update.activeCommanders,clientResponse.data['cell value'])
        client.sendMessage({'return cell value':battleFieldCell})
        #should be a button at this point
        clientResponse=client.receiveMessage()
        update=update.convertToDataObj(clientResponse)

    if update.data=='return cell value':
    #client.sendMessage(player)
        commanderResult=LanGridActions.gridActions(player,boardType,value,update,rules,clientResponse)
    #client.closeConnection()
    '''
    gameCommands ="command:end_turn:cell:\{Cell\},end:game over"
    client = Client.Client()
    client2 = Client.Client()
    resp1 = client.connectClient(message=gameCommands)
    resp2 = client2.connectClient(message=gameCommands)
    while True:
        if resp1 != None or resp2 != None:
            client.connectClient(message=gameCommands)
            client2.connectClient(message=gameCommands)'''

def hotSeatGame(player,boardType,value,rules):
    global update
    GridActions.gridActions(player,boardType,value,update,rules)
    #gridActions(player,boardType,value,rules)
  
if __name__ == '__main__':
    numbSessions = 2
    host = createStartUpScreen()
    #print(rules.getResponse())
    host.mainloop()
    #startGame(numbSessions)
    #host.mainloop()
    #client = Client()
    #client.openConnection()
    #player1 = playerWindow()

    
