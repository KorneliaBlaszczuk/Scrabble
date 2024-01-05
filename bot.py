import random
import re
import time
from player import Player
from letters_bag import blank_list


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

    def blank_on_rack_handling(self, word, old=""):
        not_in_rack = {}
        word = word.upper()
        old = old.upper()
        letter_list = [letter for letter in word]
        blank_count = self.rack.count(" ")
        if all(
            (word.count(letter) <= self.rack.count(letter) + old.count(letter))
            for letter in set(word)
        ):
            return letter_list
        else:
            not_in_rack = {
                letter: word.count(letter) - self.rack.count(letter) - old.count(letter)
                for letter in set(word)
                if letter not in not_in_rack
                and word.count(letter) > self.rack.count(letter) + old.count(letter)
            }
            all_count = sum(not_in_rack.values())

            if all_count <= blank_count:
                for e, letter in enumerate(word):
                    if (
                        letter in not_in_rack
                        and word.count(letter) == not_in_rack[letter]
                    ):
                        letter_list[e] = " "
                    elif letter in not_in_rack and not_in_rack[letter] != 0:
                        letter_list[e] = " "
                        not_in_rack[letter] -= 1
                    else:
                        letter_list[e] = letter
                return letter_list
        return []

    def blank_find(self, word, valid_words):
        letter_list = list(word)
        blank_indices = [i for i, letter in enumerate(word) if letter == " "]

        if len(blank_indices) == 2:
            # If there are two blanks, iterate through all combinations
            for letter1 in blank_list:
                for letter2 in blank_list:
                    letter_list[blank_indices[0]] = letter1
                    letter_list[blank_indices[1]] = letter2
                    check_word = "".join(letter_list).lower()
                    find = self.find_matching_choice(check_word, valid_words)
                    if find:
                        return find, word, check_word
            # If no valid word is found, return False
            return ""
        else:
            # If there is one blank, iterate through all possible replacements
            for index in blank_indices:
                for let in blank_list:
                    letter_list[index] = let
                    check_word = "".join(letter_list).lower()
                    find = self.find_matching_choice(check_word, valid_words)
                    if find:
                        return find, word, check_word

            # If no valid word is found, return False
            return ""

    def valid_first_word(self, valid_words):
        """
        Finds a valid new word for bot. Manages blank tiles
        """

        for word in valid_words:
            choice = self.blank_on_rack_handling(word)
            if choice:
                return choice
        return []

    def valid_new_word(self, valid_words, board):
        """
        Finds a valid new word for bot. Manages blank tiles
        """
        all_words = board.word_list
        random.shuffle(all_words)
        letter_list = [letter for letter in all_words[0]]
        return self.add_to(valid_words, letter_list), all_words[0]

    def new_word(self, board, valid_words):
        """
        Returns information about new word
        """

        if board.word_list:
            new_word = self.valid_new_word(valid_words, board)[0]
            full_word = self.valid_new_word(valid_words, board)[1]
            return new_word, full_word

        word = "".join(self.valid_first_word(valid_words))

        if len(board.word_list) == 0:
            position = random.choice(["vertical", "horizontal"])
            start = self.first_word(word)
            # first word must be on coordinates (7, 7)
            if position == "vertical":
                return [start, 7, position, word.upper()]
            else:
                return [7, start, position, word.upper()]
        return []

    def first_word(self, word):
        """
        Function used in a sitaution when there is
        no words on the board yet, so the word must be
        on the (7,7) index
        """
        center_index = len(word) // 2
        start = 7 - center_index
        return start

    def add_to(self, valid_words, word_list):
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
            if " " in word:
                find = self.blank_find(word, valid_words)
                matching_choice = self.word_blank(find)
                if matching_choice == "":
                    word = ""
                return word, matching_choice
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
                    all_pos_letters = word_letters + self.rack
                    if all(
                        (choice_letters.count(letter))
                        <= (all_pos_letters.count(letter))
                        for letter in set(choice_letters)
                    ):
                        return choice
                    else:
                        choice = self.blank_on_rack_handling(element, word)
                        if choice:
                            return "".join(choice)

        return ""

    def added_letters(self, original_word, modified_word):
        """
        Returns a dictionary with added letters, their index
        and base word presence (1 if the letter is after base word
        and 0 if it is before)
        """
        base_word_pres = 0
        new_letters = {}
        original_word = original_word.upper()
        modified_word = modified_word.upper()
        position = re.search(original_word.upper(), modified_word.upper()).span()
        for e, letter in enumerate(modified_word):
            if e < position[0]:
                new_letters[e, base_word_pres] = letter
            elif e >= position[1]:
                base_word_pres = 1
                new_letters[e, base_word_pres] = letter
            else:
                continue
        return new_letters

    def make_prefix_and_suffix(self, added: dict):
        prefix = []
        suffix = []
        for ind, original_pres in added:
            if original_pres == 0:
                prefix.append(added[(ind, original_pres)])
            else:
                suffix.append(added[(ind, original_pres)])
        return prefix, suffix

    def valid_add_pos(self, board, row_start, col_start, position, added):
        """
        Checks if the given position is valid, so we can add letter
        to already existing word
        """
        valid_pos_pr = board.not_touching(
            row_start, col_start, position, "".join(added)
        )
        return sum(not term for term in valid_pos_pr) == 1

    def word_blank(self, blank_find):
        prefix = []
        suffix = []
        if blank_find == "":
            return ""
        new, with_blank, without_blank = blank_find
        letters = [letter for letter in new]
        added = self.added_letters(without_blank, new)

        prefix, suffix = self.make_prefix_and_suffix(added)

        for e, letter in enumerate(with_blank):
            if letter == " ":
                letters[e + len(prefix)] = " "
        return "".join(letters)

    def made_word_info(self, board, result, choice, added_let, position):
        new_word = {}

        old_word, upd_word = result[0], result[1]
        coord = board.exist(result[0])

        prefix, suffix = self.make_prefix_and_suffix(added_let)

        if position == "horizontal" and (
            coord[2] - len(prefix) >= 0
            and (coord[2] + len(result[0]) + len(suffix) - 1 <= 14)
        ):
            row_start = coord[1]
            col_start_pr = coord[2] - len(prefix)
            col_start_suf = coord[2] + len(result[0])

            if prefix and self.valid_add_pos(
                board, row_start, col_start_pr, position, prefix
            ):
                new_word["prefix"] = [
                    row_start,
                    col_start_pr,
                    position,
                    "".join(prefix).upper(),
                ]
            elif prefix and not self.valid_add_pos(
                board, row_start, col_start_pr, position, prefix
            ):
                new_word = {}
                return new_word
            elif not prefix:
                new_word["prefix"] = []

            if suffix and self.valid_add_pos(
                board, row_start, col_start_suf, position, suffix
            ):
                new_word["suffix"] = [
                    row_start,
                    col_start_suf,
                    position,
                    "".join(suffix).upper(),
                ]
            elif suffix and not self.valid_add_pos(
                board, row_start, col_start_suf, position, suffix
            ):
                new_word = {}
                return new_word
            elif not suffix:
                new_word["suffix"] = []

        elif position == "vertical" and (
            coord[1] - len(prefix) >= 0
            and coord[1] + len(result[0]) + len(suffix) - 1 <= 14
        ):
            row_start_pr = coord[1] - len(prefix)
            row_start_suf = coord[1] + len(result[0])
            col_start = coord[2]
            if prefix and self.valid_add_pos(
                board, row_start_pr, col_start, position, prefix
            ):
                new_word["prefix"] = [
                    row_start_pr,
                    col_start,
                    position,
                    "".join(prefix).upper(),
                ]
            elif prefix and not self.valid_add_pos(
                board, row_start_pr, col_start, position, prefix
            ):
                new_word = {}
                return new_word
            elif not prefix:
                new_word["prefix"] = []

            if suffix and self.valid_add_pos(
                board, row_start_suf, col_start, position, suffix
            ):
                new_word["suffix"] = [
                    row_start_suf,
                    col_start,
                    position,
                    "".join(suffix).upper(),
                ]
            elif suffix and not self.valid_add_pos(
                board, row_start_suf, col_start, position, suffix
            ):
                new_word = {}
                return new_word
            elif not suffix:
                new_word["suffix"] = []

        else:
            new_word = {}
            return new_word

        new_word["old_word"] = old_word.upper()
        new_word["new_word"] = upd_word.upper()
        new_word["mode"] = choice
        return new_word

    def added_info(self, board, valid_words, choice):
        new_word = {}

        result = (
            self.add_to(valid_words, board.word_list)
            if choice == "added"
            else self.new_word(board, valid_words)[0]
        )
        position = ""
        old_word, upd_word = result[0], result[1]
        old_word.upper()
        upd_word.upper()
        added = self.added_letters(old_word, upd_word)
        if added:
            if board.exist(result[0]) is not False and len(old_word) == 1:
                old_info = board.exist(self.new_word(board, valid_words)[1])
                position = "horizontal" if old_info[0] == "vertical" else "vertical"
            elif board.exist(result[0]) is not False and len(old_word) != 1:
                position = board.exist(result[0])[0]

            new_word = self.made_word_info(board, result, choice, added, position)

        return new_word

    def word_finding(self, board, valid_words):
        """
        Manages word finding for bot, including making
        a new one and adding letters to an exisitng one
        """
        new_word = {}

        choice = "new" if len(board.word_list) == 0 else random.choice(["new", "added"])

        if choice == "new" and len(board.word_list) == 0:
            result = self.new_word(board, valid_words)
            if all(info != "" for info in result):
                new_word["info"] = result
                new_word["mode"] = "first"

        else:
            new_word = self.added_info(board, valid_words, choice)
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

    def valid_new(self, board, choice):
        old_word = choice["old_word"]
        new_word = choice["new_word"]
        if len(old_word) != 1:
            return True

        if choice["prefix"]:
            row, col, position, added = choice["prefix"]
            if (
                position == "horizontal"
                and self.valid_add_pos(board, row, col, position, added)
                and board.board[row][col - 1] == ""
                and board.board[row][col + len(new_word)] == ""
            ):
                return True
            elif (
                position == "vertical"
                and self.valid_add_pos(board, row, col, position, added)
                and board.board[row - 1][col] == ""
                and board.board[row + len(new_word)][col] == ""
            ):
                return True
            else:
                return False
        if choice["suffix"]:
            row, col, position, added = choice["suffix"]
            if (
                position == "horizontal"
                and self.valid_add_pos(board, row, col, position, added)
                and board.board[row][col - len(old_word) - 1] == ""
                and board.board[row][col + len(added)] == ""
            ):
                return True
            elif (
                position == "vertical"
                and self.valid_add_pos(board, row, col, position, added)
                and board.board[row - len(old_word) - 1][col] == ""
                and board.board[row + len(added)][col] == ""
            ):
                return True
            else:
                return False

        return False

    def made_word(self, board, bot_choice, letters_bag):
        """
        Updates board, word_lists
        """
        current_word = {}
        if bot_choice["mode"] == "first":
            info = bot_choice["info"]
            current_word = self.made_current_word(info)
            board.update_word_list(bot_choice["info"][3])
            self.update_words(bot_choice["info"][3])
        else:
            added_prefix, added_suffix = bot_choice["prefix"], bot_choice["suffix"]
            if added_prefix:
                current_pref = self.made_current_word(added_prefix)
                current_word.update(current_pref)
            if added_suffix:
                current_suf = self.made_current_word(added_suffix)
                current_word.update(current_suf)

            if all(
                board.board[row][col] == "" for row, col in current_word
            ) and self.valid_new(board, bot_choice):
                if bot_choice["old_word"] in board.word_list:
                    board.remove_from_word_list(bot_choice["old_word"])

                board.update_word_list(bot_choice["new_word"])
                self.update_words(bot_choice["new_word"])
            else:
                self.replace_rack(letters_bag)
                return {}
        return current_word

    def attempts(self, board, valid_words, letters_bag):
        tries = 5
        bot_choice = {}
        time.sleep(1)
        while tries > 0:
            bot_choice = self.word_finding(board, valid_words)
            if bot_choice:
                board.current_word = self.made_word(board, bot_choice, letters_bag)
                return board.current_word
            else:
                tries -= 1
        self.replace_rack(letters_bag)
        return board.current_word

    def bot_turn(self, board, board_sprite, valid_words, letters_bag):
        """
        Manages whole bot turn
        """
        board.current_word = self.attempts(board, valid_words, letters_bag)
        for pos in board.current_word:
            board.draw_tiles(board_sprite, board.current_word[pos], pos)
            letter_hand = self.rack.index(board.current_word[pos])
            self.rack[letter_hand] = ""
        board.update_board()
        print(board.word_list)
        board.current_word_empty()
