import socket,threading,pickle
from sysVar import *
from gameData import GameData
class Network:
    def __init__(self):
        self.__client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__id=int(self.__connect())
    def getId(self):
        return self.__id
    def __connect(self):
        try:
            self.__client.connect(ADDR)
            msg_length = self.__client.recv(HEADER).decode(FORMAT) # first receive msg len
            if msg_length:
                msg_length = int(msg_length)
                msg=self.__client.recv(msg_length).decode(FORMAT)  # then receive msg
                return msg
        except socket.error as e:
            print(e)
    def getGame(self):
        try:
            message = str(self.__id)
            message = message.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b" " * (HEADER - len(send_length))
            self.__client.send(send_length) # first send data length
            self.__client.send(message) # then send data
            data = self.__client.recv(2048*2)
            return  pickle.loads(data)
        except socket.error as e:
            print(e)
    def send(self,message):
        try:
            message = message.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b" " * (HEADER - len(send_length))
            self.__client.send(send_length) # first send data length
            self.__client.send(message) # then send data
        except socket.error as e:
            print(e)
    def sendData(self,data):
        """

        :param data: gameData or endGameData object sending to server
        :return:
        """
        try:
            message = OBJECT_MESSAGE.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b" " * (HEADER - len(send_length))
            self.__client.send(send_length)  # first send data length
            self.__client.send(message)  # then send data
            self.__client.sendall(pickle.dumps(data))
        except socket.error as e:
            print(e)