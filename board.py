import pygame
from constants import (
    ROWS,
    COLS,
    SQUARE_SIZE,
)
from letters_bag import blank_list


class Board:
    """
    Class Board

    Manages game board, including: words made on board, current word and
    2-dimensional board list.

    :param board: Game Board
    :type board: 2D list

    :param word_list: List of all the words on the board
    :type word_list: list

    :param current_word: dict containing current word made by player
    :type current_word: dict

    """

    def __init__(self):
        self._board = []
        self._word_list = []
        self._current_word = {}

    @property
    def word_list(self):
        return self._word_list

    @property
    def board(self):
        return self._board

    @property
    def current_word(self):
        return self._current_word

    """Word_list functions"""

    def empty_word_list(self):
        self.word_list.clear()
        return self.word_list

    def remove_from_word_list(self, word):
        self.word_list.remove(word)
        return self.word_list

    def update_word_list(self, word):
        """
        Appends a word list
        """
        self.word_list.append(word)
        return self.word_list

    """Current_word functions"""

    def current_word_update(self, coord, letter):
        """
        Updates current word
        """
        self.current_word[coord] = letter
        return self.current_word

    def current_word_empty(self):
        """
        Empties current word
        """
        self.current_word.clear()
        return self.current_word

    """Board list functions"""

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

    def update_board(self):
        """
        Adds current word (letters) to board
        """
        for pos in self.current_word:
            row, col = pos
            self.board[row][col] = self.current_word[pos]
        return self.board

    def remove_from_board(self):
        """
        Removes current word from board
        """
        for pos in self.current_word:
            row, col = pos
            self.board[row][col] = ""
        return self.board

    """Handling coordinates on board"""

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

    def space_count(self, word_coord):
        """
        Counts the number of empty spaces
        between letters of current word
        """
        count = 0
        in_group = False

        for i in range(len(word_coord) - 1):
            if word_coord[i] + 1 == word_coord[i + 1]:
                in_group = True
            elif in_group:
                count += 1
                in_group = False
            else:
                count += 1
                in_group = False

        return count

    def addword(self):
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
        row = [item[0] for item in self.current_word.keys()]
        col = [item[1] for item in self.current_word.keys()]
        if all(x == col[0] for x in col):
            const, count = col[0], row[0]
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
            const, count = row[0], col[0]
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
        return word_coord

    """Manages placement validation process"""

    def valid_position(self):
        """
        Function that sorts current word
        """
        row_key, col_key = zip(*self.current_word.keys())

        if all(x == row_key[0] for x in row_key):
            sorted_word = dict(
                sorted(
                    self.current_word.items(),
                    key=lambda item: item[0][1],
                )
            )
            self._current_word = sorted_word
        elif all(y == col_key[0] for y in col_key):
            sorted_word = dict(
                sorted(
                    self.current_word.items(),
                    key=lambda item: item[0][0],
                )
            )
            self._current_word = sorted_word
        else:
            return False

        return self.current_word

    def valid_added_word(self):
        """
        Checks if the placement of added word
        is correct
        """
        row_key = [item[0] for item in self.current_word.keys()]
        col_key = [item[1] for item in self.current_word.keys()]

        space_coord = self.addword()
        position = self.word_info_position()
        coordinates = row_key if position == "vertical" else col_key
        space_count = self.space_count(coordinates)
        if space_count == 1:
            if position == "vertical" and all(
                self.board[row][space_coord[1]] != ""
                for row in range(space_coord[0][0], space_coord[0][1])
            ):
                return True
            elif position == "horizontal" and all(
                self.board[space_coord[0]][col] != ""
                for col in range(space_coord[1][0], space_coord[1][1])
            ):
                return True
        elif space_count == 0 and not all(
            self.not_touching(
                row_key[0],
                col_key[0],
                position,
                "".join(
                    self.current_word.values(),
                ),
            )
        ):
            return True
        else:
            return False

    def not_valid_action(self, board_sprite, player):
        """
        Action called in a situation when the wrong move was made by player
        """
        for tile in board_sprite:
            for pos in self.current_word:
                letter_x, letter_y = self.row_col_to_coord(pos[0], pos[1])
                if (tile.letter() == self.current_word[pos]) and (
                    tile.position() == (letter_x, letter_y)
                ):
                    board_sprite.remove(tile)
                    pygame.display.flip()
                player.reinstate_rack(self.current_word[pos])
        self.current_word_empty()

    def not_touching(
        self,
        row_start,
        col_start,
        position="horizontal",
        word=" ",
    ) -> list:
        """
        Checks if the word is touching another by its border.
        """
        valid_condition = []
        if position == "horizontal":
            if row_start != 0:
                if all(
                    0 <= (col_start + k) < 15
                    and self.board[row_start - 1][col_start + k] == ""
                    for k in range(len(word))
                ):
                    valid_condition.append(True)
                else:
                    valid_condition.append(False)
            if row_start != 14:
                if all(
                    0 <= (col_start + k) < 15
                    and self.board[row_start + 1][col_start + k] == ""
                    for k in range(len(word))
                ):
                    valid_condition.append(True)
                else:
                    valid_condition.append(False)
            if col_start != 0:
                if self.board[row_start][col_start - 1] == "":
                    valid_condition.append(True)
                else:
                    valid_condition.append(False)
            if col_start + len(word) < 15:
                if self.board[row_start][col_start + len(word)] == "":
                    valid_condition.append(True)
                else:
                    valid_condition.append(False)
        else:
            if col_start != 0:
                if all(
                    0 <= (row_start + k) < 15
                    and self.board[row_start + k][col_start - 1] == ""
                    for k in range(len(word))
                ):
                    valid_condition.append(True)
                else:
                    valid_condition.append(False)
            if col_start != 14:
                if all(
                    0 <= (row_start + k) < 15
                    and self.board[row_start + k][col_start + 1] == ""
                    for k in range(len(word))
                ):
                    valid_condition.append(True)
                else:
                    valid_condition.append(False)
            if row_start != 0:
                if self.board[row_start - 1][col_start] == "":
                    valid_condition.append(True)
                else:
                    valid_condition.append(False)
            if row_start + len(word) < 15:
                if self.board[row_start + len(word)][col_start] == "":
                    valid_condition.append(True)
                else:
                    valid_condition.append(False)
        return valid_condition

    def valid_placement(self, board_sprite, player):
        """
        Manages validation of the placement. If it's correct nothing happens
        in this function. The game goes on. In case of the opposite, we
        execute not_valid_action.
        """
        if len(self.word_list) == 0 and not any(
            key == (7, 7) for key in self.current_word.keys()
        ):
            self.not_valid_action(board_sprite, player)
        elif (
            len(self.word_list) != 0
            and len(self.current_word.values()) == 1
            and all(
                self.not_touching(
                    list(self.current_word.keys())[0][0],
                    list(self.current_word.keys())[0][1],
                )
            )
        ):
            self.not_valid_action(board_sprite, player)
        elif not self.valid_position():
            self.not_valid_action(
                board_sprite,
                player,
            )
        else:
            if not self.current_word and not self.valid_added_word():
                self.not_valid_action(
                    board_sprite,
                    player,
                )

    def validation(self, board_sprite, valid, player):
        """
        Manages all the validation proces of word made by player
        """
        if self.word_checking(valid):
            self.word_lists_adding(player)
        else:
            self.not_valid_action(board_sprite, player)
            self.remove_from_board()

    def check_row(self):
        """
        Searches rows for words
        """
        current_word = []
        words = []
        for row in self.board:
            for e, element in enumerate(row):
                if element != "":
                    current_word.append(element)
                    if ((e + 1) != len(row) and (row[e + 1] == "")) or (
                        (e + 1) == len(row)
                    ):
                        words.append("".join(current_word))
                        current_word = []
        return words

    def check_col(self):
        """
        Searches a columns for words
        """
        current_word = []
        words = []

        for col in range(15):
            for row in range(15):
                element = self.board[row][col]
                if element != "":
                    current_word.append(element)
                    if (row + 1) != 15 and (self.board[row + 1][col] == ""):
                        words.append("".join(current_word))
                        current_word = []
                    elif (row + 1) == 15 and len(current_word) > 1:
                        words.append("".join(current_word))
                        current_word = []
                    elif (row + 1) == 15 and len(current_word) <= 1:
                        current_word = []
        return words

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

    def letter_in_board(self):
        """Returns list of letters on the board"""
        all_found = self.check_row() + self.check_col()
        letters = [word for word in (all_found) if len(word) == 1]
        return letters

    """Word authentication functions"""

    def word_authentication(self, word, valid):
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
                    if check_word in valid:
                        return True
            return False
        else:
            for e, letter in enumerate(letter_list):
                if letter == " ":
                    for let in blank_list:
                        letter_list[e] = let
                        check_word = "".join(letter_list).lower()
                        if check_word not in valid and let != blank_list[-1]:
                            continue
                        elif check_word not in valid and let == blank_list[-1]:
                            return False
                        return True
                else:
                    continue
            check_word = word.lower()
            if check_word in valid:
                return True
            else:
                return False

    def word_checking(self, valid):
        """
        Checks if all the words on the board are valid
        """
        self.empty_word_list()
        for word in self.word_in_board():
            if self.word_authentication(word, valid):
                self.update_word_list(word)
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
            if count == 1 and word in self.word_list:
                continue
            elif count == 1 and word not in self.word_list:
                self.update_word_list(word)
                player.update_words(word)
            else:
                while count != word_amount:
                    self.update_word_list(word)
                    player.update_words(word)
                    word_amount += 1
        return self.word_list

    """Functions that gives us info about words"""

    def word_info_position(self):
        row_key = [item[0] for item in self.current_word.keys()]
        position = "horizontal" if all(x == row_key[0] for x in row_key) else "vertical"
        return position

    def exist(self, word):
        """
        Checks if the word exists and on which coordinates
        """
        info = []

        find_word = []
        word = word.upper()
        for col in range(15):
            for row in range(15):
                element = self.board[row][col]
                if element != "" and element in word:
                    find_word.append(element)
                    start_row = row - len(find_word) + 1
                    if "".join(find_word) == word and self.not_touching(
                        start_row, col, "vertical", word
                    ):
                        info = ["vertical", start_row, col]
                        return info
                else:
                    find_word.clear()

        for row in range(15):
            for col in range(15):
                element = self.board[row][col]
                if element != "" and element in word:
                    find_word.append(element)
                    start_col = col - len(find_word) + 1
                    if "".join(find_word) == word and self.not_touching(
                        row, start_col, "horizontal", word
                    ):
                        info = ["horizontal", row, start_col]
                        return info
                else:
                    find_word.clear()
        return False
