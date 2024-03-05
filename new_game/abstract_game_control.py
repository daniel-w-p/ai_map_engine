import pygame
from sys import exit
from .game import Game
from .consts import GAME_MODE, GameMode

from enum import Enum


class GameAction(Enum):
    QUIT = -2
    PAUSE = -1
    NO_MOVE = 0
    RUN_LEFT = 1
    RUN_RIGHT = 2
    JUMP = 3


class AbstractGameControl:
    def __init__(self):
        self._game = Game()

    @property
    def game(self):
        return self._game

    def get_action_from_ai(self):
        return 0

    def game_step(self):
        self._game.game_step()

    def execute_action(self, api_action):
        if api_action == GameAction.QUIT.value:
            pygame.quit()
            exit()
        if api_action == GameAction.JUMP.value:
            self._game.player_jump()
        if api_action == GameAction.PAUSE.value:
            self._game.pause_game()
        # TODO MORE ACTION

    def game_action_api(self, action):
        # Make actions
        self.execute_action(action)

        state = self._game.game_state

        reward = self._game.reward

        done = self._game.is_game_over

        return state, reward, done

    def game_action_normal(self, action):
        # Make actions
        self.execute_action(action)

    def normal_loop_body(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.game_action_normal(GameAction.QUIT.value)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.game_action_normal(GameAction.JUMP.value)
                if event.key == pygame.K_SPACE:
                    if self._game.is_game_over():
                        self._game.reset_game()
                    else:
                        self._game.pause_game()

            self._game.game_events(event)

        self.game_step()

    def api_loop_body(self):
        action = self.get_action_from_ai()
        state, reward, done = self.game_action_api(action)

        if GAME_MODE == GameMode.API_PLAY:
            for event in pygame.event.get():
                self._game.game_events(event)

        if done:
            self.execute_action(GameAction.QUIT.value)
        self.game_step()
