class GameData:
    def __init__(self,x,y,id,player_id):
        self.x = x
        self.y = y
        self.id = id
        self.p_id = player_id
class EndGameData:
    def __init__(self,id,end_flag):
        self.id = id
        self.end = end_flag