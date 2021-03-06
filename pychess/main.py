from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'true'

import pygame

from . import init, handle, render, board
from .messages import messages_handle


def main() -> None:
    screen = init()
    running = True

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif board.state == board.State.playing:
                handle(screen, event)
            else:
                messages_handle(event)
        render(screen)

        clock.tick(60)

    pygame.quit()