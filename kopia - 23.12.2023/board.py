import pygame
from constants import (
    ROWS,
    COLS,
    DUN,
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

"""
Klasa Board
Zarządza planszą, w tym akcjami na niej,
jak i struktury z literami dostępnymi dla graczy

:param board: Plansza
:typ board: 2D list

:param word_list: Lista wszystkich słów na planszy
:typ word_list: list

:param letters_bag: Lista wszystich dostępnych płytek wraz z
                    punktacją
:typ letters_bag: dict

"""


class Board:
    def __init__(self):
        self.board = []
        self._word_list = []
        self.letters_bag = letters

    """win oznacza okno interaktywne"""

    @property
    def word_list(self):
        return self._word_list

    def create_board(self):
        """
        Tworzy pustą tablicę dwuwymiarową (jako argumenty w niej: "")
        """
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                self.board[row].append("")
        return self.board

    def update_board(self, current_word):
        """
        Dodaje aktualnie utworzone słowo do board
        """
        for pos in current_word:
            row, col = pos
            self.board[row][col] = current_word[pos]
        return self.board

    def remove_from_board(self, current_word):
        """
        Usuwa aktualnie utworzone słowo z board
        """
        for pos in current_word:
            row, col = pos
            self.board[row][col] = ""
        return self.board

    def update_word_list(self, word):
        """
        Aktualizuje listę słów (dodaje do niej)
        """
        self.word_list.append(word)
        return self.word_list

    def draw_rack(self, rack, rack_sprite):
        """
        Rysuje litery na stojaku
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
        Rysuje literę na planszy
        """
        row, col = pos
        letter_tile = Tile(current_letter, self.calc_coordinates(row, col))
        board_sprite.add(letter_tile)

    def taking_out(self):
        """
        Funkcja zwracająca losową wartość z listy -
        rozwiązanie to zostaje użyte przy konstrukcji stojak
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
        """
        Zajmuje się aspektem wizualnym plaszy, rysuje ją
        """
        win.fill(DUN)
        for row in range(ROWS):
            """
            Range poniżej powoduje, że co drugie pole jest innego koloru
            Podany sposób rozwiązania problemu spowoduje większą czytelność
            aplikacji dla użytkownika
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

    def draw_extra_squares(self, win):
        """
        Rysuje stojak, miejsce na litery
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
        """
        Przelicza numer kolumny i rzędu na odpowiednie koordynaty
        """
        y = row * SQUARE_SIZE
        x = col * SQUARE_SIZE
        return (x, y)

    def get_row_col_from_mouse(self, position):
        """
        Przelicza koordynaty na odpowiadające im numery kolumn i rzędów
        """
        x, y = position
        row = y // (SQUARE_SIZE)
        col = x // (SQUARE_SIZE)
        return (row, col)

    def valid_added_word(self, current_word):
        word_coord = self.addword_to(current_word)
        if all(self.board[row][col] != "" for row, col in word_coord):
            return True
        return False

    def addword_to(self, current_word):
        word_coord = []
        row = [item[0] for item in current_word.keys()]
        col = [item[1] for item in current_word.keys()]
        if all(x == col[0] for x in col):
            const = col[0]
            start = row[0]
            for coord in row:
                if coord == start:
                    start += 1
                else:
                    word_coord.append((start, const))
        if all(x == row[0] for x in row):
            const = row[0]
            start = col[0]
            for coord in col:
                if coord == start:
                    start += 1
                else:
                    word_coord.append((const, start))
                    start += 1
        return word_coord

    def not_valid(self, board_sprite, current_word, player):
        """
        Funkcja obsługująca sytuację, kiedy słowo położone przez gracza
        nie było poprawne lub jego pozycja była nieodpowiednia
        """
        for tile in board_sprite:
            for pos in current_word:
                letter_x, letter_y = self.calc_coordinates(pos[0], pos[1])
                if (tile.letter() == current_word[pos]) and (
                    tile.position() == (letter_x, letter_y)
                ):
                    board_sprite.remove(tile)
                    pygame.display.flip()
                player.reinstate_rack(current_word[pos])

    def alone_tile(self, pos):
        """
        Sprawdza czy położona przez gracza tabliczka z literą nie jest
        'samotna'
        W grze nie można położyć jako całe słowo tylko jednej tabliczki
        """
        let_row, let_col = pos
        if (
            (let_row + 1 < len(self.board) and self.board[let_row + 1][let_col] != "")
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
        Funkcja sprawdza, czy dane słowo, o podanych koordynatach początkowych
        nie spowoduje utworzenia dodatkowego słowa (czyli czy słowo
        jest samotne)
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
        Sprawdza czy na chcianej przez nas pozycji nie ma już innej
        litery
        """
        row = current_next_pos[1][0]
        col = current_next_pos[1][1]
        for letter in board_sprite:
            letter_row, letter_col = self.get_row_col_from_mouse(letter.position())
            if letter_row == row and letter_col == col:
                return True
            else:
                continue
        return False

    def check_row(self):
        """
        Przeszukuje rzędy tablicy, jeśli słowo dodajemy do listy
        """
        current_word = []
        check_word = []
        for row in self.board:
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

    def check_col(self):
        """
        Przeszukuje kolumny tablicy, jeśli słowo dodajemy do listy
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
                        else:
                            current_word = []
                        current_word = []
                    else:
                        continue
                else:
                    continue
        return check_word

    def word_in_board(self):
        """
        Zwraca listę poprawnych słów pod względem długości
        """
        words = [
            word
            for word in (self.check_row() + self.check_col())
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
        """
        Sprawdza poprawność danego słowa (czy znajduje się w liście
        akceptowalnych)
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
        for word in self.word_in_board():
            if self.word_authentication(word, words):
                continue
            else:
                return False
        return True

    def word_list_adding(self, player):
        """
        Dodaje słowo do listy gracza, jeśli jest poprawne i on
        je ułożył
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
        Obsługuje sprawdzanie poprawności słowa i akcje z nim związane
        """
        if self.word_checking(words):
            self.word_list_adding(player)
        else:
            self.not_valid(board_sprite, current_word, player)
            self.remove_from_board(current_word)

    def exist(self, word):
        """
        Sprawdza czy słowo istnieje
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
