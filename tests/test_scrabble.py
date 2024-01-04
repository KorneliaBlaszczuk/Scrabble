from player import Player
from board import Board
from letters_bag import letters
from constants import SQUARE_SIZE
from bot import Bot
import pygame
from game import ScrabbleGame
import pytest
from unittest.mock import patch
from constants import WIDTH, HEIGHT

"""
Class Player Tests
"""


def test_player():
    player = Player("Ben")
    assert player.name() == "Ben"
    assert player.words() == []
    assert player.rack() == ["", "", "", "", "", "", ""]


def test_player_update_words():
    player = Player("Ben")
    assert player.name() == "Ben"
    assert player.words() == []
    assert player.rack() == ["", "", "", "", "", "", ""]
    player.update_words("MAMA")
    assert player.words() == ["MAMA"]


def test_player_update_rack(monkeypatch):
    rack = ["C", "", "F", "G", "J", "L", "Z"]
    player = Player("Ben", rack=rack)
    board = Board()

    assert player.rack() == ["C", "", "F", "G", "J", "L", "Z"]
    monkeypatch.setattr("random.choice", lambda x: "A")
    player.updating_rack(board)
    assert player.rack() == ["C", "A", "F", "G", "J", "L", "Z"]


def test_player_update_rack_empty(monkeypatch):
    rack = ["", "", "", "", "", "", ""]
    player = Player("Ben", rack=rack)
    board = Board()

    letter_generator = iter(board.all_letters)

    monkeypatch.setattr("random.choice", lambda x: next(letter_generator))
    player.updating_rack(board)
    for i in range(len(rack)):
        assert player.rack()[i] != ""
        assert player.rack()[i] in board.all_letters


def test_player_update_no_empty(monkeypatch):
    rack = ["D", "C", "Z", "H", "L", "W", " "]
    player = Player("Ben", rack=rack)
    board = Board()

    assert player.rack() == ["D", "C", "Z", "H", "L", "W", " "]
    monkeypatch.setattr("random.choice", lambda x: "A")
    player.updating_rack(board)
    assert player.rack() == ["D", "C", "Z", "H", "L", "W", " "]


def test_update_updating_bag(monkeypatch):
    rack = ["", "", "", "", "", "", ""]
    player = Player("Ben", rack=rack)
    board = Board()
    letter_generator = iter(board.all_letters)

    monkeypatch.setattr("random.choice", lambda x: next(letter_generator))
    player.updating_rack(board)
    for i in range(len(rack)):
        letter = player.rack()[i]
        assert letter != ""
        assert (
            letters[letter][0] - player.rack().count(letter)
            == board.letters_bag[letter][0]
        )
        assert letter in board.all_letters


def test_player_reinstate_rack():
    player = Player("Ben")
    player.reinstate_rack("A")
    assert player.rack() == ["A", "", "", "", "", "", ""]


def test_player_reinstate_two_empty():
    rack = ["A", "C", "", "H", "L", "", " "]
    player = Player("Ben", rack=rack)
    player.reinstate_rack("A")
    assert player.rack() == ["A", "C", "A", "H", "L", "", " "]


def test_player_reinstate_no_empty():
    rack = ["D", "C", "Z", "H", "L", "W", " "]
    player = Player("Ben", rack=rack)
    player.reinstate_rack("A")
    assert player.rack() == ["D", "C", "Z", "H", "L", "W", " "]


def test_is_rack_used_false():
    rack = ["D", "C", "Z", "H", "L", "W", " "]
    player = Player("Ben", rack=rack)
    assert player.is_rack_used() is False


def test_is_rack_used_true():
    rack = ["", "C", "Z", "H", "L", "W", " "]
    player = Player("Ben", rack=rack)
    assert player.is_rack_used() is True


def test_replace_rack(monkeypatch):
    rack = ["C", "A", "F", "G", "J", "L", "Z"]
    player = Player("Ben", rack=rack)
    board = Board()

    assert player.rack() == ["C", "A", "F", "G", "J", "L", "Z"]
    monkeypatch.setattr("random.choice", lambda x: "A")
    player.replace_rack(board)
    assert player.rack() == ["A", "A", "A", "A", "A", "A", "A"]


def test_replace_rack_used():
    rack = ["", "C", "Z", "H", "L", "W", " "]
    player = Player("Ben", rack=rack)
    assert player.is_rack_used() is True
    board = Board()
    player.replace_rack(board)
    assert player.rack() == rack


def test_replace_updating_bag(monkeypatch):
    rack = ["", "", "", "", "", "", ""]
    player = Player("Ben", rack=rack)
    board = Board()
    letter_generator = iter(board.all_letters)

    monkeypatch.setattr("random.choice", lambda x: next(letter_generator))
    player.updating_rack(board)
    for i in range(len(rack)):
        letter = player.rack()[i]
        assert letter != ""
        assert (
            letters[letter][0]
            == player.rack().count(letter) + board.letters_bag[letter][0]
        )
        assert letter in board.all_letters


def test_empty_rack_true():
    player = Player("Ben")
    assert player.empty_rack() is True


def test_empty_rack_false():
    rack = ["", "Z", "", "", "", "", ""]
    player = Player("Ben", rack=rack)
    assert player.empty_rack() is False


def test_empty_rack_blank():
    rack = ["", " ", "", "", "", "", ""]
    player = Player("Ben", rack=rack)
    assert player.empty_rack() is False


def test_score_one_word():
    player = Player("Ben")
    board = Board()
    assert player.score_of_one_word("MAMA", board) == 6


def test_extra_points():
    player = Player("Ben")
    rack_ana = ["", "C", "Z", "H", "L", "W", " "]
    other_player = Player("Ana", rack=rack_ana)
    board = Board()
    points = player.extra_points(other_player, board)
    assert points == 9


def test_final_score():
    player = Player("Ben", words=["MAMA", "KOŃ", " MA"])
    rack_ana = ["", "C", "Z", "H", "L", "W", " "]
    other_player = Player("Ana", words=["EH"], rack=rack_ana)
    board = Board()
    score1 = player.final_score(other_player, board)
    assert score1 == 28
    score2 = other_player.final_score(player, board)
    assert score2 == -5


def test_final_score_racks_empty():
    player = Player("Ben", words=["MAMA", "KOŃ", " MA"])
    other_player = Player("Ana", words=["EH"])
    board = Board()
    assert player.final_score(other_player, board) == 19
    assert other_player.final_score(player, board) == 4


"""
Class Board Tests
"""


def test_board():
    board = Board()
    assert board.board == []
    assert board.word_list == []
    assert board.all_letters == letters.keys()
    assert board.letters_bag == letters


def test_create_board():
    board = Board()
    board.create_board()
    assert len(board.board) == 15
    assert len(board.board[0]) == 15
    assert all(element == "" for element in board.board[0])


def test_update_board():
    board = Board()
    board.create_board()
    board.current_word = {(1, 2): "B", (2, 2): "A"}
    board.update_board()
    assert board.board[1][2] == "B"
    assert board.board[2][2] == "A"


def test_update_board_empty_current():
    board = Board()
    board.create_board()
    board.current_word = {}
    board.update_board()
    for row in board.board:
        assert all(element == "" for element in row)


def test_remove_from_board():
    board = Board()
    board.create_board()
    board.current_word = {(1, 2): "B", (2, 2): "A"}
    board.update_board()
    assert board.board[1][2] == "B"
    assert board.board[2][2] == "A"
    board.remove_from_board()
    assert board.board[1][2] == ""
    assert board.board[2][2] == ""


def test_update_word_list():
    board = Board()
    assert board.word_list == []
    board.update_word_list("MAMA")
    assert board.word_list == ["MAMA"]


def test_taking_out(monkeypatch):
    board = Board()
    monkeypatch.setattr("random.choice", lambda x: "A")
    assert board.taking_out() == "A"


def test_row_col_to_coord():
    board = Board()
    row, col = 2, 5
    coordinates = board.row_col_to_coord(row, col)
    assert coordinates == (col * SQUARE_SIZE, row * SQUARE_SIZE)


def test_coord_to_row_col():
    board = Board()
    position = 250, 150
    result = board.coord_to_row_col(position)
    assert result == (2, 4)


def test_addword():
    board = Board()
    board.create_board()
    board.current_word = {(1, 2): "B", (2, 2): "A", (4, 2): "C"}
    result = board.addword()
    assert result == [(3, 4), 2]


def test_addword_col():
    board = Board()
    board.create_board()
    board.current_word = {(2, 7): "W", (4, 7): "N", (5, 7): "O"}
    result = board.addword()
    assert result == [(3, 4), 7]


def test_addword_alone():
    board = Board()
    board.create_board()
    board.current_word = {(1, 2): "B", (2, 2): "A", (3, 2): "C"}
    result = board.addword()
    assert result == [(0, 0), 2]


def test_valid_added():
    board = Board()
    board.create_board()
    board.current_word = {(1, 2): "B", (2, 2): "A", (4, 2): "C"}
    result = board.valid_added_word()
    assert not result


def test_valid_blank():
    board = Board()
    board.create_board()
    board.current_word = {
        (3, 7): "I",
        (3, 8): "K",
        (3, 9): "T",
        (4, 8): " ",
        (5, 8): "D",
    }
    result = board.update_board()
    board.current_word_empty()
    board.current_word = {(2, 7): "W", (4, 7): "N", (5, 7): "O"}
    result = board.valid_added_word()
    assert result


def test_valid_added_two_word_add():
    board = Board()
    board.create_board()
    board.current_word = {
        (3, 7): "M",
        (3, 8): "I",
        (3, 9): "T",
        (5, 7): "Ł",
        (5, 8): "O",
        (5, 9): "Ś",
    }
    result = board.update_board()
    board.current_word_empty()
    board.current_word = {(2, 8): "M", (4, 8): "G", (6, 8): "T"}
    result = board.valid_added_word()
    assert not result


def test_valid_added_empty():
    board = Board()
    board.create_board()
    board.current_word = {(1, 2): "B", (2, 2): "A", (3, 2): "C"}
    result = board.valid_added_word()
    assert not result


def test_valid_added_true():
    board = Board()
    board.create_board()
    board.current_word = {(3, 2): "C", (4, 2): "D"}
    board.update_board()
    board.current_word = {(1, 2): "B", (2, 2): "A", (5, 2): "C"}
    result = board.valid_added_word()
    assert result


def test_valid_added_cross():
    board = Board()
    board.create_board()
    board.current_word = {(2, 4): "W", (2, 5): "I", (2, 6): "I"}
    board.update_board()
    board.current_word = {(1, 5): "G", (2, 5): "I", (3, 5): "T"}
    result = board.valid_added_word()
    assert result


def test_valid_added_alone():
    board = Board()
    board.create_board()
    board.current_word = {(1, 2): "B", (2, 2): "A", (3, 2): "C"}
    result = board.valid_added_word()
    assert not result


def test_valid_added_one_false():
    board = Board()
    board.create_board()
    board.current_word = {(4, 2): "D"}
    board.update_board()
    board.current_word = {(1, 2): "B", (2, 2): "A", (5, 2): "C"}
    result = board.valid_added_word()
    assert not result


def test_alone_tile():
    board = Board()
    board.create_board()
    board.current_word_update((1, 2), "A")
    result = board.not_touching(
        list(board.current_word.keys())[0][0],
        list(board.current_word.keys())[0][1],
    )
    assert result


def test_not_touching():
    board = Board()
    board.create_board()
    word = "MAMA"
    row_start, col_start = 4, 2
    position = "vertical"
    result = board.not_touching(row_start, col_start, position, word)
    assert all(valid for valid in result)


def test_touching():
    board = Board()
    board.create_board()
    board.board[3][2] = "T"
    word = "MAMA"
    row_start, col_start = 4, 2
    position = "vertical"
    result = board.not_touching(row_start, col_start, position, word)
    assert not all(valid for valid in result)


def test_check_row_empty():
    board = Board()
    board.create_board()
    assert board.check_row() == []


def test_check_row():
    board = Board()
    board.create_board()
    board.current_word = {(4, 1): "T", (4, 2): "A"}
    board.update_board()
    assert board.check_row() == ["TA"]


def test_more_words_row():
    board = Board()
    board.create_board()
    board.current_word = {
        (4, 1): "T",
        (4, 2): "A",
        (4, 3): "T",
        (4, 5): "A",
        (4, 6): "T",
        (4, 7): "A",
    }
    board.update_board()
    assert board.check_row() == ["TAT", "ATA"]


def test_check_col_empty():
    board = Board()
    board.create_board()
    assert board.check_col() == []


def test_check_col():
    board = Board()
    board.create_board()
    board.current_word = {(4, 1): "T", (5, 1): "A"}
    board.update_board()
    assert board.check_col() == ["TA"]


def test_more_words_col():
    board = Board()
    board.create_board()
    board.current_word = {
        (1, 1): "T",
        (2, 1): "A",
        (3, 1): "T",
        (5, 1): "A",
        (6, 1): "T",
        (7, 1): "A",
    }
    board.update_board()
    assert board.check_col() == ["TAT", "ATA"]


def test_word_in_board_empty():
    board = Board()
    board.create_board()
    assert board.word_in_board() == []


def test_word_in_board():
    board = Board()
    board.create_board()
    board.current_word = {
        (4, 1): "T",
        (4, 2): "A",
        (4, 3): "T",
        (4, 4): "A",
    }
    board.update_board()
    assert board.word_in_board() == ["TATA"]


def test_word_in_board_too_long():
    board = Board()
    board.create_board()
    board.current_word = {
        (4, 1): "T",
        (4, 2): "A",
        (4, 3): "T",
        (4, 4): "A",
        (4, 5): "T",
        (4, 6): "A",
    }
    board.update_board()
    assert board.word_in_board() == []


def test_word_in_board_too_short():
    board = Board()
    board.create_board()
    board.current_word = {(4, 1): "T"}
    board.update_board()
    assert board.word_in_board() == []


def test_word_in_board_row_and_col():
    board = Board()
    board.create_board()
    board.current_word = {
        (1, 1): "T",
        (2, 1): "A",
        (3, 1): "T",
        (4, 1): "A",
        (6, 5): "T",
        (7, 5): "A",
        (4, 5): "A",
        (4, 6): "T",
        (4, 7): "A",
    }
    board.update_board()
    assert board.word_in_board() == ["ATA", "TATA", "TA"]


def test_word_authentication():
    board = Board()
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    word = "MAMA"
    assert board.word_authentication(word, words)


def test_word_authentication_false():
    board = Board()
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    word = "PEJ"
    assert not board.word_authentication(word, words)


def test_word_authentication_one_blank():
    board = Board()
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    word = " Y"
    assert board.word_authentication(word, words)


def test_word_authentication_one_blank_another():
    board = Board()
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    word = " W"
    assert board.word_authentication(word, words)


def test_word_authentication_two_blank():
    board = Board()
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    word = "M M "
    assert board.word_authentication(word, words)


def test_word_authentication_two_blank_only():
    board = Board()
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    word = "  "
    assert board.word_authentication(word, words)


def test_word_checking_true():
    board = Board()
    board.create_board()
    board.current_word = {
        (1, 1): "T",
        (2, 1): "A",
        (3, 1): "T",
        (4, 1): "A",
        (6, 5): "T",
        (7, 5): "A",
    }
    board.update_board()
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    assert board.word_checking(words)


def test_word_checking_cross():
    board = Board()
    board.create_board()
    board.current_word = {(2, 4): "W", (2, 5): "I", (2, 6): "I"}
    board.update_board()
    board.current_word = {(1, 5): "G", (2, 5): "I", (3, 5): "T"}
    board.update_board()
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    assert board.word_checking(words)


def test_word_checking_false():
    board = Board()
    board.create_board()
    board.current_word = {
        (1, 1): "T",
        (2, 1): "A",
        (3, 1): "T",
        (4, 1): "W",
        (6, 5): "T",
        (7, 5): "Z",
    }
    board.update_board()
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    assert not board.word_checking(words)


def test_word_list_add():
    board = Board()
    player = Player("Gracz")
    board.create_board()
    board.current_word = {
        (1, 1): "T",
        (2, 1): "A",
        (3, 1): "T",
        (4, 1): "A",
        (6, 5): "T",
        (7, 5): "A",
    }
    board.update_board()
    board.update_word_list("TATA")
    board.word_lists_adding(player)
    assert player.words() == ["TA"]
    assert board.word_list == ["TATA", "TA"]


def test_exist():
    board = Board()
    board.create_board()
    board.current_word = {
        (1, 1): "T",
        (2, 1): "A",
        (3, 1): "T",
        (4, 1): "A",
        (6, 5): "T",
        (7, 5): "A",
    }
    board.update_board()
    assert board.exist("TATA") == ["vertical", 1, 1]


def test_exist_false():
    board = Board()
    board.create_board()
    board.current_word = {
        (1, 1): "T",
        (2, 1): "A",
        (3, 1): "T",
        (4, 1): "A",
        (6, 5): "T",
        (7, 5): "A",
    }
    board.update_board()
    assert not board.exist("MAMA")


def test_space_count():
    board = Board()
    word_coord = [1, 2, 3, 7, 8, 12, 13]
    assert board.space_count(word_coord) == 2


"""
Class Bot Tests
"""


def test_bot():
    bot = Bot()
    assert bot.name() == "Bot"
    assert bot.words() == []
    assert bot.rack() == ["", "", "", "", "", "", ""]


def test_first_word():
    pass


def test_valid_new_word():
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    rack = ["A", "A", "M", "Z", "W", "R", "S"]
    bot = Bot(rack=rack)
    board = Board()
    board.update_word_list("A")
    assert bot.valid_new_word(words, board) == (("a", "aa"), "A")


def test_valid_new_word_none():
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    rack = ["L", "W", "F", "Ź", "P", "R", "S"]
    # there won't be any avaible words, because there is no vowel on rack
    bot = Bot(rack=rack)
    board = Board()
    board.update_word_list("HM")
    assert bot.valid_new_word(words, board) == (("", ""), "HM")


def test_new_word_vertical_first(monkeypatch):
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    board = Board()
    board.create_board()
    rack = ["A", "A", "M", "Z", "W", "R", "S"]
    bot = Bot(rack=rack)
    monkeypatch.setattr("random.choice", lambda x: "vertical")
    result = bot.new_word(board, words)
    assert result[1] == 7


def test_new_word_horizontal_first(monkeypatch):
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    board = Board()
    board.create_board()
    rack = ["A", "A", "M", "Z", "W", "R", "S"]
    bot = Bot(rack=rack)
    monkeypatch.setattr("random.choice", lambda x: "horizontal")
    result = bot.new_word(board, words)
    assert result[0] == 7


def test_first_new_word_even():
    bot = Bot()
    assert bot.first_word("MECH") == 5


def test_first_new_word_odd():
    bot = Bot()
    assert bot.first_word("BÓG") == 6


def test_find_matching_choice():
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    rack = ["I", "A", "M", "Z", "W", "R", "S"]
    bot = Bot(rack=rack)
    result = bot.find_matching_choice("mama", words)
    assert result == "imama"


def test_find_matching_choice_none():
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    rack = ["", "", "", "", "", "", ""]
    bot = Bot(rack=rack)
    result = bot.find_matching_choice("mama", words)
    assert result == ""


def test_add_to():
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    rack = ["I", "A", "M", "Z", "W", "R", "S"]
    bot = Bot(rack=rack)
    word_list = ["mama"]
    result = bot.add_to(words, word_list)
    assert result == ("mama", "imama")


def test_add_to_word_no_list():
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    rack = ["I", "A", "M", "Z", "W", "R", "S"]
    word_list = []
    bot = Bot(rack=rack)
    result = bot.add_to(words, word_list)
    assert result == ("", "")


def test_add_to_word_none():
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    rack = ["", "", "", "", "", "", ""]
    bot = Bot(rack=rack)
    word_list = ["MAMA"]
    result = bot.add_to(words, word_list)
    assert result == ("", "")


def test_added_letters():
    bot = Bot()
    result = bot.added_letters("mama", "imama")
    assert result == {(0, 0): "i"}


def test_added_letters_no():
    bot = Bot()
    result = bot.added_letters("mama", "mama")
    assert result == {}


def test_added_letters_prefix_suffix():
    bot = Bot()
    result = bot.added_letters("tu", "student")
    assert result == {
        (0, 0): "s",
        (3, 1): "d",
        (4, 1): "e",
        (5, 1): "n",
        (6, 1): "t",
    }


def test_valid_add_position():
    bot = Bot()
    board = Board()
    board.create_board()
    current_word = {(1, 0): "A", (1, 1): "M"}
    for pos in current_word:
        board.current_word_update(pos, current_word[pos])
    board.update_board()
    assert bot.valid_add_pos(board, 1, 2, "vertical", "AM")


def test_valid_add_position_alone():
    bot = Bot()
    board = Board()
    board.create_board()
    assert not bot.valid_add_pos(board, 1, 2, "vertical", "AM")


def test_valid_add_position_too_long():
    bot = Bot()
    board = Board()
    board.create_board()
    assert not bot.valid_add_pos(board, 14, 2, "vertical", "AM")


def test_valid_add_edge():
    bot = Bot()
    board = Board()
    board.create_board()
    current_word = {(14, 11): "A", (14, 12): "M"}
    for pos in current_word:
        board.current_word_update(pos, current_word[pos])
    board.update_board()
    assert bot.valid_add_pos(board, 14, 13, "horizontal", "AM")


def test_made_current_word_vertical():
    info = [10, 12, "vertical", "A"]
    bot = Bot()
    assert bot.made_current_word(info) == {(10, 12): "A"}


def test_made_current_word_horizontal():
    info = [10, 12, "horizantal", "A"]
    bot = Bot()
    assert bot.made_current_word(info) == {(10, 12): "A"}


def test_attempts_no():
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    bot = Bot()
    board = Board()
    board.create_board()
    result = bot.attempts(board, words)
    assert not result  # we don't have handler so no words can be made


def test_attempt(monkeypatch):
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    rack = ["A", "A", "M", "Z", "W", "R", "S"]
    monkeypatch.setattr("random.choice", lambda x: "new")
    bot = Bot(rack=rack)
    board = Board()
    board.create_board()
    result = bot.attempts(board, words)
    assert result


def test_attempts_result_new(monkeypatch):
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    monkeypatch.setattr("random.choice", lambda x: "new")
    rack = ["A", "A", "M", "Z", "W", "R", "S"]
    bot = Bot(rack=rack)
    board = Board()
    board.create_board()
    result = bot.attempts(board, words)
    assert result["mode"] == "new"
    assert sorted(result.keys()) == sorted(["info", "mode"])


def test_attempts_add(monkeypatch):
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    monkeypatch.setattr("random.choice", lambda x: "add")
    rack = ["A", "A", "M", "Z", "W", "R", "S"]
    bot = Bot(rack=rack)
    board = Board()
    board.create_board()
    all_words = {
        (6, 5): "T",
        (7, 5): "A",
    }
    board.update_board(all_words)
    board.update_word_list("TA")
    result = bot.attempts(board, words)
    assert result["mode"] == "add"
    assert sorted(result.keys()) == sorted(
        ["prefix", "sufix", "old_word", "new_word", "mode"]
    )


def test_made_word(monkeypatch):
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    monkeypatch.setattr("random.choice", lambda x: "new")
    rack = ["A", "A", "M", "Z", "W", "R", "S"]
    bot = Bot(rack=rack)
    board = Board()
    board.create_board()
    result = bot.made_word(board, words)
    assert result


def test_made_word_no(monkeypatch):
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    monkeypatch.setattr("random.choice", lambda x: "new")
    rack = ["", "A", "", "", "", "", ""]
    bot = Bot(rack=rack)
    board = Board()
    board.create_board()
    result = bot.made_word(board, words)
    assert not result


def test_made_word_add_to_new(monkeypatch):
    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()
    monkeypatch.setattr("random.choice", lambda x: "add")
    rack = ["Z", "A", "", "", "", "", ""]
    bot = Bot(rack=rack)
    board = Board()
    board.create_board()
    result = bot.made_word(board, words)
    assert result


@pytest.fixture
def game_instance():
    # Set up the Pygame window
    pygame.init()
    game = ScrabbleGame()
    yield game
    pygame.quit()


def test_start_win_displayed(game_instance):
    # Check if the window is displayed as expected
    assert pygame.display.get_surface().get_at((WIDTH // 2, HEIGHT)) == (0, 0, 0, 255)

    assert game_instance.player_score == 0
    assert game_instance.bot_score == 0


def test_game_init():
    game = ScrabbleGame()
    assert isinstance(game, ScrabbleGame)


def test_win_displayed(game_instance):
    # Use patch to mock the behavior of pygame.display.update()
    with patch("pygame.display.update") as mock_update:
        game_instance.start_win()
        mock_update.assert_called_once()

    assert pygame.display.get_surface().get_at((WIDTH // 2, (HEIGHT // 2))) == (
        251,
        249,
        249,
        255,
    )
