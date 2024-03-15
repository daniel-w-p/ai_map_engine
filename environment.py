import pygame
from new_game import consts
from new_game import GameCrl


class Environment:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(consts.GAME_TITLE)

        self.screen = pygame.display.set_mode((consts.SCREEN_WIDTH, consts.SCREEN_HEIGHT))
        self.game_control = GameCrl()

    def step(self, action):
        state, reward, done = self.game_control.game_action_api(action)
        self.game_control.game.game_step()
        pygame.display.update()
        return state, reward, done

    def reset(self):
        self.game_control.game.reset_game()
        return self.game_control.game.game_state
