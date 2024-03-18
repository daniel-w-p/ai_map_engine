import pygame
from new_game import config
from new_game import GameCrl


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption(config.GAME_TITLE)
    clock = pygame.time.Clock()

    game_control = GameCrl()
    background = game_control.back

    while True:
        if config.GAME_MODE == config.GameMode.NORMAL.value:
            # count all
            game_control.normal_loop_body()
            # draw all
            if game_control.game.is_game_running():
                background.draw_statics(screen)
                background.refresh_on_screen(screen)
                game_control.game.draw_stage(screen)
            else:
                background.draw_intro(screen)
            # control environ
            clock.tick(config.FRAME_RATE)
        else:
            game_control.api_loop_body()

        pygame.display.update()


if __name__ == '__main__':
    run_game()
