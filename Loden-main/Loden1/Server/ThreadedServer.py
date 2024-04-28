import threading
import traceback
import time
from Server.Server import Server
import re
import sys
sys.path.append('..')
from Abstractions.Client_Server.ABCServer import ABCServer
from Client.DataIntermediary import Data
from Rules.RulesOfCombat import CombatRules
#from ServerOperations import Operations

class ServerThreader(threading.thread):
    def __init__(self):
        super().__init__()
        self.threads = {}

    
    def pauseSession(self,session):
        while self.pause:
            time.wait(1)
    
    def startThreads(self):
        try:
            #at somepoint ill have to seperate the thread from the server
            #socketServer=self.startServer()
            playerNumb = 0
            maxPlayerThreads=2
            
            while playerNumb<maxPlayerThreads:
                playerNumb=threading.active_count()
                player = f'player_{playerNumb}'
                playerTurn=player+'_turn'
                #returns the socket connection and the client`s address
                #connect, address = socketServer.accept()
                #daemon threads are able to be stopped even if they have not finished their tasks
                #thread = threading.Thread(target=self.threadProcessing,daemon=True, args=(connect,playerTurn))
                #had a feeling this was the case but I just confirmed it. args is equal to *args which requires a list or a tuple
                thread = threading.Thread(target=self.threadProcessing,daemon=True, args=(playerTurn,))
                thread.name = player
                self.threads[player]= thread
                thread.start()
                if len(self.threads) == 2:
                    print("[Thread Count]", {threading.active_count() - 1})
                
        except Exception as e:
            print(e)
            traceback.print_exc()

            
    def waitTurn(self,command):
        #self.convertList(command)
        print("command:",command)
        for player in command.keys():
            print("queue item:",player)
            
            match str(player).lower():
                case('player_1_turn'):
                    #sets the internal flag to true
                    self.pause.set()
                    #time.sleep(1)
                    playerSession = self.threads['player_1']
                    #returns true if internal flag is set to true
                    self.pause.is_set()
                    #self.pauseSession(playerSession)
                    print('thread:',self.threads)
                case("player_2_turn"):
                    #time.sleep(1)
                    pass
            
            if command[player]=='end turn':
                #swap turn phase so that the opposite player can act
                pass
                #break

    def serverThread(self,player):
        #something to consider is that the client I created always closes the connection after every sent message. 
        # what may be needed is to simply end the connection but somehow assign player
        #->1 to the thread... either that or have each connection identify itself and name the thread based on its identity then close the connection
        try:
            response = ''
            serverConnection = True
            print('thread:',player)
            dataObj=Data()
            socketServer=self.startServer()
            connection, address = socketServer.accept()
            while serverConnection:
                #startServer = self.startServer(connection)
                message = 'testing'
                response = self.listenToSocket(connection)
                #response = Server.convertList(response)
                #key, value = Server.searchDictionary(response,'game over','game over')
                print('client message:',response,player)
                dataObj.data=response
                #value = response['end']
                #print("dict:",type(key), type(value))
                #queue the command sent by your client
                self.queue.put({player:dataObj},timeout=5)
                #self.pause.is_set()
                #print("queue:",self.queue.get())
                queueItem = self.queue.get()
                print("response:",response)
                if queueItem != None or queueItem=='end turn':
                    print("Queue:", queueItem)
                    self.waitTurn(queueItem) 
                # from here down is surpufluice code... fix it
                if queueItem == "close client connection" or queueItem == "game over":
                    serverConnection = False 
                self.sendMessage(connection,message)
                
                '''if message == 'game over!':
                    server.closeConnection(connection)
                    break  
                elif message=='close test':
                    server.closeConnection(connection)
                    break  '''
            socketServer.closeConnection(connection)
        except Exception as e:
            print(e)
            traceback.print_exc()
       
    #main logic
    def threadProcessing(self,player):
        result = Server().serverThread(player)
        rules = CombatRules()
                
