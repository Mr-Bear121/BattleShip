import sys
import os
import socket
import json
import traceback
#sys.path.append('..')
sys.path.append(f'{os.getcwd()}\\Client')
sys.path.append(f'{os.getcwd()}\\Abstractions')
print('sys path:',sys.path)
from DataIntermediary import Data
#from Abstractions.Client_Server.ABCClient import ABCClient
from Client_Server.ABCClient import ABCClient

class Client(ABCClient):

    def __init__(self,address='192.168.56.1',port=80,connection=socket.socket(socket.AF_INET, socket.SOCK_STREAM),bufferSize=4069):
        super().__init__(address,port,connection)
        self.bufferSize=bufferSize
        self.isClientConnected=False

    @staticmethod
    def createClient(address='192.168.56.1',port=80,bufferSize=4069):
        return Client(address=address,port=port,connection=socket.socket(socket.AF_INET, socket.SOCK_STREAM),bufferSize=bufferSize)
        
    def connectClient(self,message):
        response=''
        #zClient = self.client.connect((self.address,self.socket))
        zClient = self.client
        zClient.connect((self.address,self.port))
        while True:
            message=input('message:')
            #print(message)
            #print(str(message).encode())
            zClient.send(str(message).encode('ascii'))
            response = zClient.recv(4096)
            print(response.decode('ascii'))
            #if response.decode('ascii')=='end transaction':
            #    zClient.close()
            #    break
        return response.decode('ascii')

    def openConnection(self):
        #self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connection.connect((self.address,self.port))
        self.isClientConnected=True

    def returnConnection(self):
        return self.connection

    def closeConnection(self):
        self.connection.close()

    def sendMessage(self,message):
        #print(type(client))
       #self.connection.send(str(message).encode('ascii'))
       #what does it mean to be serializable?
       #apparently the format of active sessions is disliked. I dont believe I need to send it so might as well as remove it for now
       message.activeSessions=None
       serialize=json.dumps(message, default=lambda o: o.__dict__)
       self.connection.send(serialize.encode('ascii'))
 
    def receiveMessage(self):
        data = self.connection.recv(16777216)
        message=json.loads(data)
        return message


if __name__ == '__main__':
    try:
        client=Client()
        data=Data(data='testing connection')
        client.openConnection() 
        client.sendMessage(data)    
        response=client.receiveMessage()      
        print('subprocess:',response)
            
    except Exception as e:
        print(e)
        traceback.print_exc()


'''if __name__ == '__main__':
    
    gameCommands ="command:end_turn:cell:{Cell},end:game over"
    client = Client()
    client2 = Client()
    resp1 = client.connectClient(message=gameCommands)
    resp2 = client2.connectClient(message=gameCommands)
    print('respl:',resp1,resp2)
    while True:
        if resp1 != None or resp2 != None:
            client.connectClient(message=gameCommands)
            client2.connectClient(message=gameCommands)'''
