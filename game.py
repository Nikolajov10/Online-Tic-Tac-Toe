import pygame
import time

from network import Network
class Player:
    def __init__(self,id):
        self.__score=0
        self.__id = id
    def getId(self):
        return self.__id
    def getScore(self):
        return self.__score
    def __iadd__(self, num):
        self.__score += num
        return self
class Table:
    SIZE = 3
    X = 10
    O = 1
    def __init__(self):
        self.__table=[]
        for i in range(Table.SIZE):
            self.__table.append([0]*Table.SIZE)
        self.__count = 0
        self.__on_move = 0
    def clean(self):
        self.__table = []
        for i in range(Table.SIZE):
            self.__table.append([0] * Table.SIZE)
        self.__count = 0
        self.__on_move = 0
    def getPos(self,x,y):
        """
        :param x: row
        :param y: column
        :return: 0 - empty, O - 1 , X - 10
        """
        return self.__table[x][y]
    def getCount(self):
        return self.__count
    def insert(self,x,y):
        if self.__table[x][y] != 0:
            return False
        if self.__on_move == 0:
            self.__table[x][y] = Table.X
        else:
            self.__table[x][y] = Table.O
        self.__on_move = (self.__on_move + 1) % 2
        self.__count += 1
        return True

    def checkWinner(self):
        """

        :return: 0 - draw , 1 - X win , 2 - O win
        """
        winner = 0
        # check horizontaly,verticaly and diagonaly for winner
        hor = [0,0,0]
        ver =[0,0,0]
        d1= 0
        d2 = 0
        O_win = Table.O * 3
        X_win = Table.X * 3
        for i in range(Table.SIZE):
            for j in range(Table.SIZE):
                hor[i] += self.__table[i][j]
                ver[i] += self.__table[j][i]
                if i == j:
                    d1+=self.__table[i][j]
                if i+j == 2:
                    d2 += self.__table[i][j]
                if d1 == O_win or d2 == O_win:
                    winner = 2
                elif d1 == X_win or d2 == X_win:
                    winner = 1
                else:
                    if hor[i] == O_win or ver[i] == O_win:
                        winner = 2
                    elif hor[i] == X_win or ver[i] == X_win:
                        winner =1
            if winner != 0:
                break
        return winner

    def onMove(self)->chr:
        return 'x' if self.__on_move == 0 else 'o'

class Game:
    WIDTH = 600
    HEIGHT = 600
    LIGHT_GRAY = (211,211,211)
    BLACK = (0,0,0)
    RED = (200,0,0)
    BlUE = (0,0,200)
    GREEN = (0,200,0)
    FONT_SIZE = 30
    def __init__(self,id,p1:Player=None,p2:Player=None):
        self.__id = id
        self.__p1 = p1
        self.__p2 = p2
        self.__x_id = None if not p1 else p1.getId()
        self.__o_id = None if not p2 else p2.getId()
        self.__player_x = 0
        self.__on_move = 1
        self.__table=Table()
        self.__winner = None
        self.__exit = False
    def getId(self):
        return self.__id
    @staticmethod
    def createWindow():
        pygame.init()
        screen = pygame.display.set_mode((Game.WIDTH,Game.HEIGHT))
        pygame.display.set_caption("Tic-Tac-Toe")
        return screen
    def drawWindow(self,screen):
        screen.fill((Game.LIGHT_GRAY))
        if (not self.__p1) or (not self.__p2):
            text = "Waiting for player..."
            font = pygame.font.SysFont("Comic Sans MS",Game.FONT_SIZE,bold=True)
            text = font.render(text,True,Game.RED)
            screen.blit(text,((Game.WIDTH - text.get_width())//2 ,(Game.HEIGHT - text.get_height())//2))
        else:
            # drawing scores
            text1 = "Score Player1:  "+str(self.__p1.getScore())
            font = pygame.font.SysFont("Comic Sans MS", Game.FONT_SIZE//2 + 5)
            text1 = font.render(text1, True, Game.BLACK)
            screen.blit(text1, (0,0))
            text2 = "Score Player2:  " + str(self.__p2.getScore())
            font = pygame.font.SysFont("Comic Sans MS", Game.FONT_SIZE // 2 + 5 )
            text2 = font.render(text2, True, Game.BLACK)
            screen.blit(text2, (Game.WIDTH - text2.get_width() - 10 , 0))
            # drawing lines
            offset = ((Game.WIDTH + Game.HEIGHT) //2 ) // 10
            for i in range(2):
                x = Game.WIDTH // 3 * (i+1)
                y_start= offset - Game.HEIGHT // 60
                y_end = Game.HEIGHT - offset + Game.HEIGHT // 60
                pygame.draw.line(screen,Game.BLACK,(x,y_start),(x,y_end),offset // 6) # vertical lines
                y = Game.HEIGHT // 3 * (i+1)
                x_start = offset - Game.HEIGHT // 60
                x_end = Game.WIDTH - offset + Game.HEIGHT // 60
                pygame.draw.line(screen,Game.BLACK,(x_start,y),(x_end,y),offset // 6) # horizontal lines
            # drawing X and O
            for i in range(Table.SIZE):
                for j in range(Table.SIZE):
                    value = self.__table.getPos(i,j)
                    if value != 0:
                        if value == Table.X:
                            # draw X
                            # first line
                            x_start = offset // 2 + Game.WIDTH // 3 * j + 18 // (j+1)
                            x_end = (Game.WIDTH - offset // 3) // 3 * (j +  1) - 18 // (j+1)
                            y_start = offset // 2 + Game.HEIGHT // 3 * i + 18 // (i+1)
                            y_end = (Game.HEIGHT - offset // 3)  // 3 * (i +  1) - 18 // (i+1)
                            pygame.draw.line(screen,Game.RED,(x_start,y_start),(x_end,y_end),8)
                            #second line
                            x_start , x_end = x_end , x_start
                            pygame.draw.line(screen, Game.RED, (x_start, y_start), (x_end, y_end), 8)
                        else:
                            # draw O
                            x = Game.WIDTH // 3 * (j+1) - Game.WIDTH // 6 - 3
                            y = Game.HEIGHT // 3 * (i+1) - Game.HEIGHT // 6 - 3
                            pygame.draw.circle(screen,Game.BlUE,(x,y),offset * 5 // 6,10)
        pygame.display.update()
    @staticmethod
    def MousePosToTableCord(pos:tuple):
        """
        :param pos: mouse position on click
        :return: x,y cordinates in table
        """
        offset = ((Game.WIDTH + Game.HEIGHT) // 2) // 10 - (Game.HEIGHT+Game.WIDTH)//120
        x=y=0
        if pos[0] < offset or pos[0] > Game.WIDTH - offset:
            x = -1
        else:
            x = pos[0] // ((Game.WIDTH - offset + 30 ) // 3) # add 30 because of lines width
        if pos[1] < offset or pos[1] > Game.HEIGHT - offset:
            y = -1
        else:
            y= pos[1] // ((Game.HEIGHT - offset + 30 ) // 3) # add 30 because of lines width
        return x,y
    def drawEnd(self,screen):
        """

        :param winner: outcome of game
        :return:
        """
        text = "DRAW!"
        x = 0 if self.__player_x==1 else 1
        o = 0 if x==1 else 1
        if self.__winner == 1:
            text = f"PLAYER {x+1} WIN!"
        elif self.__winner == 2:
            text = f"PLAYER {o+1} WIN!"
        font = pygame.font.SysFont("Comic Sans MS", Game.FONT_SIZE )
        text = font.render(text, True, Game.GREEN)
        screen.blit(text, (Game.WIDTH//2 - text.get_width()//2, Game.HEIGHT//2 - text.get_height()//2))
        pygame.display.update()
        time.sleep(1.5)
    def isEnd(self):
        return self.__winner != None

    def endGame(self):
        self.__winner = None
        self.__table.clean()

    def __endGame(self,winner):
        self.__winner = winner
        if winner == 1:
            if self.__player_x == 0:
                self.__p1 += 1
            else:
                self.__p2 += 1
        elif winner == 2:
            if self.__player_x == 1:
                self.__p1 += 1
            else:
                self.__p2 += 1
        self.__player_x = (self.__player_x + 1) % 2
        self.__x_id , self.__o_id = self.__o_id , self.__x_id

    def play(self,x,y,player_id):
        trying_to_move = 'x' if self.__x_id == player_id else 'o'
        if trying_to_move != self.__table.onMove():
            return
        self.__table.insert(y,x)
        if self.__table.getCount() >= 5:
            win = self.__table.checkWinner()
            if (win == 1 or win == 2) or self.__table.getCount() == 9:
                self.__endGame(win)
    def setPlayer2(self,p2):
        if not self.__p2:
            self.__p2 = p2
            self.__o_id = p2.getId()
    def setPlayer1(self,p1):
        if not self.__p1:
            self.__p1 = p1
            self.__x_id = p1.getId()

    def exitGame(self):
        self.__exit = True
    def isExited(self):
        return self.__exit


