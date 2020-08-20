from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'true'

import pygame

from . import init, handle, render, board


def main() -> None:
    screen = init()
    running = True

    frame_count: int = 0
    seconds: int = 0

    clock = pygame.time.Clock()

    while running:
        frame_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif board.state == board.State.playing:
                handle(screen, event)
        render(screen)

        if int(pygame.time.get_ticks() / 1000) != seconds:
            seconds = int(pygame.time.get_ticks() / 1000)
            # print(f"FPS: {frame_count}")
            frame_count = 0

        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
