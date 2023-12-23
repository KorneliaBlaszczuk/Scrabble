import pygame
import sys
from board import Board
from constants import (
    EXTRA_SPACE,
    WIDTH,
    HEIGHT,
    extra_space_x,
    extra_space_y,
    SQUARE_SIZE,
    COLS,
    CENTRAL_COLOR,
    WHITE,
)
from tiles import Tile
from player import Player
from bot import Bot

player_score = 0
bot_score = 0


pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT + EXTRA_SPACE))
pygame.display.set_caption("SCRABBLE")
pygame.font.init()


def start_win():
    WIN.fill(CENTRAL_COLOR)

    text_data = [
        {
            "text": "SCRABBLE GAME",
            "font": 70,
            "coord": (WIDTH // 2, (HEIGHT // 2)),
        },
        {
            "text": "BY KORNELIA BŁASZCZUK",
            "font": 30,
            "coord": (WIDTH // 2, (HEIGHT // 2) + EXTRA_SPACE),
        },
        {
            "text": "CLICK SPACE BAR TO BEGIN",
            "font": 50,
            "coord": (WIDTH // 2, (HEIGHT // 2) + 3 * EXTRA_SPACE),
        },
    ]

    for e, data in enumerate(text_data):
        font_loc = "fonts/{type}.ttf"
        font_type = font_loc.format(
            type="rubikdoodle" if e == 0 or e == 2 else "rubikname"
        )
        font = pygame.font.Font(font_type, data["font"])
        text = font.render(data["text"], True, WHITE)
        text_rect = text.get_rect(center=data["coord"])
        WIN.blit(text, text_rect)

    pygame.display.update()


def game():
    global bot_score
    global player_score
    """Zmienna definiująca, czy gra jest aktywna, działa w danym momencie"""
    run = True
    """Definujemy zegar, który kontroluje nam liczbę FPS"""
    clock = pygame.time.Clock()
    board_sprite = pygame.sprite.Group()
    rack_sprite = pygame.sprite.Group()

    current_next_pos = []

    player = Player("Gracz")
    bot = Bot()
    board = Board()

    board.create_board()

    player.updating_rack(board)
    board.draw_rack(player.rack(), rack_sprite)

    bot.updating_rack(board)

    current_word = {}

    skip_count = 0
    round = 1

    with open("slowa.txt", "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()

    while run:
        """Częstotliwość odświeżania"""
        clock.tick(60)
        """
        Sprawdza wystąpienie danych zdarzeń (eventów) w danym momencie
        """
        for event in pygame.event.get():
            """Zamyka okno interaktywne"""
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    end()
                    run = False

                if event.key == pygame.K_r:
                    if player.is_rack_used():
                        rack_sprite.empty()
                        player.replace_rack(board)
                        bot.bot_turn(board, board_sprite, words, board)
                        bot.updating_rack(board)
                        board.draw_rack(player.rack(), rack_sprite)
                        round += 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    skip_count += 1
                    board.not_valid(board_sprite, current_word, player)
                    bot.bot_turn(board, board_sprite, words, board)
                    bot.updating_rack(board)
                    board.draw_rack(player.rack(), rack_sprite)
                    round += 1
                    if skip_count == 2 or bot.empty_rack():
                        end()
                        run = False

                else:
                    skip_count = 0

            """Czy nacisneliśmy przycisk myszki"""
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                x, y = position
                row, col = board.get_row_col_from_mouse(position)
                current_next_pos.append((row, col))
                count = len(current_next_pos)
                if (
                    (count == 1 and ((current_next_pos[0][0] != 16)))
                    or (count == 1 and (current_next_pos[0][1] > 10))
                    or (count == 1 and (current_next_pos[0][1] < 4))
                    or (
                        count == 1 and (player.rack()[current_next_pos[0][1] - 4] == "")
                    )
                    or (count == 2 and (current_next_pos[1][0] > 14))
                    or (count == 2 and (board.colid(board_sprite, current_next_pos)))
                ):
                    current_next_pos.clear()
                    count = 0
                if len(current_next_pos) == 2:
                    rack_row, rack_col = current_next_pos[0]
                    letter_row, letter_col = current_next_pos[1]
                    letter_x, letter_y = board.calc_coordinates(letter_row, letter_col)
                    rack_x, rack_y = board.calc_coordinates(rack_row, rack_col)

                    if player.rack()[rack_col - 4] == "":
                        current_next_pos.clear()
                        break
                    else:
                        pass
                    # kiedy gracz kliknie na plansze jako pierwsze

                    letter_title = Tile(
                        player.rack()[rack_col - 4], (letter_x, letter_y)
                    )

                    letter_row, letter_col = board.get_row_col_from_mouse((x, y))

                    current_word[(letter_row, letter_col)] = letter_title.letter()
                    rack_sprite.empty()
                    board_sprite.add(letter_title)

                    """
                    Aktualizacja stojaka
                    """

                    player.rack()[rack_col - 4] = ""

                    x = extra_space_x
                    y = (COLS + 1) * SQUARE_SIZE

                    for current_letters in player.rack():
                        if current_letters == "":
                            x += SQUARE_SIZE
                        else:
                            letter = Tile(current_letters, (x, y))
                            rack_sprite.add(letter)
                            x += SQUARE_SIZE
                    x = extra_space_x
                    y = extra_space_y + EXTRA_SPACE // 2
                    current_next_pos.clear()

            """Kiedy nacisneliśmy ENTER słowo dodawane jest do listy,
            a w stojaku uzupełniane są puste pola"""
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and current_word:
                    if len(board.word_list) == 0:
                        if any(key == (7, 7) for key in current_word.keys()):
                            pass
                        else:
                            board.not_valid(board_sprite, current_word, player)
                            current_word = {}
                    else:
                        if len(current_word.values()) < 2:
                            for pos in current_word:
                                if board.alone_tile(pos):
                                    board.not_valid(board_sprite, current_word, player)
                                    current_word = {}
                                else:
                                    continue
                        else:
                            row_key = [item[0] for item in current_word.keys()]
                            col_key = [item[1] for item in current_word.keys()]
                            if all(
                                x == row_key[0] for x in row_key
                            ) and board.valid_added_word(current_word):
                                current_word = dict(
                                    sorted(
                                        current_word.items(),
                                        key=lambda item: item[0][0],
                                    )
                                )
                            elif all(
                                x == col_key[1] for x in col_key
                            ) and board.valid_added_word(current_word):
                                current_word = dict(
                                    sorted(
                                        current_word.items(),
                                        key=lambda item: item[0][1],
                                    )
                                )
                            else:
                                board.not_valid(board_sprite, current_word, player)
                                current_word = {}
                    board.update_board(current_word)

                    board.validation(board_sprite, words, current_word, player)

                    if board.word_list:
                        if len(board.word_list[-1]) > len(current_word.values()):
                            previous_coord = board.addword_to(current_word)
                            prev_word = ""
                            for row, col in previous_coord:
                                prev_word += board.board[row][col]
                            if prev_word in board.word_list:
                                board.word_list.remove(prev_word)

                    current_word = {}

                    bot.bot_turn(board, board_sprite, words, board)
                    bot.updating_rack(board)

                    player.updating_rack(board)
                    board.draw_rack(player.rack(), rack_sprite)

                    round += 1

                    if player.empty_rack() or bot.empty_rack():
                        end()
                        run = False

                    else:
                        continue

        global player_score
        player_score = player.final_score(bot, board)

        bot_score = bot.final_score(player, board)

        board.draw_squares(WIN)
        board.draw_extra_squares(WIN)
        rack_sprite.update()
        rack_sprite.draw(WIN)
        board_sprite.update()
        board_sprite.draw(WIN)
        pygame.display.update()

    return run


def end():
    WIN.fill(CENTRAL_COLOR)
    pygame.font.init()

    font = pygame.font.Font(None, 36)

    text_info = [
        {
            "text": "THE END!",
            "font": 50,
            "coord": (WIDTH // 2, (HEIGHT // 2) + EXTRA_SPACE),
        },
        {
            "text": f"Your score: {player_score}",
            "font": 30,
            "coord": (WIDTH // 2, (HEIGHT // 2) + 2 * EXTRA_SPACE),
        },
        {
            "text": f"Bot score: {bot_score}",
            "font": 30,
            "coord": (WIDTH // 2, (HEIGHT // 2) + 3 * EXTRA_SPACE),
        },
    ]

    for e, data in enumerate(text_info):
        font_loc = "fonts/{type}.ttf"
        font_type = font_loc.format(type="rubikdoodle" if e == 0 else "rubikname")
        font = pygame.font.Font(font_type, data["font"])
        text = font.render(data["text"], True, WHITE)
        text_rect = text.get_rect(center=data["coord"])
        WIN.blit(text, text_rect)
    pygame.display.flip()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()

    """WIN.fill(CENTRAL_COLOR)


    for e, data in enumerate(text_info):
        font_loc = "fonts/{type}.ttf"
        font_type = font_loc.format(type="rubikdoodle" if e == 0 else "rubikname")
        font = pygame.font.Font(font_type, data["font"])
        text = font.render(data["text"], True, WHITE)
        text_rect = text.get_rect(center=data["coord"])
        WIN.blit(text, text_rect)

    run_end = True"""


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = game()[0]
        if run:
            start_win()
    pygame.quit()
    sys.exit()


main()
