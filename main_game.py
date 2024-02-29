import pygame
from sys import exit
from new_game import consts
from new_game import Drawing


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((consts.SCREEN_WIDTH, consts.SCREEN_HEIGHT))
    pygame.display.set_caption(consts.GAME_TITLE)
    clock = pygame.time.Clock()

    draw_object = Drawing()

    screen.blit(draw_object.background, (0, 0))
    screen.blit(draw_object.stats_panel, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        draw_object.refresh_on_screen(screen)

        pygame.display.update()
        clock.tick(consts.FRAME_RATE)


if __name__ == '__main__':
    run_game()
