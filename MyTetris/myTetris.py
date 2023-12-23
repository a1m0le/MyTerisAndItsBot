"""" This is the main tetris game """

import numpy as np
import math

class tile:

    def __init__(self, name):
        self.name = name
        self.rotation = 0

    def rotate(self):
        self.rotation += 1

    def undo_rotate(self):
        self.rotation-=1

class tiles:

    def __init__(self):
        # each one stores the offset from the top left corner and after each rotation
        self.tiles = {}
        self.tiles["I"] = [ [0,0,1,0,2,0,3,0], [0,0,0,1,0,2,0,3]]
        self.tiles["O"] = [[0,0,0,1,1,0,1,1]]
        self.tiles["Z"] = [[0,0,0,1,1,1,1,2]  , [0,1,1,1,1,0,2,0]]
        self.tiles["S"] = [[0,1,1,1,1,0,0,2]  ,  [0,0,1,0,1,1,2,1]]
        self.tiles["T"] = [[0,0,0,1,0,2,1,1]  , [0,1,1,1,1,0,2,1], [0,1,1,0,1,1,1,2]  , [0,0,1,0,2,0,1,1]]
        self.tiles["L"] = [[0,0,0,1,1,1,2,1]  , [1,0,1,1,1,2,0,2]  ,[0,0, 1,0, 2,0, 2,1]  ,[0,0,0,1,0,2,1,0]]
        self.tiles["J"] = [[0,0,1,0,2,0,0,1],  [0,0,0,1,0,2,1,2],  [0,1,1,1,2,1,2,0],  [0,0,1,0,1,1,1,2]]
        self.tile_names=['I','O','Z','S','T','L','J']

    def gen_tile(self):
        prob = np.random.uniform()*7
        return tile(self.tile_names[math.floor(prob)])

    def get_offsets(self, tile):
        return self.tiles[tile.name][tile.rotation % len(self.tiles[tile.name])]



LEFT = -1
RIGHT = 1


class board:
    # define the game board
    def __init__(self):
        self.board=[]
        for i in range(20):
            self.board.append([0]*10)
        # first 6 rows are for tile positions
        self.anchor=(1,3)
        self.dropped = True
        self.tile_location = []

    def prepare_for_new_tile(self):
        self.anchor=(1,3)
        self.tile_location = []


    def place_tile(self, tiles, tile):
        if not self.dropped:
            return
        self.prepare_for_new_tile()
        offsets = tiles.get_offsets(tile)
        for t in range(4):
            i = self.anchor[0]+offsets[2*t]
            j = self.anchor[1]+offsets[2*t+1]
            self.board[i][j] = 1
            self.tile_location.append((i,j))
        self.dropped = False


    def move(self, tiles, tile, direction):
        if self.dropped:
            return
        if direction==LEFT:
            shift = -1
        else:
            shift = 1
        # go left
        prepare_next = []
        for i,j in self.tile_location:
            newj = j + shift
            newi = i
            if newj < 0 or newj > 9 :
                return
            prepare_next.append((newi,newj))
        for i,j in self.tile_location:
            self.board[i][j] = 0
        for i,j in prepare_next:
            self.board[i][j] = 1
        self.tile_location = prepare_next
        self.anchor = (self.anchor[0], self.anchor[1]+shift)

    
    def rotate(self, tiles, tile):
        if self.dropped:
            return
        #rotate about the anccor
        tile.rotate()
        offsets = tiles.get_offsets(tile)
        prepare_next = []
        for t in range(4):
            i = self.anchor[0]+offsets[2*t]
            j = self.anchor[1]+offsets[2*t+1]
            if (j<0 or j>9):
                tile.undo_rotate()
                return
            prepare_next.append((i,j))
        for i,j in self.tile_location:
            self.board[i][j] = 0
        for i,j in prepare_next:
            self.board[i][j] = 1
        self.tile_location = prepare_next

    # very unoptimized
    def drop(self):
        self.dropped = True
        points = 0
        min_drop_dist = 999
        for i,j in self.tile_location:
            # search that j column
            for b in range(i+1, 21):
                if b == 20:
                    min_drop_dist = min(min_drop_dist, b-i-1)
                elif self.board[b][j] == 2:
                    min_drop_dist = min(min_drop_dist, b-i-1)
                    break
        for i,j in self.tile_location:
            di = i + min_drop_dist
            self.board[i][j] = 0
            self.board[di][j] = 2
        # now we calculate points and consolidate
        for i in range(6):
            flag = 0
            for j in range(10):
                flag = flag | self.board[i][j]
                if flag > 0:
                    # GAME OVER
                    return -999
        newi = 19
        oldi = 6 
        for i in range(19, 5, -1):
            flag = 2
            stop_flag = 0
            for j in range(10):
                flag = flag & self.board[i][j]
                stop_flag = stop_flag | self.board[i][j]
            if not stop_flag:
                oldi = i
            if flag == 0:
                # we keep it
                for j in range(10):
                    self.board[newi][j] = self.board[i][j]
                newi -= 1
            else:
                points += 1

        for i in range(oldi, newi+1):
            self.board[i] = [0,0,0,0,0,0,0,0,0,0]
        return max(0,(points*2-1)*100)


        
class tetrisGame:

    def __init__(self, queue=None):
        self.board = board()
        self.score = 0
        self.tiles = tiles()
        self.queued_tiles = queue
        self.currentTile = self.spawn_tile()
        # place the first tile on
        self.board.place_tile(self.tiles, self.currentTile)
        self.gameover = False


    def get_board(self):
        return self.board.board

    def get_score(self):
        return self.score

    def get_tile(self):
        return self.currentTile

    def spawn_tile(self):
        if self.queued_tile is None:
            return self.tiles.gen_tile()
        else:
            return tile(self.queued_tiles.pop(0))

    def is_game_over(self):
        return self.gameover

    def player_moves(self, move):
        if self.gameover:
            return
        if move == 1: # move left
            self.board.move(self.tiles, self.currentTile, LEFT)
            return
        if move == 2: # move right
            self.board.move(self.tiles, self.currentTile, RIGHT)
            return
        if move == 3: # rotate
            self.board.rotate(self.tiles, self.currentTile)
            return
        if move == 4:
            new_points = self.board.drop()
            if new_points < 0:
                self.gameover = True
                return
            self.score += new_points
            self.currentTile = self.spawn_tile()
            self.board.place_tile(self.tiles, self.currentTile)







if __name__ == "__main__":
    #unit tests
    mytiles = tiles()
    print(mytiles.gen_tile())





