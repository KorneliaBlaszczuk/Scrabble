import pygame
import sys
from game import ScrabbleGame


def main():
    game = ScrabbleGame()
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_name = game.name_win()
                    name = player_name if player_name != "" else "Player"
                    run = game.game(name)
        if run:
            game.start_win()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
