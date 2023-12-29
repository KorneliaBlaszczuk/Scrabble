import pygame
from constants import (
    ROWS,
    COLS,
    CINEREOUS,
    BEAVER,
    CENTRAL_COLOR,
    SQUARE_SIZE,
    EXTRA_SQUARES,
    extra_space_x,
)
import random
from letters_bag import letters, blank_list
from tiles import Tile


class Board:
    """
    Class Board

    Manages game board, letters bag and the visble side of the game.
    It enables to draw board squares and a place for player's rack.

    :param board: Game Board
    :type board: 2D list

    :param word_list: List of all the words on the board
    :type word_list: list

    :param letters_bag: List of all the avaible letter tiles in the
    bag with its amount and value
    :type letters_bag: dict

    """

    def __init__(self):
        self.board = []
        self._word_list = []
        self.letters_bag = letters.copy()

    @property
    def word_list(self):
        return self._word_list

    @property
    def all_letters(self):
        return self.letters_bag.keys()

    def create_board(self):
        """
        Makes a 2 dimensional board, where the empty spots,
        that are avaible to put a letters, are mark as ""
        """
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                self.board[row].append("")
        return self.board

    def update_board(self, current_word):
        """
        Adds current word (letters) to board
        """
        for pos in current_word:
            row, col = pos
            self.board[row][col] = current_word[pos]
        return self.board

    def remove_from_board(self, current_word):
        """
        Removes current word from board
        """
        for pos in current_word:
            row, col = pos
            self.board[row][col] = ""
        return self.board

    def update_word_list(self, word):
        """
        Appends a word list
        """
        self.word_list.append(word)
        return self.word_list

    def draw_rack(self, rack, rack_sprite):
        """
        Draw tiles on the player's rack
        """
        x = extra_space_x
        y = (COLS + 1) * SQUARE_SIZE
        for current_letters in rack:
            if current_letters == "":
                x += SQUARE_SIZE
            else:
                letter_title = Tile(current_letters, (x, y))
                rack_sprite.add(letter_title)
                x += SQUARE_SIZE

    def draw_tiles(self, board_sprite, current_letter, pos):
        """
        Draw tile on the board
        """
        row, col = pos
        letter_tile = Tile(current_letter, self.row_col_to_coord(row, col))
        board_sprite.add(letter_tile)

    def taking_out(self):
        """
        Returns a random value from a letters bag.
        Used in rack construction.
        """
        all_letters = []
        for letter in self.letters_bag:
            if self.letters_bag[letter][0] > 0:
                all_letters.append(letter)
        chosen_letter = random.choice(all_letters) if all_letters else ""
        return chosen_letter

    def draw_squares(self, win):
        """
        Manages a visual aspect of the board (draws it)
        """
        for row in range(ROWS):
            """
            Color depends on the row and column
            """
            for col in range(COLS):
                color = (
                    CENTRAL_COLOR
                    if row == col == 7
                    else (CINEREOUS if (row + col) % 2 == 0 else BEAVER)
                )
                pygame.draw.rect(
                    win,
                    color,
                    (
                        row * SQUARE_SIZE,
                        col * SQUARE_SIZE,
                        SQUARE_SIZE,
                        SQUARE_SIZE,
                    ),
                )

    def draw_rack_squares(self, win):
        """
        Draws a player's rack
        """
        for i in range(EXTRA_SQUARES):
            x = SQUARE_SIZE * 4 + i * SQUARE_SIZE
            y = (COLS + 1) * SQUARE_SIZE
            color = CINEREOUS if i % 2 == 0 else BEAVER
            pygame.draw.rect(win, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

    def row_col_to_coord(self, row, col):
        """
        Converts row and column number to proper coordinates
        """
        y = row * SQUARE_SIZE
        x = col * SQUARE_SIZE
        return x, y

    def coord_to_row_col(self, position):
        """
        Converts coordinates to suitable row and column number
        """
        x, y = position
        row = y // (SQUARE_SIZE)
        col = x // (SQUARE_SIZE)
        return row, col

    def valid_added_word(self, current_word):
        """
        Checks if the placement of added word
        is correct
        """
        word_coord = self.addword(current_word)
        print(word_coord)
        for i in range(len(word_coord[1]) - 1):
            if word_coord[1][i] + 1 != word_coord[1][i + 1]:
                return False
        if type(word_coord[0][0]) is tuple:  # checks which argument is a tuple
            coord = word_coord[0][0]
            col = word_coord[0][1]
            if all(element != 0 for element in coord):
                # checks if there is a empty space
                if all(self.board[row][col] != "" for row in range(coord[0], coord[1])):
                    return True
                else:
                    return False
        else:
            coord = word_coord[0][1]
            row = word_coord[0][0]
            if all(element != 0 for element in coord):
                if all(self.board[row][col] != "" for col in range(coord[0], coord[1])):
                    return True
                else:
                    return False
        return True

    def addword(self, current_word):
        """
        Function finds the empty space between
        put letters and returns start, end and
        constant paramether.
        If there is not empty space, then start and end
        return both zero
        """
        suffix = []
        word_coord = []
        start = 0
        row = [item[0] for item in current_word.keys()]
        col = [item[1] for item in current_word.keys()]
        if all(x == col[0] for x in col):
            const = col[0]
            count = row[0]
            for coord in row:
                if coord == count:
                    count += 1
                else:
                    if start == 0:
                        start = count
                    suffix.append(coord)
                    count += 1
            end = suffix[0] if suffix else 0
            word_coord = [(start, end), const]
        if all(x == row[0] for x in row):
            const = row[0]
            count = col[0]
            for coord in col:
                if coord == count:
                    count += 1
                else:
                    if start == 0:
                        start = count
                    suffix.append(coord)
                    count += 1
            end = suffix[0] if suffix else 0
            word_coord = [const, (start, end)]
        return word_coord, suffix

    def not_valid(self, board_sprite, current_word, player):
        """
        Action called in a situation when the wrong move was made by player
        """
        for tile in board_sprite:
            for pos in current_word:
                letter_x, letter_y = self.row_col_to_coord(pos[0], pos[1])
                if (tile.letter() == current_word[pos]) and (
                    tile.position() == (letter_x, letter_y)
                ):
                    board_sprite.remove(tile)
                    pygame.display.flip()
                player.reinstate_rack(current_word[pos])

    def alone_tile(self, pos):
        """
        Checks if the tile is alone. You cannot place a single tile, as
        a word is scrabble
        """
        let_row, let_col = pos
        if (
            (
                (let_row + 1 < len(self.board))
                and (self.board[let_row + 1][let_col] != "")
            )
            or (let_row - 1 >= 0 and self.board[let_row - 1][let_col] != "")
            or (let_col - 1 >= 0 and self.board[let_row][let_col - 1] != "")
            or (
                let_col + 1 < len(self.board[let_row])
                and self.board[let_row][let_col + 1] != ""
            )
        ):
            return False
        else:
            return True

    def not_touching(self, row_start, col_start, position, word):
        """
        Checks if the word is alone
        """
        valid_con = []
        if position == "horizontal":
            if row_start != 0:
                if all(
                    0 <= (col_start + k) < 15
                    and self.board[row_start - 1][col_start + k] == ""
                    for k in range(len(word))
                ):
                    valid_con.append(True)
                else:
                    valid_con.append(False)
            if row_start != 14:
                if all(
                    0 <= (col_start + k) < 15
                    and self.board[row_start + 1][col_start + k] == ""
                    for k in range(len(word))
                ):
                    valid_con.append(True)
                else:
                    valid_con.append(False)
            if col_start != 0:
                if self.board[row_start][col_start - 1] == "":
                    valid_con.append(True)
                else:
                    valid_con.append(False)
            if col_start + len(word) < 15:
                if self.board[row_start][col_start + len(word)] == "":
                    valid_con.append(True)
                else:
                    valid_con.append(False)
        else:
            if col_start != 0:
                if all(
                    0 <= (row_start + k) < 15
                    and self.board[row_start + k][col_start - 1] == ""
                    for k in range(len(word))
                ):
                    valid_con.append(True)
                else:
                    valid_con.append(False)
            if col_start != 14:
                if all(
                    0 <= (row_start + k) < 15
                    and self.board[row_start + k][col_start + 1] == ""
                    for k in range(len(word))
                ):
                    valid_con.append(True)
                else:
                    valid_con.append(False)
            if row_start != 0:
                if self.board[row_start - 1][col_start] == "":
                    valid_con.append(True)
                else:
                    valid_con.append(False)
            if row_start + len(word) < 15:
                if self.board[row_start + len(word)][col_start] == "":
                    valid_con.append(True)
                else:
                    valid_con.append(False)
        return valid_con

    def colid(self, board_sprite, current_next_pos):
        """
        Checks if on the position there is not a tile
        """
        row = current_next_pos[1][0]
        col = current_next_pos[1][1]
        for letter in board_sprite:
            letter_row, letter_col = self.coord_to_row_col(letter.position())
            if letter_row == row and letter_col == col:
                return True
            else:
                continue
        return False

    def check_row(self):
        """
        Searches rows for words
        """
        current_word = []
        check_word = []
        for row in self.board:
            for e, element in enumerate(row):
                if element != "":
                    current_word.append(element)
                    if ((e + 1) != len(row) and (row[e + 1] == "")) or (
                        (e + 1) == len(row)
                    ):
                        check_word.append("".join(current_word))
                        current_word = []
        return check_word

    def check_col(self):
        """
        Searches a columns for words
        """
        current_word = []
        check_word = []

        for col in range(15):
            for row in range(15):
                element = self.board[row][col]
                if element != "":
                    current_word.append(element)
                    if (row + 1) != 15 and (self.board[row + 1][col] == ""):
                        check_word.append("".join(current_word))
                        current_word = []
                    elif (row + 1) == 15:
                        if len(current_word) > 1:
                            check_word.append("".join(current_word))
                        current_word = []
        return check_word

    def word_in_board(self):
        """
        Return a list of words from board meeting the requirements
        """
        words = [
            word
            for word in (self.check_row() + self.check_col())
            if len(word) > 1 and len(word) < 6
        ]
        return words

    def word_authentication(self, word, words):
        """
        Checks if the word is valid (in the list of authentic words).
        Function also manages blank tiles
        """
        blank = [e for e, letter in enumerate(word) if letter == " "]
        letter_list = list(word)

        if len(blank) == 2:
            for letter1 in blank_list:
                for letter2 in blank_list:
                    letter_list[blank[0]] = letter1
                    letter_list[blank[1]] = letter2
                    check_word = "".join(letter_list).lower()
                    if check_word in words:
                        return True
            return False
        else:
            for e, letter in enumerate(letter_list):
                if letter == " ":
                    for let in blank_list:
                        letter_list[e] = let
                        checked_word = "".join(letter_list).lower()
                        if checked_word not in words:
                            if let != blank_list[-1]:
                                continue
                            else:
                                return False
                        return True
                else:
                    continue
            checked_word = word.lower()
            if checked_word in words:
                return True
            else:
                return False

    def word_checking(self, words):
        """
        Checks if all the words on the board are valid
        """
        for word in self.word_in_board():
            if self.word_authentication(word, words):
                continue
            else:
                return False
        return True

    def word_lists_adding(self, player):
        """
        Adds the word to the personal word list of certain player
        """
        for word in self.word_in_board():
            count = self.word_in_board().count(word)
            word_amount = self.word_list.count(word)
            if count == 1:
                if word in self.word_list:
                    continue
                else:
                    self.update_word_list(word)
                    player.update_words(word)
            else:
                while count != word_amount:
                    self.update_word_list(word)
                    player.update_words(word)
                    word_amount += 1
        return self.word_list

    def validation(self, board_sprite, words, current_word, player):
        """
        Manages all the validation proces of word made by player
        """
        if self.word_checking(words):
            self.word_lists_adding(player)
            print("valid")
        else:
            print("invalid")
            self.not_valid(board_sprite, current_word, player)
            self.remove_from_board(current_word)

    def exist(self, word):
        """
        Checks if the word exists and on which coordinates
        """
        pos = []

        find_word = []
        word = word.upper()
        for col in range(15):
            for row in range(15):
                element = self.board[row][col]
                if element != "" and element in word:
                    find_word.append(element)
                    if "".join(find_word) == word:
                        start_row = row - len(find_word) + 1
                        if self.not_touching(start_row, col, "vertical", word):
                            pos = ["vertical", start_row, col]
                            return pos
                else:
                    find_word.clear()

        for row in range(15):
            for col in range(15):
                element = self.board[row][col]
                if element != "" and element in word:
                    find_word.append(element)
                    if "".join(find_word) == word:
                        start_col = col - len(find_word) + 1
                        if self.not_touching(row, start_col, "horizontal", word):
                            pos = ["horizontal", row, start_col]
                            return pos
                else:
                    find_word.clear()
        return False
