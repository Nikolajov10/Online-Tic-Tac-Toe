import socket
import pickle
import threading
from sysVar import *
from game import Game,Player
from gameData import GameData,EndGameData

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # init server , IPV4
server.bind(ADDR)

id=0
games = []
players = []

def clientConnection(conn:socket.socket, addr):
    print(f"[NEW_CONNECTION] {addr} with id={id} connected...")
    connected=True
    str_id=str(id)
    message = str_id.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    conn.send(send_length)  # first send data length
    conn.send(message)  # then send data
    while connected:
        msg_length=conn.recv(HEADER).decode(FORMAT)

        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected=False
                if int(str_id) % 2 == 1:
                    games[int(str_id) // 2].exitGame()
                else:
                    games[int(str_id) // 2 - 1].exitGame()
            elif msg == OBJECT_MESSAGE:
                g = pickle.loads(conn.recv(2048 * 2))
                if isinstance(g,GameData):
                    game:Game = games[g.id - 1]
                    game.play(g.x,g.y,g.p_id)
                elif isinstance(g,EndGameData):
                    game = games[g.id - 1]
                    if g.end:
                        game.endGame()
            else:
                if int(msg) <= id:
                    try:
                        game = games [(int(msg) - 1) // 2]
                    except IndexError:
                        connected = False
                    try:
                        conn.sendall(pickle.dumps(game))
                    except:
                        pass
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] server is listening on {SERVER}")
    while True:
        conn,addr = server.accept()
        global id
        id += 1
        g = None
        p = Player(id)
        players.append(p)
        if id % 2 == 1:
            g = Game(id // 2 + 1)
            g.setPlayer1(p)
            games.append(g)
            print("Created a new Game with id " + str(id // 2 + 1))
        else:
            g = games[id // 2 - 1]
            g.setPlayer2(p)
        thread = threading.Thread(target=clientConnection,args=(conn,addr))
        thread.start()
        print("[ACTIVE CONNECTIONS] " + str(threading.activeCount()-1)) # -1 because we always have main as active thread
print("[STARTING] server is starting...")
start()