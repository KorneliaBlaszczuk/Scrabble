import pygame


"""
Wielkość okna gry zależna jest od sprzętu gracza.
Poniżej pobrane zostają potrzebne informacje.
"""
pygame.init()
display_info = pygame.display.Info()


"""
Zdefiniowane wymiary BOARD, w tym liczba kolumn i rzędów
tr_width, tr_height to zmnienne określające pewny wymiar
okna względem systemu. Z racji, że interesuje nas jedynie
liczba zmienno przecinkowa, są one jedynie pomocnicze.
Wykorzystujemy je następniew w obliczeniu wartości HEIGHT
i WIDTH.
"""

ROWS, COLS = 15, 15
tr_width = int(display_info.current_w * 0.8 // 2)
tr_height = int(display_info.current_w * 0.8 // 2)
WIDTH = int(tr_width // COLS) * COLS
HEIGHT = int(tr_height // ROWS) * ROWS
SQUARE_SIZE = WIDTH // COLS
EXTRA_SPACE = int(display_info.current_h * 0.1)
EXTRA_SQUARES = 7


"""Zdeyfiniowane kolory"""

DUN = (206, 195, 184)
WHITE = (255, 255, 255)
BEAVER = (169, 146, 125)
CINEREOUS = (138, 113, 106)
BLACK = (0, 0, 0)


extra_space_y = HEIGHT
extra_space_x = WIDTH // 2 - (EXTRA_SQUARES * SQUARE_SIZE) // 2
