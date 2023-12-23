"""Display and allow player of tetris"""""

import os
import myTetris
import vlc


def refresh_display():
    os.system("clear")
    print()
    print()
    print()
    print()


def gprint(content):
    print("                ",end="",flush=True)
    print(content,flush=True)



def display_score(game):
    gprint("    Score: "+str(game.get_score()))
    gprint("")




def display_board(game):
    board = game.get_board()
    bottomJ = None
    for i in range(0,len(board)):
        if i==5:
            line=">|"
        else:
            line=" |"
        for j in range(0,10):
            if board[i][j]>0:
                line += "[]"
                if i <= 4:
                    bottomJ = j
            else:
                if i>4 and j == bottomJ:
                    line+=".."
                else:
                    line += "  "
        if i == 5:
            line += "|<"
        else:
            line += "|"
        gprint(line)
    gprint("  TTTTTTTTTTTTTTTTTTTT")

def display_instruction():
    print()
    print()
    print(" (A=left D=right W=rotate S=drop)")
    print("Type the command and press enter: ",end="")



def display_all(game):
    refresh_display()
    display_score(game)
    display_board(game)
    display_instruction()



# AI will produce a list of tiles that will appear in their order by a list as queue.
# AI will also produce a list of moves it will take


if __name__=="__main__":
    p = vlc.MediaPlayer("bgm.mp3")
    p.play()
    AIplayed_queue = []
    AImoves = []
    game = myTetris.tetrisGame(AIplayed_queue)
    mapping = {'a':1,'d':2,'w':3,'s':4}
    for i in range(0, len(AImoves)):
        display_all(game)
        cmd = input()
        game.player_moves(AImoves[0])
    display_all(game)
    print(" GAME OVER !!!!!!!!!")







            

