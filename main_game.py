import pygame
from new_game import consts
from new_game import Drawing
from new_game import GameCrl


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((consts.SCREEN_WIDTH, consts.SCREEN_HEIGHT))
    pygame.display.set_caption(consts.GAME_TITLE)
    clock = pygame.time.Clock()

    draw_object = Drawing()
    game_control = GameCrl()

    while True:
        if consts.GAME_MODE == consts.GameMode.NORMAL.value:
            # count all
            game_control.normal_loop_body()
            # draw all
            if not game_control.game.is_game_over():
                draw_object.draw_statics(screen)
                draw_object.refresh_on_screen(screen)
            else:
                draw_object.draw_intro(screen)
            # control environ
            clock.tick(consts.FRAME_RATE)
        else:
            game_control.api_loop_body()

        pygame.display.update()


if __name__ == '__main__':
    run_game()
