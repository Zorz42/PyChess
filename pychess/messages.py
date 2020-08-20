import pygame

from .variables import window_padding, cell_size

win_text, win_text_rect = None, None
lose_text, lose_text_rect = None, None
draw_text, draw_text_rect = None, None


def messages_init() -> None:
    global win_text, win_text_rect, lose_text, lose_text_rect, draw_text, draw_text_rect
    pygame.font.init()
    font = pygame.font.Font('freesansbold.ttf', 50)
    win_text = font.render('You Won!', True, (11, 218, 81))
    win_text_rect = win_text.get_rect()
    win_text_rect.center = window_padding + cell_size * 4, window_padding + cell_size * 4

    lose_text = font.render('You Lost!', True, (184, 15, 10))
    lose_text_rect = lose_text.get_rect()
    lose_text_rect.center = window_padding + cell_size * 4, window_padding + cell_size * 4

    draw_text = font.render('Game Draw!', True, (220, 220, 0))
    draw_text_rect = draw_text.get_rect()
    draw_text_rect.center = window_padding + cell_size * 4, window_padding + cell_size * 4


def display_game_draw(screen: pygame.display) -> None:
    screen.blit(draw_text, draw_text_rect)


def display_lost(screen: pygame.display) -> None:
    screen.blit(lose_text, lose_text_rect)


def display_won(screen: pygame.display) -> None:
    screen.blit(win_text, win_text_rect)
