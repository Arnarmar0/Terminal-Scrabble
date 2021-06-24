import random
import copy

class Player:
    def __init__(self, name):
        self.name = name
        self.tiles = []
        self.score = 0

class Board:
    def __init__(self):
        self.board = [['.']*15 for _ in range(15)]
        self.multi_board = [[30, 1, 1, 2, 1, 1, 1, 30, 1, 1, 1, 2, 1, 1, 30],
        [1, 20, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 20, 1],
        [1, 1, 20, 1, 1, 1, 2, 1, 2, 1, 1, 1, 20, 1, 1],
        [2, 1, 1, 20, 1, 1, 1, 2, 1, 1, 1, 20, 1, 1, 2],
        [1, 1, 1, 1, 20, 1, 1, 1, 1, 1, 20, 1, 1, 1, 1],
        [1, 3, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 3, 1],
        [1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1],
        [30, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 30],
        [1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1],
        [1, 3, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 3, 1],
        [1, 1, 1, 1, 20, 1, 1, 1, 1, 1, 20, 1, 1, 1, 1],
        [2, 1, 1, 20, 1, 1, 1, 2, 1, 1, 1, 20, 1, 1, 2],
        [1, 1, 20, 1, 1, 1, 2, 1, 2, 1, 1, 1, 20, 1, 1],
        [1, 20, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 20, 1],
        [30, 1, 1, 2, 1, 1, 1, 30, 1, 1, 1, 2, 1, 1, 30]]
    
    def display_board(self):
        print("      a  b  c  d  e  f  g  h  i  j  k  l  m  n  o ")
        for i in range(15):
            if (i < 9):
                print("   " + str(i+1) + "  " + "  ".join(self.board[i]))
            else:
                print("   " + str(i+1) + " " + "  ".join(self.board[i]))

class Bag:
    def __init__(self):
        self.tiles = {
        "E":12, "A":9, "I":9, "O":8, "N":6, "R":6, "T":6, "L":4, "S":4, "U":4,
        "D":4, "G":3, "B":2, "C":2, "M":2, "P":2, "F":2, "H":2, "V":2, "W":2,
        "Y":2, "K":1, "J":1, "X":1, "Q":1, "Z":1}

        self.tile_values = {
        "E":1, "A":1, "I":1, "O":1, "N":1, "R":1, "T":1, "L":1, "S":1, "U":1,
        "D":2, "G":2, "B":3, "C":3, "M":3, "P":3, "F":4, "H":4, "V":4, "W":4,
        "Y":4, "K":5, "J":8, "X":8, "Q":10, "Z":10}
    
    def draw_tile(self):
        drawn_tile = random.choice(list(self.tiles))
        if self.tiles[drawn_tile] == 1:
            del self.tiles[drawn_tile]
        else:
            self.tiles[drawn_tile] -= 1
        return drawn_tile
    
    def has_tiles(self):
        return bool(self.tiles)
    
    def num_tiles(self):
        numTiles = 0
        for letter in self.tiles:
            numTiles += self.tiles[letter]
        return numTiles

class Dictionary:
    def __init__(self, filename):
        self.dict_set = set()
        fileobject = open(filename, "r")
        for line in fileobject:
            if line != "\n":
                self.dict_set.add(line.split()[0].upper())

            