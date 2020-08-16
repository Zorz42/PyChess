import pygame
from . import init, handle, render


def main():
    screen = init()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                handle(event)
        render(screen)
    pygame.quit()


if __name__ == '__main__':
    main()
