import socket
import json
import threading
import queue
import time
import traceback
import time
import re
import sys
import os
sys.path.append(f'{os.getcwd()}')
from Abstractions.Client_Server.ABCServer import ABCServer
from Client.DataIntermediary import Data
from Rules.RulesOfCombat import CombatRules
#from ServerOperations import Operations

class Server(ABCServer):
    def __init__(self):
        super().__init__(socket.gethostbyname(socket.gethostname()),80)
        #self.queue = queue.Queue()
        self.queue = {}
        self.threads = {}
        self.pause = threading.Event()
        self.dataObj=Data()
        self.isTest=False

    def two_PlayerSession():
        pass

    def testServer(self):
        while True:
            print("server address:",self.address,"port number:",self.port)
            isValid = socket.inet_aton(self.address)
            server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            #server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((self.address, self.port))
            # 5 is = to backlog
            server.listen(4)
            connection, address = server.accept()
            print("listen 1:")
            message = ''
            while True:
                #recv = buffer size in bytes
                #Note: For best match with hardware and network realities->
                #, the value of bufsize should be a relatively small->
                #power of 2, for example, 4096.
                data = connection.recv(4096)
                message= data.decode()
                print(message)
                test = Server.convertList(message)
                print(test)
                print("type 1:",type(test))
                test = Server.searchDictionary(test,'game over','game over')
                print(test)
                connection.send("Testing server.".encode())
                break
            connection.close()

    def startServer(self):
        print("server address:",self.address,"port number:",self.port)
        isValid = socket.inet_aton(self.address)
        serverSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serverSock.bind((self.address, self.port))
        # 5 is = to backlog
        serverSock.listen(5)
        #connection, address = server.accept()
        #print(type(server))
        #print(connection)
        return serverSock
    
    '''def startServer(self,server):
        connection, address = server.accept()
        #print(type(server))
        #print(connection)
        return connection
    '''
    @staticmethod
    def convertList(diction) -> dict:
       try:
           dictionData = {}
           #diction = diction.split(":")
           diction = re.split(r':|,',diction)
           print("convert:",diction)
           for i in range(0,(len(diction)-1)):
               dictionData[diction[i]] = diction[i+1]
           return dictionData
       except Exception as e:
           print(e)
           traceback.print_exc()

    @staticmethod
    def searchList(myList, searchItem):
        for item in myList:
            print(item)
            if item == searchItem:
                return item
        return searchItem + ' not found'
       
    def listenToSocket(self,connection):
        try:
            message = ''
            #recv = buffer size in bytes
            #Note: For best match with hardware and network realities->
            #, the value of bufsize should be a relatively small->
            #power of 2, for example, 4096. '64^2'
            #note, if the client has disconnected then b'' is returned
            data = connection.recv(16777216)
            print('listening data',data)
            message=json.loads(data)
            #message=message.decode('ascii')
            print('socket info:',message)
            print('socket info:',type(message))
            if not data:
                message = 'no data sent'
            elif '':
                return 'return client connection'
            #this is not needed for this project however, if I ever wanted to expand the code it would be nice to have this capability
            elif message['data']=='testing connection':
                message['data']='server created'
                self.sendMessage(connection,message)
            else:
                print(message, end='\n')                    
            return message
        except Exception as e:
            print(e)
            traceback.print_exc()
    
    def sendMessage(self,connection,message):
        #probably just use self.connection.send()
        #connection.send(str(message).encode())
        serialize=json.dumps(message, default=lambda o: o.__dict__)
        connection.send(serialize.encode('ascii'))
        
    def closeConnection(self,connection):
        if connection != None:
            connection.close()
        print('Client disconnected.')
        
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
                socketServer=self.startServer()
                connection, address = socketServer.accept()
                playerNumb=threading.active_count()
                player = f'player_{playerNumb}'
                playerTurn=player+'_turn'
                print('start threads connection:', connection)
                print('number of thread connections:', playerNumb)
                #returns the socket connection and the client`s address
                #connect, address = socketServer.accept()
                #daemon threads are able to be stopped even if they have not finished their tasks
                #thread = threading.Thread(target=self.threadProcessing,daemon=True, args=(connect,playerTurn))
                #had a feeling this was the case but I just confirmed it. args is equal to *args which requires a list or a tuple
                #threadLocked=threading.Lock()
                thread = threading.Thread(target=self.threadProcessing,daemon=True, args=(player,playerTurn,connection))
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

    def serverThread(self,player,player_Turn,connection):
        #something to consider is that the client I created always closes the connection after every sent message. 
        # what may be needed is to simply end the connection but somehow assign player
        #->1 to the thread... either that or have each connection identify itself and name the thread based on its identity then close the connection
        try:
            response = ''
            serverConnection = True
            print('thread:',player)
            dataObj=None
            queueItem=None
            while serverConnection:
                message = 'testing'
                #returns a data object as a json string
                response = self.listenToSocket(connection)
                print('data response:', response)
                #print('data:',response['data'],response['playerName'],response['activeSessions'],response['activeCommanders'],response['boardType'],player)
                dataObj=Data(data=response['data'],playerName=response['playerName'],activeSessions=response['activeSessions'],activeCommanders=response['activeCommanders'],boardType=response['boardType'])
                if dataObj.data=='requesting player number':
                    dataObj.playerName=player
                #queue the command sent by your client
                #self.queue.put({player:dataObj},timeout=5)
                self.queue[player]=dataObj
                print(self.queue)
                #if what is queued is does not belong to this player:STILL VALID JUST DONT HAVE A PLAYER 2 YET
                #while True:
                opponent=None
                #jurry rigged: I want to eventually have people create usernames. but this is just a 'it will do' logic for this current iteration of the game.
                #maybe I can say: 'check list of players. find you instance. any other instances is your opponent.'
                if player=='player_1':
                    opponent='player_2'
                elif player=='player_2':
                    opponent='player_1'
                else:
                    pass
                if opponent in self.queue.keys():
                    queueItem= self.queue[opponent]
                    queueItem=queueItem.data
                    break
                else:
                    queueItem='waiting for player connection'
                    time.sleep(1)
                            
                
                #if you see that player 2 has data then get it
                #if isinstance(self.queue['player_2_turn'],Data):
                #    queueItem= self.queue['player_2_turn']
                #    queueItem=queueItem.data
                #print("queue:",self.queue.get())
                #queueItem = self.queue.get()
                #queueItem = self.queue[player]
                #queueItem=queueItem.data()
                print("response:",response)
                #if queueItem != None or queueItem=='end turn':
                if queueItem=='end turn':
                    print("Queue:", queueItem)
                    self.waitTurn(queueItem) 
                elif queueItem=='waiting for player connection':
                    message='waiting for other player'
                    dataObj.data=message
                    #self.sendMessage(connection,queueItem)

                self.sendMessage(connection,dataObj)

                # from here down is surpufluice code... fix it
                if dataObj.data == "close client connection" or queueItem == "game over":
                    dataObj.data='closing connection'
                    self.sendMessage(connection,dataObj)
                    serverConnection = False 
                    self.closeConnection()
                
        except Exception as e:
            print(e)
            traceback.print_exc()
       
    #main logic
    def threadProcessing(self,player,player_Turn,connection):
        self.serverThread(player,player_Turn,connection)
        rules = CombatRules()
                
        
    def getResponseCode(self,connection):
        pass

if __name__ == '__main__':
    try:
        server = Server()
        #server.testServer()
        #serverConnect=server.startServer()
        #server.listen(serverConnect)
        #server.sendMessage(serverConnect,"testing")
        #server.closeConnection(serverConnect)
        server.startThreads()
           
            
    except Exception as e:
        print(e)
        traceback.print_exc()
