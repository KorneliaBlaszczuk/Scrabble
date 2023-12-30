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
    DUN,
    rect_x,
    rect_y,
    rect_width,
    rect_height,
)
from tiles import Tile
from player import Player
from bot import Bot


"""
Make game class
"""


class ScrabbleGame:
    def __init__(self):
        pygame.init()
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT + 2 * EXTRA_SPACE))
        pygame.display.set_caption("SCRABBLE")
        pygame.font.init()

    def start_win(self):
        self.WIN.fill(CENTRAL_COLOR)

        text_data = [
            {
                "text": "SCRABBLE GAME",
                "font": SQUARE_SIZE,
                "coord": (WIDTH // 2, (HEIGHT // 2)),
            },
            {
                "text": "BY KORNELIA BŁASZCZUK",
                "font": SQUARE_SIZE // 2,
                "coord": (WIDTH // 2, (HEIGHT // 2) + EXTRA_SPACE),
            },
            {
                "text": "CLICK SPACE BAR TO BEGIN",
                "font": SQUARE_SIZE,
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
            self.WIN.blit(text, text_rect)

        pygame.display.update()

    def name_win(self):
        self.WIN.fill(CENTRAL_COLOR)

        player_name = ""

        base_font = pygame.font.Font(None, SQUARE_SIZE)
        user_text = ""

        input_rect = pygame.Rect(
            rect_x,
            2 * HEIGHT // 3,
            rect_width,
            rect_height,
        )

        text_data = [
            {
                "text": "Please, enter your name (max 10 characters).",
                "coord": (WIDTH // 2, (HEIGHT // 2)),
            },
            {
                "text": "Click to write:",
                "coord": (WIDTH // 2, (HEIGHT // 2) + EXTRA_SPACE // 2),
            },
            {
                "text": "Click ENTER to continue",
                "coord": (WIDTH // 2, (HEIGHT // 2) + 3 * EXTRA_SPACE),
            },
        ]

        for e, data in enumerate(text_data):
            font = pygame.font.Font("fonts/rubikname.ttf", SQUARE_SIZE // 2)
            text = font.render(data["text"], True, WHITE)
            text_rect = text.get_rect(center=data["coord"])
            self.WIN.blit(text, text_rect)

        active = False
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        active = True
                    else:
                        active = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE and active:
                        user_text = user_text[:-1]

                    if event.key == pygame.K_RETURN:
                        player_name = user_text
                        run = False

                    elif active:
                        user_text += event.unicode

            if len(user_text) == 10:
                player_name = user_text
                run = False

            color = "grey" if active else "white"

            pygame.draw.rect(self.WIN, color, input_rect)

            name_surface = base_font.render(user_text, True, "black")

            name_rect = name_surface.get_rect(
                center=(WIDTH // 2, 2 * HEIGHT // 3 + rect_height // 2)
            )
            self.WIN.blit(name_surface, name_rect)

            pygame.display.flip()
        return player_name

    def game(self, player_name):
        self.WIN.fill(DUN)
        """Zmienna definiująca, czy gra jest aktywna,
        działa w danym momencie"""
        run = True
        """Definujemy zegar, który kontroluje nam liczbę FPS"""
        clock = pygame.time.Clock()
        board_sprite = pygame.sprite.Group()
        rack_sprite = pygame.sprite.Group()

        current_next_pos = []

        player = Player(player_name)
        bot = Bot()
        board = Board()

        board.create_board()

        player.updating_rack(board)
        board.draw_rack(player.rack(), rack_sprite)

        bot.updating_rack(board)

        current_word = {}

        player_score = 0
        bot_score = 0

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
                        self.end(player_name, player_score, bot_score)
                        run = False

                    if event.key == pygame.K_r:
                        if player.is_rack_used() is False:
                            rack_sprite.empty()
                            player.replace_rack(board)
                            bot.bot_turn(board, board_sprite, words)
                            bot.updating_rack(board)
                            board.draw_rack(player.rack(), rack_sprite)
                            round += 1

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        skip_count += 1
                        board.not_valid(board_sprite, current_word, player)
                        bot.bot_turn(board, board_sprite, words)
                        bot.updating_rack(board)
                        board.draw_rack(player.rack(), rack_sprite)
                        round += 1
                        if skip_count == 2 or bot.empty_rack():
                            self.end(player_name, player_score, bot_score)
                            run = False

                    else:
                        skip_count = 0

                """Czy nacisneliśmy przycisk myszki"""
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    x, y = position
                    row, col = board.coord_to_row_col(position)
                    current_next_pos.append((row, col))
                    count = len(current_next_pos)
                    if (
                        (count == 1 and ((current_next_pos[0][0] != 16)))
                        or (count == 1 and (current_next_pos[0][1] > 10))
                        or (count == 1 and (current_next_pos[0][1] < 4))
                        or (
                            count == 1
                            and (player.rack()[current_next_pos[0][1] - 4] == "")
                        )
                        or (count == 2 and (current_next_pos[1][0] > 14))
                        or (
                            count == 2
                            and (
                                board.colid(
                                    board_sprite,
                                    current_next_pos,
                                )
                            )
                        )
                    ):
                        current_next_pos.clear()
                        count = 0
                    if len(current_next_pos) == 2:
                        rack_row, rack_col = current_next_pos[0]
                        letter_row, letter_col = current_next_pos[1]
                        letter_x, letter_y = board.row_col_to_coord(
                            letter_row,
                            letter_col,
                        )
                        rack_x, rack_y = board.row_col_to_coord(
                            rack_row,
                            rack_col,
                        )

                        if player.rack()[rack_col - 4] == "":
                            current_next_pos.clear()
                            break
                        else:
                            pass
                        # kiedy gracz kliknie na plansze jako pierwsze

                        letter_title = Tile(
                            player.rack()[rack_col - 4], (letter_x, letter_y)
                        )

                        letter_row, letter_col = board.coord_to_row_col((x, y))

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
                                board.not_valid(
                                    board_sprite,
                                    current_word,
                                    player,
                                )
                                current_word = {}
                        else:
                            if len(current_word.values()) < 2:
                                for pos in current_word:
                                    if board.alone_tile(pos):
                                        board.not_valid(
                                            board_sprite, current_word, player
                                        )
                                        current_word = {}
                                    else:
                                        continue
                            else:
                                row_key = [item[0] for item in current_word.keys()]
                                col_key = [item[1] for item in current_word.keys()]
                                if all(x == row_key[0] for x in row_key):
                                    sorted_word = dict(
                                        sorted(
                                            current_word.items(),
                                            key=lambda item: item[0][1],
                                        )
                                    )
                                    print(board.valid_added_word(sorted_word))
                                    if not board.valid_added_word(sorted_word):
                                        board.not_valid(
                                            board_sprite,
                                            current_word,
                                            player,
                                        )
                                        current_word = {}
                                    else:
                                        current_word = sorted_word
                                elif all(y == col_key[0] for y in col_key):
                                    sorted_word = dict(
                                        sorted(
                                            current_word.items(),
                                            key=lambda item: item[0][0],
                                        )
                                    )
                                    print(board.valid_added_word(sorted_word))
                                    if not board.valid_added_word(sorted_word):
                                        board.not_valid(
                                            board_sprite,
                                            current_word,
                                            player,
                                        )
                                        current_word = {}
                                    else:
                                        current_word = sorted_word
                                else:
                                    print("none placement")
                                    board.not_valid(
                                        board_sprite,
                                        current_word,
                                        player,
                                    )
                                    current_word = {}
                        board.update_board(current_word)
                        board.validation(
                            board_sprite,
                            words,
                            current_word,
                            player,
                        )
                        print(player.rack())
                        if board.word_list and len(current_word) > 1:
                            if len(board.word_list[-1]) > len(current_word.values()):
                                previous_coord = board.addword(current_word)
                                prev_word = ""
                                if type(previous_coord[0][0]) is tuple:
                                    coords = previous_coord[0][0]
                                    col = previous_coord[0][1]
                                    for row in range(coords[0], coords[1]):
                                        prev_word += board.board[row][col]
                                else:
                                    coords = previous_coord[0][1]
                                    row = previous_coord[0][0]
                                    for col in range(coords[0], coords[1]):
                                        prev_word += board.board[row][col]

                                if prev_word in board.word_list:
                                    board.word_list.remove(prev_word)

                        current_word = {}

                        print(board.word_list)

                        bot.bot_turn(board, board_sprite, words)
                        bot.updating_rack(board)

                        player.updating_rack(board)
                        board.draw_rack(player.rack(), rack_sprite)

                        round += 1

                        if player.empty_rack() or bot.empty_rack():
                            self.end(player_name, player_score, bot_score)
                            run = False

                        else:
                            continue

            pygame.draw.rect(
                self.WIN,
                CENTRAL_COLOR,
                (rect_x, rect_y, rect_width, rect_height),
            )

            current_text = f"Round {round}"
            font = pygame.font.Font("fonts/rubikname.ttf", 30)
            text = font.render(current_text, True, WHITE)
            text_rect = text.get_rect(
                center=(WIDTH // 2, rect_y + rect_height // 2),
            )
            self.WIN.blit(text, text_rect)
            pygame.display.flip()

            player_score = player.final_score(bot, board)
            bot_score = bot.final_score(player, board)

            board.draw_squares(self.WIN)
            board.draw_rack_squares(self.WIN)
            rack_sprite.update()
            rack_sprite.draw(self.WIN)
            board_sprite.update()
            board_sprite.draw(self.WIN)
            pygame.display.update()

        return run

    def end(self, player_name, player_score, bot_score):
        self.WIN.fill(CENTRAL_COLOR)
        pygame.font.init()

        font = pygame.font.Font(None, 36)

        winner_name = player_name if player_score > bot_score else "Bot"

        text_info = [
            {
                "text": "THE END!",
                "font": SQUARE_SIZE,
                "coord": (WIDTH // 2, (HEIGHT // 2) + EXTRA_SPACE),
            },
            {
                "text": f"{player_name}'s score: {player_score}",
                "font": SQUARE_SIZE // 2,
                "coord": (WIDTH // 2, (HEIGHT // 2) + 2 * EXTRA_SPACE),
            },
            {
                "text": f"Bot score: {bot_score}",
                "font": SQUARE_SIZE // 2,
                "coord": (WIDTH // 2, (HEIGHT // 2) + 3 * EXTRA_SPACE),
            },
            {
                "text": f"{winner_name} won",
                "font": SQUARE_SIZE,
                "coord": (WIDTH // 2, (HEIGHT // 2) + 4 * EXTRA_SPACE),
            },
        ]

        for e, data in enumerate(text_info):
            font_loc = "fonts/{type}.ttf"
            font_type = font_loc.format(
                type="rubikdoodle" if e == 0 or e == 3 else "rubikname"
            )
            font = pygame.font.Font(font_type, data["font"])
            text = font.render(data["text"], True, WHITE)
            text_rect = text.get_rect(center=data["coord"])
            self.WIN.blit(text, text_rect)
        pygame.display.flip()

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    pygame.quit()
                    sys.exit()
