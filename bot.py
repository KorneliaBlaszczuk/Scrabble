import random
import re
from player import Player


class Bot(Player):
    """
    Class Bot
    Manages bot actions. Inherits from Player Class.

    param name: "Bot"
    type name: str

    param word: list of made words
    type word: list
    """

    def __init__(self, name="Bot", words=None, rack=None):
        super().__init__(name, words, rack)

    def valid_new_word(self, valid_words):
        """
        Finds a valid new word for bot. Manages blank tiles
        """
        blank_count = self.rack().count(" ")

        for word in valid_words:
            not_in_rack = {}
            word = word.upper()
            letter_list = [letter for letter in word]

            if all(
                (word.count(letter) <= self.rack().count(letter))
                for letter in set(word)
            ):
                return letter_list
            else:
                not_in_rack = {
                    letter: word.count(letter) - self.rack().count(letter)
                    for letter in set(word)
                    if letter not in not_in_rack
                    and word.count(letter) > self.rack().count(letter)
                }
                all_count = sum(not_in_rack.values())

                if all_count <= blank_count:
                    for e, letter in enumerate(word):
                        if letter in not_in_rack:
                            if word.count(letter) == not_in_rack[letter]:
                                letter_list[e] = " "
                            elif not_in_rack[letter] != 0:
                                letter_list[e] = " "
                                not_in_rack[letter] -= 1
                        else:
                            letter_list[e] = letter
                    return letter_list
        return []

    def new_word(self, board, valid_words):
        """
        Returns information about new word
        """
        new_word = self.valid_new_word(valid_words)
        word = "".join(new_word)
        position = random.choice(["vertical", "horizontal"])
        start_pos = list(range(15))
        other_pos = list(range(15))
        random.shuffle(start_pos)
        random.shuffle(other_pos)
        """because we shuffle coordinates through which we iterate,
        it gives a feeling of randomness"""
        if len(board.word_list) == 0:
            start = self.first_new_word(word)
            # first word must be on coordinates (7, 7)
            if position == "vertical":
                return [start, 7, position, word.upper()]
            else:
                return [7, start, position, word.upper()]

        return self.find_valid_position(
            word,
            board,
            start_pos,
            other_pos,
            position,
        )

    def find_valid_position(self, word, board, start_pos, other_pos, position):
        """
        Finds valid position to put a new word
        """
        for start in start_pos:
            for col_or_row in other_pos:
                if position == "vertical":
                    if self.is_valid_position(
                        board,
                        start,
                        col_or_row,
                        position,
                        word,
                    ):
                        return [start, col_or_row, position, word.upper()]
                else:
                    if self.is_valid_position(
                        board,
                        start,
                        col_or_row,
                        position,
                        word,
                    ):
                        return [col_or_row, start, position, word.upper()]
        return ["", "", "", ""]

    def is_valid_position(self, board, start, col_or_row, position, word):
        """
        Checks if the choosen position is valid
        """
        if start + len(word) < 15:
            if position == "vertical":
                if all(
                    board.board[start + k][col_or_row] == "" for k in range(len(word))
                ) and all(board.not_touching(start, col_or_row, position, word)):
                    return True
            else:
                if all(
                    board.board[col_or_row][start + k] == "" for k in range(len(word))
                ) and all(board.not_touching(col_or_row, start, position, word)):
                    return True
        return False

    def first_new_word(self, word):
        """
        Function used in a sitaution when there is
        no words on the board yet, so the word must be
        on the (7,7) index
        """
        center_index = len(word) // 2
        start = 7 - center_index
        return start

    def add_to_word(self, valid_words, word_list):
        """
        Manages adding letters to already existing ones on board
        """
        """
        Obsługa blank
        """
        if not word_list:
            return "", ""

        random.shuffle(word_list)
        for word in word_list:
            word = word.lower()
            matching_choice = self.find_matching_choice(word, valid_words)
            if matching_choice:
                return word, matching_choice

        return "", ""

    def find_matching_choice(self, word, valid_words):
        """
        Finds a matching choice in word_list for the given word
        """
        for element in valid_words:
            if re.search(word, element):
                choice = element
                if choice and choice != word:
                    choice_letters = [letter.upper() for letter in choice]
                    word_letters = [letter.upper() for letter in word]
                    all_pos_letters = word_letters + self.rack()
                    if all(
                        (choice_letters.count(letter))
                        <= (all_pos_letters.count(letter))
                        for letter in set(choice_letters)
                    ):
                        return choice
        return ""

    def added_letters(self, original_word, modified_word):
        """
        Returns a dictionary with added letters, their index
        and base word presence (1 if the letter is after base word
        and 0 if it is before)
        """
        base_word_pres = 0
        new_letters = {}
        position = re.search(original_word, modified_word).span()
        for e, letter in enumerate(modified_word):
            if e < position[0]:
                new_letters[e, base_word_pres] = letter
            elif e >= position[1]:
                base_word_pres = 1
                new_letters[e, base_word_pres] = letter
            else:
                continue
        return new_letters

    def valid_add_pos(self, board, row_start, col_start, position, added):
        """
        Checks if the given position is valid, so we can add letter
        to already existing word
        """
        valid_pos_pr = board.not_touching(
            row_start, col_start, position, "".join(added)
        )
        false_count = 0
        for term in valid_pos_pr:
            if term is False:
                false_count += 1
        if false_count == 1:
            return True
        return False

    def word_finding(self, board, valid_words):
        """
        Manages word finding for bot, including making
        a new one and adding letters to an exisitng one
        """
        new_word = {}
        prefix = []
        sufix = []
        old_word = ""
        upd_word = ""
        if len(board.word_list) == 0:
            choice = "new"
        else:
            choice = random.choice(["new", "added"])
        if choice == "new":
            result = self.new_word(board, valid_words)
            if all(info != "" for info in result):
                new_word["info"] = result
                new_word["mode"] = choice
        else:
            if len(board.word_list) != 0:
                result = self.add_to_word(valid_words, board.word_list)
                old_word, upd_word = result[0], result[1]
                if old_word != "" and upd_word != "":
                    added_let = self.added_letters(result[0], result[1])
                    if added_let:
                        for ind, original_pres in added_let:
                            if original_pres == 0:
                                prefix.append(added_let[(ind, original_pres)])
                            else:
                                sufix.append(added_let[(ind, original_pres)])
                        if board.exist(result[0]) is not False:
                            coord = board.exist(result[0])
                            if coord[0] == "horizontal":
                                if coord[2] - len(prefix) >= 0 and (
                                    coord[2] + len(result[0]) + len(sufix) - 1 <= 14
                                ):
                                    row_start = coord[1]
                                    col_start_pr = coord[2] - len(prefix)
                                    col_start_suf = coord[2] + len(result[0])
                                    if prefix:
                                        if self.valid_add_pos(
                                            board,
                                            row_start,
                                            col_start_pr,
                                            "horizontal",
                                            prefix,
                                        ):
                                            new_word["prefix"] = [
                                                row_start,
                                                col_start_pr,
                                                "horizontal",
                                                "".join(prefix).upper(),
                                            ]
                                        else:
                                            new_word = {}
                                            return new_word
                                    else:
                                        new_word["prefix"] = []
                                    if sufix:
                                        if self.valid_add_pos(
                                            board,
                                            row_start,
                                            col_start_suf,
                                            "horizontal",
                                            sufix,
                                        ):
                                            new_word["sufix"] = [
                                                row_start,
                                                col_start_suf,
                                                "horizontal",
                                                "".join(sufix).upper(),
                                            ]
                                        else:
                                            new_word = {}
                                            return new_word
                                    else:
                                        new_word["sufix"] = []
                                else:
                                    new_word = {}
                                    return new_word
                            else:
                                if (
                                    coord[1] - len(prefix) >= 0
                                    and coord[1] + len(result[0]) + len(sufix) - 1 <= 14
                                ):
                                    row_start_pr = coord[1] - len(prefix)
                                    row_start_suf = coord[1] + len(result[0])
                                    col_start = coord[2]
                                    if prefix:
                                        if self.valid_add_pos(
                                            board,
                                            row_start_pr,
                                            col_start,
                                            "vertical",
                                            prefix,
                                        ):
                                            new_word["prefix"] = [
                                                row_start_pr,
                                                col_start,
                                                "vertical",
                                                "".join(prefix).upper(),
                                            ]
                                        else:
                                            new_word = {}
                                            return new_word
                                    else:
                                        new_word["prefix"] = []
                                    if sufix:
                                        if self.valid_add_pos(
                                            board,
                                            row_start_suf,
                                            col_start,
                                            "vertical",
                                            sufix,
                                        ):
                                            new_word["sufix"] = [
                                                row_start_suf,
                                                col_start,
                                                "vertical",
                                                "".join(sufix).upper(),
                                            ]
                                        else:
                                            new_word = {}
                                            return new_word
                                    else:
                                        new_word["sufix"] = []
                                else:
                                    new_word = {}
                                    return new_word
                            new_word["old_word"] = old_word.upper()
                            new_word["new_word"] = upd_word.upper()
                            new_word["mode"] = choice
                    else:
                        new_word = {}
                        return new_word
        return new_word

    def made_current_word(self, info):
        """
        Returns current_word dictionary, used in game() function
        in game.py
        """
        current_word = {}
        if info[2] == "vertical":
            cur_row = int(info[0])
            for letter in info[3]:
                current_word[(cur_row, info[1])] = letter
                cur_row += 1
        else:
            cur_col = int(info[1])
            for letter in info[3]:
                current_word[(info[0], cur_col)] = letter
                cur_col += 1
        return current_word

    def attempts(self, board, valid_words):
        tries = 4
        bot_choice = {}
        while tries > 0:
            bot_choice = self.word_finding(board, valid_words)
            if not bot_choice:
                tries -= 1
            else:
                return bot_choice
        return bot_choice

    def made_word(self, board, valid_words):
        """
        Updates board, word_lists
        """
        current_word = {}
        bot_choice = self.attempts(board, valid_words)
        print(bot_choice)
        if bot_choice:
            if bot_choice["mode"] == "new":
                info = bot_choice["info"]
                current_word = self.made_current_word(info)
                board.update_word_list(bot_choice["info"][3])
                self.update_words(bot_choice["info"][3])
            else:
                added_prefix = bot_choice["prefix"]
                if added_prefix:
                    current_pref = self.made_current_word(added_prefix)
                    current_word.update(current_pref)
                added_sufix = bot_choice["sufix"]
                if added_sufix:
                    current_suf = self.made_current_word(added_sufix)
                    current_word.update(current_suf)

                board.word_list.remove(bot_choice["old_word"])
                board.update_word_list(bot_choice["new_word"])
                self.update_words(bot_choice["new_word"])
        else:
            self.replace_rack(board)
        return current_word

    def bot_turn(self, board, board_sprite, valid_words):
        """
        Manages whole bot turn
        """
        current_word = self.made_word(board, valid_words)
        for pos in current_word:
            board.draw_tiles(board_sprite, current_word[pos], pos)
            letter_hand = self.rack().index(current_word[pos])
            self.rack()[letter_hand] = ""
        board.update_board(current_word)
