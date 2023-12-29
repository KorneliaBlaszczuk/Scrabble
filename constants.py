import pygame


"""
Size of the game window depends on the player's computer.
Below, the needed information are taken.
"""
pygame.init()
display_info = pygame.display.Info()


"""
Defined board size (number of row and columns).
tr_width, tr_height are variables describbing certain window
size depending on system. There are supplementary because we are
interested only in floating point number.
We used them when calculating HEIGHT and WIDTH
"""

ROWS, COLS = 15, 15
tr_width = int(display_info.current_w * 0.8 // 2)
tr_height = int(display_info.current_w * 0.8 // 2)
WIDTH = int(tr_width // COLS) * COLS
HEIGHT = int(tr_height // ROWS) * ROWS
SQUARE_SIZE = WIDTH // COLS
EXTRA_SPACE = int(display_info.current_h * 0.1)
EXTRA_SQUARES = 7

"""
Defined box sizes
"""
rect_width = WIDTH // 4
rect_height = SQUARE_SIZE
rect_x = WIDTH // 2 - rect_width // 2
rect_y = (HEIGHT // 2) + 5 * EXTRA_SPACE

"""Defined colours"""

DUN = (206, 195, 184)
WHITE = (255, 255, 255)
BEAVER = (169, 140, 125)
CINEREOUS = (150, 100, 106)
BLACK = (0, 0, 0)
CENTRAL_COLOR = (100, 50, 60)


extra_space_y = HEIGHT
extra_space_x = WIDTH // 2 - (EXTRA_SQUARES * SQUARE_SIZE) // 2
