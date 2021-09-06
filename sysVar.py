import socket

# initialazing data

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
HEADER = 64 # len in bytes
ADDR = (SERVER,PORT)
FORMAT = "UTF-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
OBJECT_MESSAGE = "OBJECT"