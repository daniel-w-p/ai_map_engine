import pygame.time
from enum import Enum

from new_game.map_decoder import MapDecoder
from new_game.figures import Player
from new_game.figures import Wood
from .consts import SCREEN_WIDTH


class GameState(Enum):
    END = 0
    RUN = 1
    PAUSE = 2


class Game:
    def __init__(self):
        self._player = Player()
        self._obstacles = []
        self._environs = []
        self._rewards = []
        self._map = 0
        self._level = 0
        self._score = 0
        self._distance = 0
        self._high_score = 0
        self._game_state = GameState.END.value
        self._environment_state = None
        self._play_time_start = pygame.time.get_ticks()
        self._map_decoder = MapDecoder()

        self._actual_left = 0
        self._actual_right = SCREEN_WIDTH
        self._screen_margin = SCREEN_WIDTH / 2

        self.obstacles_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacles_event, 500)

    def reset_game(self):
        self._map = 0
        self._level = 0
        self._score = 0
        self._distance = 0
        self._game_state = GameState.RUN.value
        self._environment_state = None

        self._actual_left = 0
        self._actual_right = SCREEN_WIDTH
        self._screen_margin = SCREEN_WIDTH / 2

        self._play_time_start = pygame.time.get_ticks()
        self.init_map()

    def init_map(self):
        self._map_decoder.prepare_map()
        for k, v in self._map_decoder.elements_dictionary.items():
            w, h = k
            if self._actual_left - self._screen_margin < w < self._actual_right + self._screen_margin:
                if v in self._map_decoder.particles_dictionary:
                    if self._map_decoder.particles_dictionary[v].value < 3:
                        wood = Wood()

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

    def game_events(self, event):
        if event.type == self.obstacles_event:
            for obstacle in self._obstacles:
                obstacle.update_animation()

    def game_step(self):
        if not self._player.alive:
            self._game_state = GameState.END.value

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
