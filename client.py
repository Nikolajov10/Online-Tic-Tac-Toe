from network import Network
from sysVar import DISCONNECT_MESSAGE
from game import Player,Game
from  gameData import *
import pygame

n = Network()

def handleEvents(game:Game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            x, y = Game.MousePosToTableCord(pos)
            if x != -1 and y != -1:
                game_data = GameData(x,y,game.getId(),n.getId())
                n.sendData(game_data)
    return True

def start():
    run = True
    screen = Game.createWindow()
    while run:
        game = n.getGame()
        game.drawWindow(screen)
        if game.isExited():
            break
        if game.isEnd():
            game.drawEnd(screen)
            end = EndGameData(game.getId(),True)
            n.sendData(end)
            game = n.getGame()
        run = handleEvents(game)

start()
n.send(DISCONNECT_MESSAGE)