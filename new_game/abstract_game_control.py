import pygame
from sys import exit
from .game import Game
from setup import ProjectSetup, GameMode
from .game_background import GameBackground

from enum import Enum


class GameAction(Enum):
    QUIT = -2
    PAUSE = -1
    NO_ACTION = 0
    STOP_MOVE = 1
    RUN_LEFT = 2
    RUN_RIGHT = 3
    JUMP = 4


class AbstractGameControl:
    def __init__(self):
        if ProjectSetup.MODES["play_mode"] != GameMode.API_LEARN.value:
            self._background = GameBackground()  # background not related with map
        else:
            self._background = None
        self._game = Game(self._background)
        self._action = GameAction.NO_ACTION
        self._done = False

    @staticmethod
    def action_space_size():
        return len(GameAction) - 2  # NO_ACTION = 0 STOP_MOVE = 1 RUN_LEFT = 2 RUN_RIGHT = 3 JUMP = 4

    @property
    def game(self):
        return self._game

    @property
    def back(self):
        return self._background

    @property
    def reward(self):
        reward = self.calculate_reward()
        return reward

    def calculate_reward(self):
        return self._game.life_score + self._game.points_score

    def action_from_ai(self, action):
        self._action = action

    def execute_action(self, api_action):
        if api_action == GameAction.QUIT.value:
            pygame.quit()
            exit()
        if api_action == GameAction.JUMP.value:
            self._game.player_jump()
        if api_action == GameAction.RUN_LEFT.value:
            self._game.player_left()
        if api_action == GameAction.RUN_RIGHT.value:
            self._game.player_right()
        if api_action == GameAction.STOP_MOVE.value:
            self._game.player_retard()
        if api_action == GameAction.PAUSE.value:
            self._game.pause_game()

    def game_action_api(self, action):
        # Make actions
        self.execute_action(action)

        env_state, plr_state = self._game.environment_state

        reward = self.reward

        self._done = self._game.game_state

        return env_state, plr_state, reward, self._done

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
                if event.key == pygame.K_a:
                    self.game_action_normal(GameAction.RUN_LEFT.value)
                if event.key == pygame.K_d:
                    self.game_action_normal(GameAction.RUN_RIGHT.value)
                if event.key == pygame.K_SPACE:
                    if self._game.is_game_over():
                        self._game.reset_game()
                    else:
                        self._game.pause_game()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    self.game_action_normal(GameAction.STOP_MOVE.value)

            self._game.game_events(event)
        if self._game.is_game_running():
            self._game.game_step()

    def api_loop_body(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.game_action_normal(GameAction.QUIT.value)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self._game.is_game_over():
                        self._game.reset_game()
                    else:
                        self._game.pause_game()

            self._game.game_events(event)

        if self._done:
            self.execute_action(GameAction.QUIT.value)
        if self._game.is_game_running():
            self._game.game_step()

