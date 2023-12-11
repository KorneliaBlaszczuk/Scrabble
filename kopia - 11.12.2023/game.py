import pygame
from board import Board
from constants import (
    EXTRA_SPACE,
    WIDTH,
    HEIGHT,
    extra_space_x,
    extra_space_y,
    SQUARE_SIZE,
    COLS,
)
from tiles import Tile
from player import Player, Bot


WIN = pygame.display.set_mode((WIDTH, HEIGHT + EXTRA_SPACE))
pygame.display.set_caption("SCRABBLE")
pygame.font.init()


def draw_handler(board, handler, handler_sprite):
    current_handler = board.updating_handler(handler)
    x = extra_space_x
    y = (COLS + 1) * SQUARE_SIZE
    for current_letters in current_handler:
        letter_title = Tile(current_letters, (x, y))
        handler_sprite.add(letter_title)
        x += SQUARE_SIZE


def main():
    """Zmienna definiująca, czy gra jest aktywna, działa w danym momencie"""
    run = True
    """Definujemy zegar, który kontroluje nam liczbę FPS"""
    clock = pygame.time.Clock()
    board_sprite = pygame.sprite.Group()
    handler_sprite = pygame.sprite.Group()
    currentword_sprite = pygame.sprite.Group()

    current_next_pos = []

    player = Player("Gracz")
    bot = Bot("Bot")

    board = Board()
    board.create_board()
    board.updating_handler(player.handler())
    board.draw_handler(player.handler(), handler_sprite)
    current_word = {}
    skip_count = 0

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
                if event.key == pygame.K_r:
                    handler_sprite.empty()
                    board.replace_handler(player.handler())
                    # kolejka bota
                    board.draw_handler(player.handler(), handler_sprite)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    skip_count += 1
                    pass

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
                        count == 1
                        and (player.handler()[current_next_pos[0][1] - 4] == "")
                    )
                    or (count == 2 and (current_next_pos[1][0] > 14))
                    or (count == 2 and (board.colid(board_sprite, current_next_pos)))
                ):
                    current_next_pos.clear()
                    count = 0
                if len(current_next_pos) == 2:
                    handler_row, handler_col = current_next_pos[0]
                    letter_row, letter_col = current_next_pos[1]
                    letter_x, letter_y = board.calc_coordinates(letter_row, letter_col)
                    handler_x, handler_y = board.calc_coordinates(
                        handler_row, handler_col
                    )

                    if player.handler()[handler_col - 4] == "":
                        current_next_pos.clear()
                        break
                    else:
                        pass
                    # kiedy gracz kliknie na plansze jako pierwsze

                    letter_title = Tile(
                        player.handler()[handler_col - 4], (letter_x, letter_y)
                    )

                    letter_row, letter_col = board.get_row_col_from_mouse((x, y))

                    current_word[(letter_row, letter_col)] = letter_title.letter()
                    handler_sprite.empty()
                    board_sprite.add(letter_title)

                    """
                    Aktualizacja handlera
                    """

                    player.handler()[handler_col - 4] = ""

                    x = extra_space_x
                    y = (COLS + 1) * SQUARE_SIZE

                    for current_letters in player.handler():
                        if current_letters == "":
                            x += SQUARE_SIZE
                        else:
                            letter = Tile(current_letters, (x, y))
                            handler_sprite.add(letter)
                            x += SQUARE_SIZE
                    x = extra_space_x
                    y = extra_space_y + EXTRA_SPACE // 2
                    current_next_pos.clear()

            """Kiedy nacisneliśmy ENTER słowo dodawane jest do listy,
            a w handlerze uzupełniane są puste pola"""
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(current_word.values()) < 2:
                        for pos in current_word:
                            if board.alone_tile(board.board, pos):
                                board.not_valid(board_sprite, current_word, player)
                                current_word = {}
                            else:
                                continue
                    else:
                        row_key = [item[0] for item in current_word.keys()]
                        col_key = [item[1] for item in current_word.keys()]
                        if all(x == row_key[0] for x in row_key):
                            current_word = dict(
                                sorted(
                                    current_word.items(), key=lambda item: item[0][0]
                                )
                            )
                        elif all(x == col_key[1] for x in col_key):
                            current_word = dict(
                                sorted(
                                    current_word.items(), key=lambda item: item[0][1]
                                )
                            )
                        else:
                            board.not_valid(board_sprite, current_word, player)
                            current_word = {}
                    board.update_board(current_word)
                    if board.word_checking(board.board, words):
                        board.word_list_adding(board.board, player)
                    else:
                        board.not_valid(board_sprite, current_word, player)
                        board.remove_from_board(current_word)
                    current_word = {}
                    board.updating_handler(player.handler())
                    board.draw_handler(player.handler(), handler_sprite)
                    if player.empty_handler(player.handler()):
                        run = False
                    else:
                        continue

        board.draw_squares(WIN)
        board.draw_extra_squares(WIN)
        handler_sprite.update()
        handler_sprite.draw(WIN)
        board_sprite.update()
        board_sprite.draw(WIN)
        currentword_sprite.update()
        currentword_sprite.draw(WIN)
        pygame.display.update()

    print(player.final_score(player.handler(), bot))
    pygame.quit()


main()
