class Player:
    """
    Class Player
    Manage player, including their word list and rack.

    :param name: player's name
    :type name: str

    :param words: player's list of words
    :type words: list

    :param rack: player's rack for avaible letters
    :type rack: list

    """

    def __init__(self, name, words=None, rack=None):
        self._name = str(name)
        self._words = words if words else []
        self._rack = rack if rack else ["", "", "", "", "", "", ""]

    def name(self):
        return self._name

    def words(self):
        return self._words

    def rack(self):
        return self._rack

    def update_words(self, word):
        """
        Updates player's list of words
        """
        self.words().append(word)
        return self.words()

    def updating_rack(self, board):
        """
        A function that updates the rack -
        in case one of its positions is empty
        adds to it a random letter from the LETTERS dictionary
        taking into account the number of plates of a given letter
        in the 'bag'.
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
        Restores the beginning of the rack status for the round.
        """
        for e, hand_letter in enumerate(self.rack()):
            if hand_letter == "":
                self.rack()[e] = letter
                break
            else:
                continue

    def is_rack_used(self):
        """
        Checks whether the stand is in use, i.e. whether any letters
        have already been removed during the current round
        """
        for char in self.rack():
            if char == "":
                return True
            else:
                continue
        return False

    def replace_rack(self, board):
        """
        Replaces the letters on the rack
        """
        if self.is_rack_used():
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
        Checks if the rack is empty
        """
        for place in self.rack():
            if place != "":
                return False
        return True

    def score_of_one_word(self, word, board):
        """
        Returns point score of given word
        """
        score = 0
        for letter in word:
            current_amount, points = board.letters_bag[letter]
            score += points
        return score

    def extra_points(self, other, board):
        """
        Checks for extra points for player.
        Used when the other player's rack isn't
        empty while player's is
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
        Returns total score. When player's rack is empty it checks
        if the other's rack is not, and adds extra points.
        Ending the game, while having a letters on rack,
        results in minus points
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
