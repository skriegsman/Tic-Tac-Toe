class consts:
    EMPTY = "-"
    X = "X"
    O = "O"

    #Colors       R    G    B
    BGCOLOR   = (255, 255, 255)
    BLACK     = (  0,   0,   0)
    RED       = (255,   0,   0)
    BLUE      = (  0,   0, 255)
    LIGHTBLUE = (  0, 255, 255)

    #Game Board
    XWIDTH = 20

    #Pygame Constants
    MENUHEIGHT = 50
    WINDOWWIDTH = 900
    WINDOWHEIGHT = 900
    FULLWINDOWHEIGHT = WINDOWHEIGHT + MENUHEIGHT
    FPS = 30

    #Menu Settings
    DIFFICULTY = 0 #Value for the percentage of the time it should make a random move rather than the best move
    ENDSESSION = False #While true the program will quit after one game
    AIGAME = True #While true the AI will play itself
    RANDOMSTART = True #While true the player going first will be random


def other_player(player):
    return consts.X if player == consts.O else consts.O

def all_same(vec):
    return vec[0] == vec[1] == vec[2] != consts.EMPTY
