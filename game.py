import pygame
import sys
from constants import (
    EXTRA_SPACE,
    WIDTH,
    HEIGHT,
    extra_space_x,
    extra_space_y,
    SQUARE_SIZE,
    EXTRA_SQUARES,
    COLS,
    CENTRAL_COLOR,
    CINEREOUS,
    BEAVER,
    WHITE,
    DUN,
    rect_x,
    rect_y,
    rect_width,
    rect_height,
    ROWS,
)
from tiles import Tile
from player import Player
from bot import Bot
from move import Move
from board import Board
from letters_bag import LettersBag


class ScrabbleGame:
    """
    Class ScrabbleGame

    Manages game, including visual aspect of it

    :param WIN: game window
    :type WIN: pygame.Surface

    :param player: class Player
    :type player: class

    :param bot: class Bot
    :type bot: class

    :param board: class Board
    :type board: class

    :param move: class Move
    :type move: class

    :param letters_bag: class LettersBag
    :type letters_bag: class

    :param turn: shows whose turn it is
    :type turn: str

    :param round: number of current round
    :type round: int

    :param skip_count: shows how many times in a row
        the player skipped their round
    :type skip_count: int

    :param player_score: score of the player
    :type player_score: int

    :param bot_score: score of the bot
    :type bot_score: int
    """

    def __init__(self):
        pygame.init()
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT + 2 * EXTRA_SPACE))
        pygame.display.set_caption("SCRABBLE")
        pygame.font.init()

        self.player = Player()
        self.bot = Bot()
        self.board = Board()
        self.move = Move()
        self.letters_bag = LettersBag()

        self._turn = self.bot.name
        self._round = 1
        self._skip_count = 0

        self._player_score = 0
        self._bot_score = 0

    @property
    def turn(self):
        return self._turn

    @property
    def round(self):
        return self._round

    @property
    def skip_count(self):
        return self._skip_count

    @property
    def player_score(self):
        return self._player_score

    @property
    def bot_score(self):
        return self._bot_score

    def update_turn(self):
        """
        Updates whose turn it is
        """
        if self.turn == "Bot":
            self._turn = self.player.name
        else:
            self._turn = "Bot"
        return self._turn

    def update_round(self):
        """
        Updates round count
        """
        self._round += 1
        return self._round

    def update_skip_count(self):
        """
        Updates skip count
        """
        self._skip_count += 1
        return self._skip_count

    def empty_skip_count(self):
        """
        Empties skip count. Now it's equal to 0
        """
        self._skip_count = 0
        return self._skip_count

    def update_scores(self):
        """
        Updates players' scores
        """
        self._player_score = self.player.final_score(
            self.bot,
            self.letters_bag,
        )
        self._bot_score = self.bot.final_score(
            self.player,
            self.letters_bag,
        )
        return self._player_score, self._bot_score

    def draw_rack(self, rack, rack_sprite):
        """
        Draw tiles on the player's rack
        """
        x = extra_space_x
        y = (COLS + 1) * SQUARE_SIZE
        for current_letters in rack:
            if current_letters == "":
                x += SQUARE_SIZE
            else:
                letter_title = Tile(current_letters, (x, y))
                rack_sprite.add(letter_title)
                x += SQUARE_SIZE

    def draw_tiles(self, board_sprite, current_letter, position):
        """
        Draw tile on the board
        """
        row, col = position
        letter_tile = Tile(current_letter, self.board.row_col_to_coord(row, col))
        board_sprite.add(letter_tile)

    def draw_squares(self):
        """
        Manages a visual aspect of the board (draws it)
        """
        for row in range(ROWS):
            """
            Color depends on the row and column
            """
            for col in range(COLS):
                color = (
                    CENTRAL_COLOR
                    if row == col == 7
                    else (CINEREOUS if (row + col) % 2 == 0 else BEAVER)
                )
                pygame.draw.rect(
                    self.WIN,
                    color,
                    (
                        row * SQUARE_SIZE,
                        col * SQUARE_SIZE,
                        SQUARE_SIZE,
                        SQUARE_SIZE,
                    ),
                )

    def draw_rack_squares(self):
        """
        Draws a player's rack
        """
        for i in range(EXTRA_SQUARES):
            x = SQUARE_SIZE * 4 + i * SQUARE_SIZE
            y = (COLS + 1) * SQUARE_SIZE
            color = CINEREOUS if i % 2 == 0 else BEAVER
            pygame.draw.rect(self.WIN, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

    def draw_updated_rack(self, rack_sprite):
        x = extra_space_x
        y = (COLS + 1) * SQUARE_SIZE

        for current_letters in self.player.rack:
            if current_letters == "":
                x += SQUARE_SIZE
            else:
                letter = Tile(current_letters, (x, y))
                rack_sprite.add(letter)
                x += SQUARE_SIZE

        x = extra_space_x
        y = extra_space_y + EXTRA_SPACE // 2

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
                        if user_text:
                            self.player.update_name(user_text)
                        run = False

                    elif active and event.key != pygame.K_BACKSPACE:
                        user_text += event.unicode

            # if the player write a name containing 10 symbols, the game starts
            if len(user_text) == 10:
                if user_text:
                    self.player.update_name(user_text)
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

    def game(self):
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

        # To make the code shorter we used:
        player = self.player
        board = self.board
        bot = self.bot
        letters_bag = self.letters_bag
        move = self.move

        board.create_board()

        player.updating_rack(letters_bag)
        self.draw_rack(player.rack, rack_sprite)

        bot.updating_rack(letters_bag)

        with open("slowa.txt", "r", encoding="utf-8") as file:
            content = file.read()
            words = content.split()

        self.update_turn()

        while run:
            clock.tick(60)

            for event in pygame.event.get():
                # Closes interactive window
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        # Aborts game running; shows score
                        self.end()
                        run = False

                    if event.key == pygame.K_r:
                        # Replaces rack, only if it wasn't used (bot turn)
                        if player.is_rack_used() is False:
                            rack_sprite.empty()
                            player.replace_rack(letters_bag)

                            self.update_turn()
                            self.draw_info_box()
                            bot.bot_turn(
                                self,
                                board,
                                board_sprite,
                                words,
                                letters_bag,
                            )
                            bot.updating_rack(letters_bag)
                            self.update_turn()
                            self.draw_info_box()

                            self.draw_rack(player.rack, rack_sprite)
                            self.update_round()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        # Skips round; if count == 2: end of the game
                        self.update_skip_count()
                        board.not_valid_action(board_sprite, player)

                        self.update_turn()
                        self.draw_info_box()
                        bot.bot_turn(self, board, board_sprite, words, letters_bag)
                        bot.updating_rack(letters_bag)
                        self.update_turn()
                        self.draw_info_box()

                        self.draw_rack(player.rack, rack_sprite)
                        self.update_round()
                        if self.skip_count == 2 or bot.empty_rack():
                            self.end()
                            run = False

                    else:
                        self.empty_skip_count()

                # Checks if we pushed mousebuttons, manages moving tiles
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    x, y = position
                    row, col = board.coord_to_row_col(position)
                    move.update_click((row, col))
                    # manages mouse clicks
                    move.click_handling(player, board, board_sprite)

                    if len(move.click) == 2:
                        rack_row, rack_col = move.click[0]
                        letter_row, letter_col = move.click[1]
                        letter_x, letter_y = board.row_col_to_coord(
                            letter_row,
                            letter_col,
                        )

                        # If the player clicks on an empty space in rack
                        if player.rack[rack_col - 4] == "":
                            move.empty_click()
                            break

                        # Gets info about letter tile; moves it
                        letter_title = Tile(
                            player.rack[rack_col - 4], (letter_x, letter_y)
                        )

                        letter_row, letter_col = board.coord_to_row_col((x, y))

                        board.current_word_update(
                            (letter_row, letter_col), letter_title.letter
                        )
                        rack_sprite.empty()
                        board_sprite.add(letter_title)

                        # Rack updating (display)

                        player.rack[rack_col - 4] = ""

                        self.draw_updated_rack(rack_sprite)

                        move.empty_click()

                # If enter the word is checked and then bot turn
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and board.current_word:
                        # manages word placements
                        board.valid_placement(board_sprite, player)

                        board.update_board()
                        board.validation(
                            board_sprite,
                            words,
                            player,
                        )

                        board.current_word_empty()

                        self.win_update(rack_sprite, board_sprite)

                        self.update_turn()

                        self.draw_info_box()
                        bot.bot_turn(self, board, board_sprite, words, letters_bag)
                        bot.updating_rack(letters_bag)
                        self.update_turn()
                        self.draw_info_box()

                        player.updating_rack(letters_bag)
                        self.draw_rack(player.rack, rack_sprite)

                        self.update_round()

                        # after round the game checks if the terms for end
                        if player.empty_rack() or bot.empty_rack():
                            self.end()
                            run = False

                        else:
                            continue

            self.draw_info_box()
            self.win_update(rack_sprite, board_sprite)
            self.update_scores()

        return run

    def end(self):
        """
        Manages ending screen
        """
        self.WIN.fill(CENTRAL_COLOR)
        pygame.font.init()

        font = pygame.font.Font(None, 36)

        winner_name = self.player.name if self.player_score > self.bot_score else "Bot"

        text_info = [
            {
                "text": "THE END!",
                "font": SQUARE_SIZE,
                "coord": (WIDTH // 2, (HEIGHT // 2) + EXTRA_SPACE),
            },
            {
                "text": f"{self.player.name}'s score: {self.player_score}",
                "font": SQUARE_SIZE // 2,
                "coord": (WIDTH // 2, (HEIGHT // 2) + 2 * EXTRA_SPACE),
            },
            {
                "text": f"Bot score: {self.bot_score}",
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

    def draw_info_box(self):
        pygame.draw.rect(
            self.WIN,
            CENTRAL_COLOR,
            (rect_x, rect_y, rect_width, rect_height),
        )

        # prints round number
        current_text = f"Round {self.round}: {self.turn}"
        font = pygame.font.Font("fonts/rubikname.ttf", 30)
        text = font.render(current_text, True, WHITE)
        text_rect = text.get_rect(
            center=(WIDTH // 2, rect_y + rect_height // 2),
        )
        self.WIN.blit(text, text_rect)
        pygame.display.flip()

    def win_update(self, rack_sprite, board_sprite):
        self.draw_squares()
        self.draw_rack_squares()
        rack_sprite.update()
        rack_sprite.draw(self.WIN)
        board_sprite.update()
        board_sprite.draw(self.WIN)

        pygame.display.update()
