from classes import *

# This can be changed if dictionary file changes
DICT_FILE = "Collins Scrabble Words (2019) with definitions.txt"
DIV = "\n" + "-" * 30 + "\n"

class Game:
    def __init__(self):
        self.board = Board()
        self.playerlist = []
        self.bag = Bag()
        self.dictionary = Dictionary(DICT_FILE)
        self.cur_player = 0
        self.skip_counter = 0
        self.first_turn = True
    
    # Adds up to four players
    def add_players(self):
        print("How many players will be playing?")
        number = input("2-4: ")
        for i in range(1, int(number) + 1):
            self.playerlist.append(Player(input("Input name of player {}: ".format(i))))

    # The function that plays the game, utilizes different functionality based on user choice
    def play(self):
        self.add_players()
        while self.skip_counter != 2 and self.bag.has_tiles():
            for i in range(len(self.playerlist)):
                self.cur_player = i
                print(DIV + "{}'s turn!".format(self.playerlist[self.cur_player].name) + "\n")
                self.draw_tiles()
                print("Your tiles: {}".format(self.playerlist[i].tiles))
                choice = self.pick_choice()
                temp_score = copy.deepcopy(self.playerlist[i].score)
                if choice == "p":
                    self.skip_counter = 0
                    self.board.display_board()
                    print("Your tiles: {}".format(self.playerlist[i].tiles))
                    if self.add_word():
                        self.board.display_board()
                        print("Score for last word: {}".format(self.playerlist[i].score - temp_score))
                elif choice == "e":
                    self.skip_counter = 0
                    if self.exchange() == False:
                        break
                    print("Your new tiles: {}\n".format(self.playerlist[self.cur_player].tiles))
                    print("There are {} tiles left in the bag".format(self.bag.num_tiles()))
                elif choice == "s":
                    self.skip_counter += 1
                    if self.skip_counter >= 2:
                        break    
        self.print_score()
        print("\nThank you for playing!")

    # Gives user the choice to pick between playing, exchanging tiles or skipping
    def pick_choice(self):
        print("Choose whether to play, exchange tiles or skip")
        choice = input("p/e/s: ")
        return choice
    
    # Draws seven tiles from the bag, if bag is empty then return false
    def draw_tiles(self):
        if self.bag.has_tiles():
            for _ in range(len(self.playerlist[self.cur_player].tiles), 7):
                self.playerlist[self.cur_player].tiles.append(self.bag.draw_tile())
        else:
            print("Bag is empty. Game over!")
            return False

    # Iterates through list of players and prints score for each player
    def print_score(self):
        print("\nScoreboard:")
        for i in range(len(self.playerlist)):
            print("{}: {}".format(self.playerlist[i].name, self.get_score(i)))
    
    # Deletes tiles user does not want and draws new tiles for the ones the user exchanged
    def exchange(self):
        print("What tiles are you exchanging?")
        to_exchange = input("Tiles with ',' between, f.x. 'A,B': ")
        self.delete_tiles(to_exchange.replace(",","").upper())
        if self.draw_tiles() == False:
            return False

    # Automatically places first word in center of board. If not first turn then asks user for
    # coordinates of word placement and iterates through letters in word and places each letter
    # in corresponding space in board. If letter falls on double or triple word value, the word
    # score is doubled/tripled.
    def add_word(self):
        print("What word are you going to play?")
        word = (input("Word: ")).upper()
        if self.first_turn:
            x = 7
            y = 7
        else:
            print("What will be the coordinates of x?")
            x = ord(input("a-o: ")) - 97
            print("What will be the coordinates of y?")
            y = int(input("1-15: ")) - 1
        print("Will the word be placed vertical or horizontal?")
        orientation = input("h/v: ")
        temp_board = copy.deepcopy(self.board.board)
        word_score = 0
        multiplier = None
        new_word = ""
        connected = False
        for letter in word.upper():
            if self.board.board[y][x] != '.' and self.board.board[y][x] != letter:
                self.board.board = temp_board
                print("Word does not fit there")
                return False
            if self.board.board[y][x] != '.':
                connected = True
            elif self.board.board[y][x] != letter:
                new_word += letter
            self.board.board[y][x] = letter
            if self.calculate_score(letter, x, y) == "Double":
                multiplier = 2
                word_score += self.bag.tile_values[letter]
            elif self.calculate_score(letter, x, y) == "Triple":
                multiplier = 3
                word_score += self.bag.tile_values[letter]
            else:
                word_score += self.calculate_score(letter, x, y)
            if orientation == "v":
                y += 1
            elif orientation == "h":
                x += 1
        if self.check_word(word, new_word) == False:
            self.board.board = temp_board
            return
        if connected == False and self.first_turn != True:
            print("\nWords must connect with other words")
            self.board.board = temp_board
            return
        if len(self.playerlist[self.cur_player].tiles) == 0:
            self.playerlist[self.cur_player].score += 50
        if multiplier != None:
            word_score *= multiplier
        self.playerlist[self.cur_player].score += word_score
        self.delete_tiles(new_word)
        self.first_turn = False
        return True
    
    # Calculates the score of each placed tile. If tile lands on double or triple board value,
    # the function returns the strings "double" or "triple" which are then used in the add_word
    # function to multiply the word value
    def calculate_score(self, letter, x, y):
        if self.board.multi_board[y][x] != 20 and self.board.multi_board[y][x] != 30:
            return self.bag.tile_values[letter] * (self.board.multi_board[y][x])
        elif self.board.multi_board[y][x] == 20:
            return "Double"
        elif self.board.multi_board[y][x] == 30:
            return "Triple"
    
    # Deletes used tiles.
    def delete_tiles(self, word):
        for letter in word:
            for i in range(len(self.playerlist[self.cur_player].tiles)):
                if self.playerlist[self.cur_player].tiles[i] == letter:
                    del self.playerlist[self.cur_player].tiles[i]
                    break
                i += 1
    
    def get_score(self, player_no):
        return self.playerlist[player_no].score

    # Checks if player has all required letters, checks if word is in dictionary and checks
    # if all neighboring words are legal relative to the new word placement
    def check_word(self, word, new_word):
        for letter in new_word:
            if letter.upper() not in self.playerlist[self.cur_player].tiles:
                print("You don't have the letter {}".format(letter.upper()))
                return False
        if word in self.dictionary.dict_set and self.check_all_words():
            return True
        elif word not in self.dictionary.dict_set:
            print("\nThis word is not a word in the english dictionary!")
            return False
        if self.check_all_words() == False:
            print("Neighboring words won't work if you place these tiles there")
            return False
    
    # Iterates through the newly created board to check if all neighboring words are legal
    # relative to the new word placement. First it checks vertical words, then horizontal.
    # If it finds word that is illegal, it reverts board to last position.
    def check_all_words(self):
        x = 0
        y = 0
        word = ""
        while x != 15:
            for i in range(15):
                if self.board.board[i][x] != '.':
                    word += self.board.board[i][x]
                elif self.board.board[i][x] == '.' and word != "":
                    if len(word) != 1:
                        if word not in self.dictionary.dict_set:
                            return False
                    word = ""
            x += 1
        while y != 15:
            for i in range(15):
                if self.board.board[y][i] != '.':
                    word += self.board.board[y][i]
                elif self.board.board[y][i] == '.' and word != "":
                    if len(word) != 1:
                        if word not in self.dictionary.dict_set:
                            return False
                    word = ""
            y += 1
        return True


if __name__ == "__main__":
    game = Game()
    game.play()