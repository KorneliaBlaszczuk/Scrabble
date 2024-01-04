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
            if hand_letter == "" and board.taking_out() != "":
                letter = board.taking_out()
                if board.letters_bag[letter][0] > 0:
                    self.rack()[e] = letter
                    letter_info = board.letters_bag[letter]
                    new_info = (letter_info[0] - 1, letter_info[1])
                    board.letters_bag[letter] = new_info
        return self.rack()

    def reinstate_rack(self, letter):
        """
        Restores the beginning of the rack status for the round.
        """
        for e, hand_letter in enumerate(self.rack()):
            if hand_letter == "":
                self.rack()[e] = letter
                break

    def is_rack_used(self):
        """
        Checks whether the stand is in use, i.e. whether any letters
        have already been removed during the current round
        """
        return "" in self.rack()

    def replace_rack(self, board):
        """
        Replaces the letters on the rack
        """
        if not self.is_rack_used():
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
        return all(place == "" for place in self.rack())

    def score_of_one_word(self, word, board):
        """
        Returns point score of given word
        """
        return sum(board.letters_bag[letter][1] for letter in word)

    def extra_points(self, other, board):
        """
        Checks for extra points for player.
        Used when the other player's rack isn't
        empty while player's is
        """
        extra_points = sum(
            board.letters_bag[letter][1] for letter in other.rack() if letter != ""
        )
        return extra_points

    def final_score(self, other, board):
        """
        Returns total score. When player's rack is empty it checks
        if the other's rack is not, and adds extra points.
        Ending the game, while having a letters on rack,
        results in minus points
        """
        total_score = sum(self.score_of_one_word(word, board) for word in self.words())

        if self.empty_rack():
            total_score += self.extra_points(other, board)
        else:
            total_score -= sum(
                board.letters_bag[letter][1] for letter in self.rack() if letter != ""
            )
        return total_score
