import pygame
from constants import SQUARE_SIZE, WHITE, BLACK


class Tile(pygame.sprite.Sprite):
    """
    Class Tile
    Describes tile objects

    :param letter: holds a symbol of the tile
    :type letter: string

    :param position: holds a position of the tile
    :type position: int
    """

    def __init__(self, letter, position):
        super().__init__()

        self._letter = letter
        self._position = position

        self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        self.image.fill(WHITE)
        pygame.draw.rect(self.image, BLACK, self.image.get_rect(), 1)

        font = pygame.font.Font(None, 50)
        text = font.render(str(letter), True, BLACK)
        text_rect = text.get_rect(center=self.image.get_rect().center)
        self.image.blit(text, text_rect)

        self.rect = self.image.get_rect(topleft=position)

    def letter(self):
        return self._letter

    def position(self):
        return self._position
