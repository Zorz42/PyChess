import pygame

board = []


def init():
    pass


def handle(event):
    # Handle event(s)
    pass


def render(screen):
    # Render to screen?
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
    pygame.display.flip()
