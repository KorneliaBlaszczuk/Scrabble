"""
Klasa Player
Zarządza graczem

:param name: Nazwa gracza
:typ name: str

:param words: Lista słów utworzonych przez gracza
:typ words: list

:param rack: Stojak na wylosowane literki gracza
:typ rack: list

"""


class Player:
    def __init__(self, name, words=None):
        self._name = str(name)
        self._words = words if words else []
        self._rack = ["", "", "", "", "", "", ""]

    def name(self):
        return self._name

    def words(self):
        return self._words

    def update_words(self, word):
        self.words().append(word)
        return self.words()

    def rack(self):
        return self._rack

    def updating_rack(self, board):
        """
        Funkcja aktualizująca stojak -
        w przypadku, gdy któraś z jego pozycji jest pusta
        dodaje do niej losową literę ze słownika LETTERS
        z uwzględnieniem ilości tabliczek danej litery
        w 'woreczku'.
        """
        for e, hand_letter in enumerate(self.rack()):
            if hand_letter == "":
                if board.taking_out() == "":
                    pass
                else:
                    letter = board.taking_out()
                    if board.letters_bag[letter][0] > 0:
                        self.rack()[e] = letter
                        letter_info = board.letters_bag[letter]
                        new_info = (letter_info[0] - 1, letter_info[1])
                        board.letters_bag[letter] = new_info
                    else:
                        continue
        return self.rack()

    def reinstate_rack(self, letter):
        """
        Funkcja przywraca początku dla danej rundy stan stojaka
        """
        for e, hand_letter in enumerate(self.rack()):
            if hand_letter == "":
                self.rack()[e] = letter
                break
            else:
                continue

    def is_rack_used(self):
        """
        Sprawdza czy stojak jest używany, czyli czy w trakcie
        aktualnej rundy nie zostały już wyjęte z niego żadne litery
        """
        for char in self.rack():
            if char == "":
                return False
            else:
                continue
        return True

    def replace_rack(self, board):
        """
        Wymienia literki na stojaku (wszystkie)
        """
        if self.is_rack_used() is False:
            return self.rack()
        else:
            for e, letter in enumerate(self.rack()):
                letter_info = board.letters_bag[letter]
                new_info = (letter_info[0] + 1, letter_info[1])
                board.letters_bag[letter] = new_info
                self.rack()[e] = ""
        self.updating_rack(board)
        return self.rack()

    def empty_rack(self):
        """
        Sprawdza czy stojak na litery jest pusty
        """
        for place in self.rack():
            if place != "":
                return False
        return True

    def score_of_one_word(self, word, board):
        """
        Zwraca wynik punktowy danego w argumencie słowa
        na podstawie punktacji danych liter
        """
        score = 0
        for letter in word:
            current_amount, points = board.letters_bag[letter]
            score += points
        return score

    def extra_points(self, other, board):
        """
        Sprawdza ilość dodatkowych punktów dla gracza
        z uwagi na obecność liter na stojaku przeciwnika
        """
        extra_points = 0
        for letter in other.rack():
            if letter != "":
                amount, points = board.letters_bag[letter]
                extra_points += points
            else:
                continue
        return extra_points

    def final_score(self, other, board):
        """
        Funkcja zwracająca ostateczny wynik gry,
        z uwzględnieniem 'punktów karnych' za zostawienie
        liter na stojaku gracza
        """
        total_score = 0
        for word in self.words():
            total_score += self.score_of_one_word(word, board)
        if self.empty_rack():
            total_score += self.extra_points(other, board)
        else:
            for letter in self.rack():
                if letter != "":
                    amount, points = board.letters_bag[letter]
                    total_score -= points
                else:
                    continue
        return total_score
