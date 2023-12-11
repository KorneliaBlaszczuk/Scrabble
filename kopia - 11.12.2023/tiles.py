from letters_bag import blank_list
import pygame
from constants import SQUARE_SIZE, WHITE, BLACK

correct_words = open("slowa.txt", "r")

word_list = []


class Tile(pygame.sprite.Sprite):
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

    def set_position(self, new_position):
        self._position = new_position
        return self._position

    def delete(self):
        self.kill()

    def blank_tile_word(self, letter, word):
        """
        Za płykę blank podstawiamy po kolei możliwe litery z blank_list.
        Sprawdzamy zgodność kolejnych kombinacji słów,
        aż do momentu znalezienia pierwszej poprawnej.
        Do listy słów utworzonych przez gracza dopisujemy daną kombinacji,
        z uwzględnieniem płytki BLANK.
        """
        if letter == " ":
            for let in blank_list:
                word.replace(letter, let)
                if word in correct_words:
                    word.replace(let, " ")
                    word_list.append(word)
                    break
                else:
                    word.replace(let, " ")

    def calculate_coordinates(self):
        x = (self.row) * SQUARE_SIZE + SQUARE_SIZE // 2
        y = (self.col) * SQUARE_SIZE + SQUARE_SIZE // 2
        return (x, y)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calculate_coordinates()
        # Napisać funkcję, która zmienia położenia płytki w pygame
