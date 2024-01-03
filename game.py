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


class ScrabbleGame:
    """
    Class ScrabbleGame
    Manages game, including game windows and clicks
    """

    def __init__(self):
        pygame.init()
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT + 2 * EXTRA_SPACE))
        pygame.display.set_caption("SCRABBLE")
        pygame.font.init()

    def start_win(self):
        """
        Function that handles starting window of a game
        """
        self.WIN.fill(CENTRAL_COLOR)

        # data including texts that are shown on the board
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

        # printing text
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
        """
        Window in which the player can enter their name.
        In case of not doing it, the automatic name is 'Player'.
        """
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

        # data that containes texts shown on the screen
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

        # printing texts on screen
        for data in text_data:
            font = pygame.font.Font("fonts/rubikname.ttf", SQUARE_SIZE // 2)
            text = font.render(data["text"], True, WHITE)
            text_rect = text.get_rect(center=data["coord"])
            self.WIN.blit(text, text_rect)

        active = False
        run = True

        """
        Part of the code that manages filling the name
        field.
        """
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

                # player can only enter their name if the square is active
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE and active:
                        user_text = user_text[:-1]

                    if event.key == pygame.K_RETURN:
                        player_name = user_text
                        run = False

                    elif active:
                        user_text += event.unicode

            # if the player write a name containing 10 symbols, the game starts
            if len(user_text) == 10:
                player_name = user_text
                run = False

            # if clicked the square is grey, else white
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
        """
        Function that handles main game
        """
        self.WIN.fill(DUN)

        # Variable that defines if the game is active
        run = True

        # Defining clock (FPS)
        clock = pygame.time.Clock()

        # Rack and board sprite that store tiles
        board_sprite = pygame.sprite.Group()
        rack_sprite = pygame.sprite.Group()

        # list that stores current mouse clicks
        current_click = []

        # classes used in game
        player = Player(player_name)
        bot = Bot()
        board = Board()

        board.create_board()

        player.updating_rack(board)
        board.draw_rack(player.rack(), rack_sprite)

        bot.updating_rack(board)


        # score of a player and bot
        player_score = 0
        bot_score = 0

        # Skip and round counter
        skip_count = 0
        round = 1

        with open("slowa.txt", "r", encoding="utf-8") as file:
            content = file.read()
            words = content.split()

        while run:
            clock.tick(60)

            for event in pygame.event.get():
                # Closes interactive window
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        # Aborts game running; shows score
                        self.end(player_name, player_score, bot_score)
                        run = False

                    if event.key == pygame.K_r:
                        # Replaces rack, only if it wasn't used (bot turn)
                        if player.is_rack_used() is False:
                            rack_sprite.empty()
                            player.replace_rack(board)
                            bot.bot_turn(board, board_sprite, words)
                            bot.updating_rack(board)
                            board.draw_rack(player.rack(), rack_sprite)
                            round += 1

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        # Skips round; if count == 2: end of the game
                        skip_count += 1
                        board.not_valid_action(board_sprite, player)
                        bot.bot_turn(board, board_sprite, words)
                        bot.updating_rack(board)
                        board.draw_rack(player.rack(), rack_sprite)
                        round += 1
                        if skip_count == 2 or bot.empty_rack():
                            self.end(player_name, player_score, bot_score)
                            run = False

                    else:
                        skip_count = 0

                # Checks if we pushed mousebuttons, manages moving tiles
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    x, y = position
                    row, col = board.coord_to_row_col(position)
                    current_click.append((row, col))
                    count = len(current_click)
                    if (
                        (count == 1 and ((current_click[0][0] != 16)))
                        or (count == 1 and (current_click[0][1] > 10))
                        or (count == 1 and (current_click[0][1] < 4))
                        or (
                            count == 1
                            and (player.rack()[current_click[0][1] - 4] == "")
                        )
                        or (count == 2 and (current_click[1][0] > 14))
                        or (
                            count == 2
                            and (
                                board.colid(
                                    board_sprite,
                                    current_click,
                                )
                            )
                        )
                    ):
                        current_click.clear()
                    if len(current_click) == 2:
                        rack_row, rack_col = current_click[0]
                        letter_row, letter_col = current_click[1]
                        letter_x, letter_y = board.row_col_to_coord(
                            letter_row,
                            letter_col,
                        )

                        # If the player clicks on an empty space in rack
                        if player.rack()[rack_col - 4] == "":
                            current_click.clear()
                            break

                        # Gets info about letter tile; moves it
                        letter_title = Tile(
                            player.rack()[rack_col - 4], (letter_x, letter_y)
                        )

                        letter_row, letter_col = board.coord_to_row_col((x, y))

                        board.current_word_update((letter_row, letter_col), letter_title.letter())
                        rack_sprite.empty()
                        board_sprite.add(letter_title)

                        # Rack updating

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
                        current_click.clear()

                # If enter the word is checked and then bot turn
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and board.current_word:
                        if len(board.word_list) == 0:
                            if not any(key == (7, 7) for key in board.current_word.keys()):
                                board.not_valid_action(
                                    board_sprite,
                                    player,
                                )
                                board.current_word_empty()
                        else:
                            if len(board.current_word.values()) < 2:
                                for pos in board.current_word:
                                    if board.alone_tile(pos):
                                        print('removing here')
                                        board.not_valid_action(
                                            board_sprite, player
                                        )
                                        board.current_word_empty()
                                    else:
                                        continue
                            else:
                                row_key = [item[0] for item in board.current_word.keys()]
                                col_key = [item[1] for item in board.current_word.keys()]
                                if board.sort_current_word() and board.valid_added_word(
                                        row_key, col_key
                                    ):
                                    pass
                                else:
                                    print('row_key itd')
                                    print(board.current_word)
                                    board.not_valid_action(
                                            board_sprite,
                                            player,
                                        )
                                    board.current_word_empty()

                        print(board.current_word)
                        board.update_board()
                        board.validation(
                            board_sprite,
                            words,
                            player,
                        )

                        print(board.word_list)
                        if board.word_list and len(board.current_word) > 1:
                            if len(board.word_list[-1]) > len(board.current_word.values()):
                                previous_coord = board.addword()
                                prev_word = ""
                                print(board.word_info_position())
                                if board.word_info_position() == "vertical":
                                    coords = previous_coord[0]
                                    col = previous_coord[1]
                                    print(coords, col)
                                    for row in range(coords[0], coords[1]):
                                        prev_word += board.board[row][col]
                                else:
                                    coords = previous_coord[1]
                                    row = previous_coord[0]
                                    print(coords)
                                    for col in range(coords[0], coords[1]):
                                        prev_word += board.board[row][col]

                                    if prev_word in board.word_list:
                                        board.word_list.remove(prev_word)

                        board.current_word_empty()

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

                    print(board.word_list)

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

    def click_handling(self):
        pass

    def update_on_screen(self):
        pass