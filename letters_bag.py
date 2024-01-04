import random

"""
All avabile letters with its start amount and values (points)
"""

letters = {
    "A": (9, 1),
    "Ą": (1, 5),
    "B": (2, 3),
    "C": (3, 2),
    "Ć": (1, 6),
    "D": (3, 2),
    "E": (7, 1),
    "Ę": (1, 5),
    "F": (1, 5),
    "G": (2, 3),
    "H": (2, 3),
    "I": (8, 1),
    "J": (2, 3),
    "K": (3, 2),
    "L": (3, 2),
    "Ł": (2, 3),
    "M": (3, 2),
    "N": (5, 1),
    "Ń": (1, 7),
    "O": (6, 1),
    "Ó": (1, 5),
    "P": (3, 2),
    "R": (4, 1),
    "S": (4, 1),
    "Ś": (1, 5),
    "T": (3, 2),
    "U": (2, 3),
    "W": (4, 1),
    "Y": (4, 2),
    "Z": (5, 1),
    "Ź": (1, 9),
    "Ż": (1, 5),
    " ": (2, 0),
}

"""
Letters that blank can be
"""

blank_list = [
    "a",
    "ą",
    "b",
    "c",
    "ć",
    "d",
    "e",
    "ę",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "ł",
    "m",
    "n",
    "ń",
    "o",
    "ó",
    "p",
    "r",
    "s",
    "ś",
    "t",
    "u",
    "w",
    "y",
    "z",
    "ź",
    "ż",
]


class LettersBag:
    def __init__(self):
        self._letters_bag = letters.copy()

    @property
    def letters_bag(self):
        return self._letters_bag

    @property
    def all_letters(self):
        return self.letters_bag.keys()

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

    def put_back(self, letter):
        letter_info = self.letters_bag[letter]
        new_info = (letter_info[0] - 1, letter_info[1])
        self.letters_bag[letter] = new_info
        return self.letters_bag
