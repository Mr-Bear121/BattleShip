import sys
import os
import subprocess
import time
sys.path.append(f'{os.getcwd}\\..')
print(sys.path)
from Client.Client import Client
from Client.DataIntermediary import Data


if __name__ == '__main__':
    #the reason why this server is probably not working might bne because it encounters a catostrpohic error then dies... meaning it doesnt print the error
    serverProcess=subprocess.Popen('python Server/Server.py')
    client2Process=subprocess.Popen('python Client/Client.py')
    client=Client.createClient()
    data=Data(data='testing connection')
    client.openConnection()
    client.sendMessage(data)
    response=client.receiveMessage()
    print('client 1:',response)