import pygame.time
from .player import Player
from enum import Enum


class GameState(Enum):
    END = 0
    RUN = 1
    PAUSE = 2


class Game:
    def __init__(self):
        self._player = Player()
        self._map = 0
        self._level = 0
        self._score = 0
        self._distance = 0
        self._high_score = 0
        self._game_state = GameState.END.value
        self._environment_state = None
        self._play_time_start = pygame.time.get_ticks()

    def reset_game(self):
        self._map = 0
        self._level = 0
        self._score = 0
        self._distance = 0
        self._game_state = GameState.RUN.value
        self._environment_state = None
        self._play_time_start = pygame.time.get_ticks()

    def pause_game(self):
        if self._game_state == GameState.PAUSE.value:
            self._game_state = GameState.RUN.value
        else:
            self._game_state = GameState.PAUSE.value

    def player_jump(self):
        self._player.jump()

    def player_left(self):
        self._player.move(False)

    def player_right(self):
        self._player.move(True)

    def game_step(self):
        pass

    def update_environment_state(self):
        pass

    def calculate_reward(self):
        scale_distance_param = 0.2
        scale_time_param = 0.002
        play_time = pygame.time.get_ticks() - self._play_time_start
        #  minus here on the elapsed time should make AI to move
        return self._score + scale_distance_param * self._distance - scale_time_param * play_time

    @property
    def game_state(self):
        return self._game_state

    @property
    def environment_state(self):
        self.update_environment_state()
        return self._environment_state

    @property
    def reward(self):
        reward = self.calculate_reward()
        return reward

    def is_game_over(self):
        return self._game_state == GameState.END.value

    def is_game_paused(self):
        return self._game_state == GameState.PAUSE.value
