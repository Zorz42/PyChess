import pygame
from pychess import init, handle, render


def main():
    init()

    pygame.init()
    pygame.display.set_caption('PyChess')

    screen = pygame.display.set_mode((500, 500))
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
