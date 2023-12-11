from letters_bag import letters


class Player:
    def __init__(self, name, words=None):
        self._name = name
        self._words = words if words else []
        self._handler = ["", "", "", "", "", "", ""]

    def name(self):
        return self._name

    def words(self):
        return self._words

    def update_words(self, word):
        self.words().append(word)
        return self.words()

    def handler(self):
        return self._handler

    def add_word(self, word):
        self.words().append(word)
        return self.words()

    def empty_handler(self, handler):
        for place in handler:
            if place != "":
                return False
        return True

    def score_of_one_word(self, word):
        """
        Funkcja zwracający wynik punktowy danego w argumencie słowa
        na podstawie słownika
        """
        score = 0
        for letter in word:
            current_amount, points = letters[letter]
            score += points
        return score

    def extra_points(self, other):
        extra_points = 0
        for letter in other.handler():
            if letter != "":
                amount, points = letters[letter]
                extra_points += points
            else:
                continue
        return extra_points

    def final_score(self, handler, other):
        """
        Funkcja zwracająca ostateczny wynik gry,
        z uwzględnieniem 'punktów karnych' za zostawienie
        liter w handlerze
        """
        total_score = 0
        for word in self.words():
            total_score += self.score_of_one_word(word)
        if self.empty_handler(handler):
            total_score += self.extra_points(other)
        else:
            for letter in handler:
                if letter != "":
                    amount, points = letters[letter]
                    total_score -= points
                else:
                    continue
        return total_score


class Bot(Player):
    def __init__(self, name, words=None):
        super().__init__(name, words)
