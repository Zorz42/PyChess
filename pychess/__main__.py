import pygame

from . import init, handle, render, board


def main():
    screen = init()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif board.active:
                handle(screen, event)
        render(screen)
    pygame.quit()


if __name__ == '__main__':
    main()
