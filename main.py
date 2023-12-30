import pygame
import sys
from game import game, name_win, start_win


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
                    player_name = name_win()
                    name = player_name if player_name != "" else "Player"
                    run = game(name)
        if run:
            start_win()
    pygame.quit()
    sys.exit()


main()
