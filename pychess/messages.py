import pygame
from pygame import gfxdraw
from copy import copy

from .variables import window_padding, cell_size, board

win_text, win_rect = None, pygame.Rect((0, 0, 0, 0))
lose_text, lose_rect = None, pygame.Rect((0, 0, 0, 0))
draw_text, draw_rect = None, pygame.Rect((0, 0, 0, 0))
play_again_text, play_again_rect = None, pygame.Rect((0, 0, 0, 0))

mouse_clicked = False


def messages_handle(event: pygame.event):
    global mouse_clicked
    mouse_clicked = event.type == pygame.MOUSEBUTTONDOWN


def in_rect(x: int, y: int, rect: pygame.Rect):
    return rect.y < y < rect.y + rect.h and rect.x < x < rect.x + rect.w


def draw_play_again_button(screen: pygame.display):
    text_rect_shadow = copy(play_again_rect)
    text_rect_shadow.w += 10
    text_rect_shadow.h += 10
    text_rect_shadow.x -= 5
    text_rect_shadow.y -= 5

    mouse_x, mouse_y = pygame.mouse.get_pos()
    if in_rect(mouse_x, mouse_y, text_rect_shadow):
        gfxdraw.box(screen, text_rect_shadow, (0, 0, 0, 120))
        if mouse_clicked:
            board.state = board.State.initializing
    else:
        gfxdraw.box(screen, text_rect_shadow, (0, 0, 0, 80))

    screen.blit(play_again_text, play_again_rect)


def messages_init() -> None:
    pygame.font.init()
    font = pygame.font.Font('freesansbold.ttf', 50)

    global win_text, win_rect
    win_text = font.render('You Won!', True, (11, 218, 81))
    win_rect = win_text.get_rect()
    win_rect.center = window_padding + cell_size * 4, window_padding + cell_size * 4
    win_rect.y -= 60

    global lose_text, lose_rect
    lose_text = font.render('You Lost!', True, (184, 15, 10))
    lose_rect = lose_text.get_rect()
    lose_rect.center = window_padding + cell_size * 4, window_padding + cell_size * 4
    lose_rect.y -= 60

    global draw_text, draw_rect
    draw_text = font.render('Game Draw!', True, (220, 220, 0))
    draw_rect = draw_text.get_rect()
    draw_rect.center = window_padding + cell_size * 4, window_padding + cell_size * 4
    draw_rect.y -= 60

    global play_again_text, play_again_rect
    font = pygame.font.Font('freesansbold.ttf', 30)

    play_again_text = font.render('Play again', True, (200, 200, 200))
    play_again_rect = play_again_text.get_rect()
    play_again_rect.center = window_padding + cell_size * 4, window_padding + cell_size * 4
    play_again_rect.y += 100


def display_game_draw(screen: pygame.display) -> None:
    text_rect_shadow = copy(draw_rect)
    text_rect_shadow.w += 20
    text_rect_shadow.h += 20
    text_rect_shadow.x -= 10
    text_rect_shadow.y -= 10
    gfxdraw.box(screen, text_rect_shadow, (0, 0, 0, 120))
    screen.blit(draw_text, draw_rect)
    draw_play_again_button(screen)


def display_lost(screen: pygame.display) -> None:
    text_rect_shadow = copy(lose_rect)
    text_rect_shadow.w += 20
    text_rect_shadow.h += 20
    text_rect_shadow.x -= 10
    text_rect_shadow.y -= 10
    gfxdraw.box(screen, text_rect_shadow, (0, 0, 0, 120))
    screen.blit(lose_text, lose_rect)
    draw_play_again_button(screen)


def display_won(screen: pygame.display) -> None:
    text_rect_shadow = copy(win_rect)
    text_rect_shadow.w += 20
    text_rect_shadow.h += 20
    text_rect_shadow.x -= 10
    text_rect_shadow.y -= 10
    gfxdraw.box(screen, text_rect_shadow, (0, 0, 0, 120))
    screen.blit(win_text, win_rect)
    draw_play_again_button(screen)
