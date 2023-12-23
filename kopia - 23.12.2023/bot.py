import random
import re
from player import Player


class Bot(Player):
    def __init__(self, name="Bot", words=None):
        super().__init__(name, words)

    def new_word(self, board, word_list):
        for word in word_list:
            if all(
                word.upper().count(letter) <= self.rack().count(letter)
                for letter in set(word.upper())
            ):
                position = random.choice(["vertical", "horizontal"])
                start_pos = list(range(15))
                other_pos = list(range(15))
                random.shuffle(start_pos)
                random.shuffle(other_pos)
                if position == "vertical":
                    for start in start_pos:
                        for col in other_pos:
                            if len(board.word_list) == 0:
                                start = self.first_new_word(word)
                                return [start, 7, position, word.upper()]
                            if start + len(word) < 15:
                                if all(
                                    board.board[start + k][col] == ""
                                    for k in range(len(word))
                                ) and all(
                                    board.not_touching(start, col, position, word)
                                ):
                                    return [start, col, position, word.upper()]
                else:
                    for start in start_pos:
                        for row in other_pos:
                            if len(board.word_list) == 0:
                                start = self.first_new_word(word)
                                return [7, start, position, word.upper()]
                            if start + len(word) < 15:
                                if all(
                                    board.board[row][start + k] == ""
                                    for k in range(len(word))
                                ) and all(
                                    board.not_touching(row, start, position, word)
                                ):
                                    return [row, start, position, word.upper()]
        return ["", "", "", ""]

    def first_new_word(self, word):
        center_index = len(word) // 2
        start = 7 - center_index
        return start

    def add_to_word(self, word_list, all_words):
        """
        Obsługa blank
        """
        if not all_words:
            return "", ""
        choice = ""
        random.shuffle(all_words)
        for word in all_words:
            word = word.lower()
            for element in word_list:
                if re.search(word, element):
                    choice = element
                if choice:
                    if choice != word:
                        choice_letters = [letter.upper() for letter in choice]
                        word_letters = [letter.upper() for letter in word]
                        all_possibble_let = word_letters + self.rack()
                        if all(
                            choice_letters.count(letter)
                            <= all_possibble_let.count(letter)
                            for letter in set(choice_letters)
                        ):
                            return word, choice
                        else:
                            choice = ""
        word, choice = "", ""
        return word, choice

    def added_letters(self, original_word, modified_word):
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

    def word_finding(self, board, word_list):
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
            result = self.new_word(board, word_list)
            if all(info != "" for info in result):
                new_word["info"] = result
                new_word["mode"] = choice
        else:
            if len(board.word_list) != 0:
                result = self.add_to_word(word_list, board.word_list)
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

    def made_word(self, board, words, letters_bag):
        current_word = {}
        bot_choice = self.word_finding(board, words)
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
            self.replace_rack(letters_bag)
        print(current_word)
        return current_word

    def bot_turn(self, board, board_sprite, words, letters_bag):
        current_word = self.made_word(board, words, letters_bag)
        for pos in current_word:
            board.draw_tiles(board_sprite, current_word[pos], pos)
            letter_hand = self.rack().index(current_word[pos])
            self.rack()[letter_hand] = ""
        board.update_board(current_word)


"""
Jeśli bot próbując ułożyć słowo żadnego nie znajdzie,
to próbuje innym sposobem, ostatecznie skippuje, albo
wymienia stojak z literami
"""
