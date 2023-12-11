import pygame
from constants import (
    ROWS,
    COLS,
    DUN,
    CINEREOUS,
    BEAVER,
    SQUARE_SIZE,
    EXTRA_SQUARES,
    extra_space_x,
)
import random
from letters_bag import letters, blank_list
from tiles import Tile


class Board:
    def __init__(self):
        self.board = []
        self.word_list = []
        self.letters_bag = letters
        self.selected_piece = None

    """win oznacza okno interaktywne"""

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                self.board[row].append("")
        return self.board

    def update_board(self, current_word):
        for pos in current_word:
            row, col = pos
            self.board[row][col] = current_word[pos]
        return self.board

    def remove_from_board(self, current_word):
        for pos in current_word:
            row, col = pos
            self.board[row][col] = ""
        return self.board

    def update_word_list(self, word):
        self.word_list.append(word)
        return self.word_list

    def updating_handler(self, handler):
        """
        Funkcja aktualizująca handler -
        w przypadku, gdy któraś z jego pozycji jest pusta
        dodaje do niej losową literę ze słownika LETTERS
        z uwzględnieniem ilości tabliczek danej litery
        w 'woreczku'.
        """
        for e, hand_letter in enumerate(handler):
            if hand_letter == "":
                if self.taking_out() == "":
                    pass
                else:
                    letter = self.taking_out()
                    if self.letters_bag[letter][0] > 0:
                        handler[e] = letter
                        letter_info = self.letters_bag[letter]
                        new_info = (letter_info[0] - 1, letter_info[1])
                        self.letters_bag[letter] = new_info
                    else:
                        continue
        return handler

    def reinstate_handler(self, handler, letter):
        for e, hand_letter in enumerate(handler):
            if hand_letter == "":
                handler[e] = letter
                break
            else:
                continue

    def is_handler_used(self, handler):
        for char in handler:
            if char == "":
                return False
            else:
                continue
        return True

    def replace_handler(self, handler):
        if self.is_handler_used(handler) is False:
            return handler
        else:
            for e, letter in enumerate(handler):
                letter_info = self.letters_bag[letter]
                new_info = (letter_info[0] + 1, letter_info[1])
                self.letters_bag[letter] = new_info
                handler[e] = ""
        self.updating_handler(handler)
        return handler

    def draw_handler(self, handler, handler_sprite):
        x = extra_space_x
        y = (COLS + 1) * SQUARE_SIZE
        for current_letters in handler:
            if current_letters == "":
                x += SQUARE_SIZE
            else:
                letter_title = Tile(current_letters, (x, y))
                handler_sprite.add(letter_title)
                x += SQUARE_SIZE

    def taking_out(self):
        """
        Funkcja zwracająca losową wartość z listy -
        rozwiązanie to zostaje użyte przy konstrukcji handlera.
        """
        all_letters = []
        for letter in self.letters_bag:
            if self.letters_bag[letter][0] > 0:
                all_letters.append(letter)
        if len(all_letters) != 0:
            choosen_letter = random.choice(all_letters)
        else:
            choosen_letter = ""
        return choosen_letter

    def draw_squares(self, win):
        win.fill(DUN)
        for row in range(ROWS):
            """
            Range poniżej powoduje, że co drugie pole jest innego koloru
            Podany sposób rozwiązania problemu spowoduje większą czytelność
            aplikacji dla użytkownika
            """
            for col in range(COLS):
                color = CINEREOUS if (row + col) % 2 == 0 else BEAVER
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

    def draw_extra_squares(self, win):
        """
        Rysuje handler
        """
        for i in range(EXTRA_SQUARES):
            x = SQUARE_SIZE * 4 + i * SQUARE_SIZE
            y = (COLS + 1) * SQUARE_SIZE
            if i % 2 == 0:
                color = CINEREOUS
            else:
                color = BEAVER
            pygame.draw.rect(win, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

    def calc_coordinates(self, row, col):
        y = row * SQUARE_SIZE
        x = col * SQUARE_SIZE
        return (x, y)

    def get_row_col_from_mouse(self, position):
        x, y = position
        row = y // (SQUARE_SIZE)
        col = x // (SQUARE_SIZE)
        return (row, col)

    def not_valid(self, board_sprite, current_word, player):
        for tile in board_sprite:
            for pos in current_word:
                letter_x, letter_y = self.calc_coordinates(pos[0], pos[1])
                if (tile.letter() == current_word[pos]) and (
                    tile.position() == (letter_x, letter_y)
                ):
                    board_sprite.remove(tile)
                    pygame.display.flip()
                self.reinstate_handler(player.handler(), current_word[pos])

    def alone_tile(self, board, pos):
        let_row, let_col = pos
        if (
            (let_row + 1 < len(board) and board[let_row + 1][let_col] != "")
            or (let_row - 1 >= 0 and board[let_row - 1][let_col] != "")
            or (let_col - 1 >= 0 and board[let_row][let_col - 1] != "")
            or (let_col + 1 < len(board[let_row]) and board[let_row][let_col + 1] != "")
        ):
            return False
        else:
            return True

    def colid(self, board_sprite, current_next_pos):
        row = current_next_pos[1][0]
        col = current_next_pos[1][1]
        for letter in board_sprite:
            letter_row, letter_col = self.get_row_col_from_mouse(letter.position())
            if letter_row == row and letter_col == col:
                return True
            else:
                continue
        return False

    def check_row(self, board):
        current_word = []
        check_word = []
        for row in board:
            for e, element in enumerate(row):
                if element != "":
                    current_word.append(element)
                    if (e + 1) != len(row) and (row[e + 1] == ""):
                        check_word.append("".join(current_word))
                        current_word = []
                    elif (e + 1) == len(row):
                        check_word.append("".join(current_word))
                        current_word = []
                    else:
                        continue
                else:
                    continue
        return check_word

    def check_col(self, board):
        current_word = []
        check_word = []

        for col in range(15):
            for row in range(15):
                element = board[row][col]
                if element != "":
                    current_word.append(element)
                    if (row + 1) != 15 and (board[row + 1][col] == ""):
                        check_word.append("".join(current_word))
                        current_word = []
                    elif (row + 1) == 15:
                        if len(current_word) > 1:
                            check_word.append("".join(current_word))
                        else:
                            current_word = []
                        current_word = []
                    else:
                        continue
                else:
                    continue
        return check_word

    def word_in_board(self, board):
        words = [
            word
            for word in (self.check_row(board) + self.check_col(board))
            if len(word) > 1 and len(word) < 6
        ]
        return words

    def char_in_word(self, text):
        char = []
        for letter in text:
            char.append(letter)
        return char

    def check_word_in_file(self, word, words):
        """
        Funkcja sprawdzająca wystąpienie słowa w danym dokumencie
        """
        return word in words

    def word_authentication(self, word, words):
        letter_list = list(word)
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

    def word_checking(self, board, words):
        for word in self.word_in_board(board):
            if self.word_authentication(word, words):
                continue
            else:
                return False
        return True

    def word_list_adding(self, board, player):
        for word in self.word_in_board(board):
            count = self.word_in_board(board).count(word)
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
