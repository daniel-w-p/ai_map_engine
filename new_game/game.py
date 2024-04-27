import pygame.time
import numpy as np
from enum import Enum

from new_game.map_decoder import MapDecoder, GameParticles
from new_game.figures import ImagePart, Wood, Cloud, Pear, Apple, Water, Fire, Meteor, Player
from .config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_SIDE_MARGIN, MINIMAP_ONE_PIXEL, TimeEvents
from .game_background import GameBackground

from setup import ProjectSetup, GameMode


class GameState(Enum):
    END = 0
    RUN = 1
    PAUSE = 2
    FINISH = 3


class RewardPoints(Enum):
    APPLE = 1
    PEAR = 3
    WATER = 7


class Game:
    def __init__(self, background: GameBackground = None):
        if ProjectSetup.MODES["play_mode"] == GameMode.API_LEARN.value:
            print("Render is off")

        self._player = Player()
        self._obstacles = pygame.sprite.Group()
        self._environs = pygame.sprite.Group()
        self._rewards = pygame.sprite.Group()
        self._game_background = background  # part of the game not related with map
        self._map = 1
        self._level = 1
        self._score = 0
        self._distance = 0
        self._high_score = 0
        self._game_state = GameState.PAUSE.value
        self._environment_state = None
        self._play_time_start = pygame.time.get_ticks()
        self._map_decoder = MapDecoder()

        self._scroll_right = None
        self._actual_left = 0
        self._actual_right = SCREEN_WIDTH
        self._screen_margin = SCREEN_SIDE_MARGIN

        self.obstacles_event = pygame.USEREVENT + TimeEvents.OBSTACLE_EVENT.value
        pygame.time.set_timer(self.obstacles_event, 100)

        self.elapsed_event = pygame.USEREVENT + TimeEvents.ELAPSED_EVENT.value
        pygame.time.set_timer(self.elapsed_event, 500)

        if self._game_background is not None:
            self._game_background.set_player_life_text(str(self._player.life))

        self.init_map()
        self._player.reset()

    def reset_game(self):
        self._map = 0
        self._level = 0
        self._score = 0
        self._distance = 0
        self._game_state = GameState.RUN.value
        self._environment_state = None

        self._scroll_right = None
        self._actual_left = 0
        self._actual_right = SCREEN_WIDTH
        self._screen_margin = SCREEN_SIDE_MARGIN

        self._player.reset()
        self.set_map_init_content()

        self._play_time_start = pygame.time.get_ticks()
        if self._game_background is not None:
            self._game_background.set_player_life_text(str(self._player.life))

    @staticmethod
    def env_state_size():
        return SCREEN_HEIGHT // MINIMAP_ONE_PIXEL, SCREEN_WIDTH // MINIMAP_ONE_PIXEL, 1

    def set_map_part(self, width, height, kind):
        if kind.value < 3:
            wood = Wood(ImagePart(kind.value % 3))
            wood.rect.x = width
            wood.rect.y = height
            self._environs.add(wood)
        elif kind.value < 6:
            cloud = Cloud(ImagePart(kind.value % 3))
            cloud.rect.x = width
            cloud.rect.y = height
            self._environs.add(cloud)
        elif kind == GameParticles.PEAR:
            pear = Pear()
            pear.rect.x = width
            pear.rect.y = height
            self._rewards.add(pear)
        elif kind == GameParticles.APPLE:
            apple = Apple()
            apple.rect.x = width
            apple.rect.y = height
            self._rewards.add(apple)
        elif kind == GameParticles.WATER:
            water = Water()
            water.rect.x = width
            water.rect.y = height
            self._rewards.add(water)
        elif kind == GameParticles.FIRE:
            fire = Fire()
            fire.rect.x = width
            fire.rect.y = height
            self._obstacles.add(fire)
        elif kind == GameParticles.METEOR:
            meteor = Meteor()
            meteor.rect.x = width
            meteor.rect.y = height
            self._obstacles.add(meteor)
        elif kind == GameParticles.FINISH:
            fin = Wood(ImagePart(1))
            fin.rect.x = width
            fin.rect.y = height
            self._rewards.add(fin)

    def add_right_content(self):
        for k, v in self._map_decoder.elements_dictionary.items():
            w, h = k
            if self._actual_right <= w < self._actual_right + self._screen_margin:
                self.set_map_part(w - self._actual_left, h, v)

    def add_left_content(self):
        for k, v in self._map_decoder.elements_dictionary.items():
            w, h = k
            if self._actual_left - self._screen_margin < w <= self._actual_left:
                self.set_map_part(w - self._actual_left, h, v)

    def set_map_content(self):
        for k, v in self._map_decoder.elements_dictionary.items():
            w, h = k
            if self._actual_left - self._screen_margin < w < self._actual_right + self._screen_margin:
                self.set_map_part(w, h, v)

    def set_map_init_content(self):
        self._obstacles = pygame.sprite.Group()
        self._environs = pygame.sprite.Group()
        self._rewards = pygame.sprite.Group()
        self.set_map_content()

    def init_map(self):
        self._map_decoder.prepare_map()
        self.set_map_init_content()

    def draw_stage(self, screen):
        if ProjectSetup.MODES["play_mode"] != GameMode.API_LEARN.value:  # TODO ?? move from here to drawing ??
            self._environs.draw(screen)
            self._rewards.draw(screen)
            self._obstacles.draw(screen)
            self._player.draw(screen)

    def player_collisions(self):
        collisions_env = pygame.sprite.spritecollide(self._player, self._environs, False)
        collisions_rew = pygame.sprite.spritecollide(self._player, self._rewards, True)
        collisions_hurt = pygame.sprite.spritecollide(self._player, self._obstacles, False)

        if collisions_env:
            for environ in collisions_env:
                self._player.stop(
                    environ.rect.y <= self._player.rect.y + self._player.rect.height < environ.rect.y + environ.rect.height,
                    environ.rect.y - self._player.rect.height + 1)
        if collisions_hurt:
            for hurt in collisions_hurt:
                self._player.hurt(isinstance(hurt, Fire))
                if self._game_background is not None:
                    self._game_background.set_player_life_text(str(self._player.life))

        if collisions_rew:
            for reward in collisions_rew:
                if isinstance(reward, Apple):
                    self.add_reward(RewardPoints.APPLE.value)
                elif isinstance(reward, Pear):
                    self.add_reward(RewardPoints.PEAR.value)
                elif isinstance(reward, Water):
                    self.add_reward(RewardPoints.WATER.value)
                elif isinstance(reward, Wood):
                    self.add_reward(100)
                    self._game_state = GameState.FINISH.value

            if self._game_background is not None:
                self._game_background.set_game_score_text(str(self._score))

    def player_movement(self):
        if self._player.rect.y > SCREEN_HEIGHT:
            self._player.fall_out()
            if self._game_background is not None:
                self._game_background.set_player_life_text(str(self._player.life))

        if self._player.rect.x > SCREEN_WIDTH * 0.75 and self._actual_right < self._map_decoder.map_real_width and self._scroll_right is None:
            self._scroll_right = True
            self._player.scroll_screen(self._scroll_right)
            for env in self._environs:
                env.scroll_screen(self._scroll_right)
            for rew in self._rewards:
                rew.scroll_screen(self._scroll_right)
            for obs in self._obstacles:
                obs.scroll_screen(self._scroll_right)

        if self._player.rect.x < SCREEN_WIDTH * 0.25 and self._actual_left > 0 and self._scroll_right is None:
            self._scroll_right = False
            self._player.scroll_screen(self._scroll_right)
            for env in self._environs:
                env.scroll_screen(self._scroll_right)
            for rew in self._rewards:
                rew.scroll_screen(self._scroll_right)
            for obs in self._obstacles:
                obs.scroll_screen(self._scroll_right)

        if self._scroll_right is not None and not self._player.animated_move:
            if self._scroll_right:
                self._scroll_right = None
                self._actual_left += self._screen_margin
                self._actual_right += self._screen_margin
                self.add_right_content()
            else:
                self._scroll_right = None
                self._actual_left -= self._screen_margin
                self._actual_right -= self._screen_margin
                self.add_left_content()

    def game_step(self):
        self._environs.update()
        self._rewards.update()
        self._obstacles.update()
        self._player.update()

        self.player_collisions()

        self.player_movement()

        if self._player.is_dead:
            self._game_state = GameState.END.value

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

    def player_retard(self):
        self._player.retard()

    def game_events(self, event):
        if event.type == self.obstacles_event:
            for obstacle in self._obstacles:
                obstacle.update_animation()

        if event.type == self.elapsed_event:
            play_time = pygame.time.get_ticks() - self._play_time_start
            if self._game_background is not None:
                self._game_background.set_game_time_text(str(play_time // 1000))

    def update_environment_state(self):
        mini_height, mini_width, _ = self.env_state_size()

        mini_map = np.zeros((mini_height, mini_width))

        for i in range(mini_height):
            for j in range(mini_width):
                for e in self._environs:
                    if j == e.rect.x // MINIMAP_ONE_PIXEL and i == e.rect.y // MINIMAP_ONE_PIXEL:
                        mini_map[i, j] = 0.4
                for o in self._obstacles:
                    if j == o.rect.x // MINIMAP_ONE_PIXEL and i == o.rect.y // MINIMAP_ONE_PIXEL:
                        mini_map[i, j] = 0.2
                        if i < mini_height - 1:
                            mini_map[i+1, j] = 0.2
                for r in self._rewards:
                    if j == r.rect.x // MINIMAP_ONE_PIXEL and i == r.rect.y // MINIMAP_ONE_PIXEL:
                        if isinstance(r, Apple):
                            mini_map[i, j] = 0.9
                        elif isinstance(r, Pear):
                            mini_map[i, j] = 0.95
                        elif isinstance(r, Water):
                            mini_map[i, j] = 1.0
                        else:
                            mini_map[i, j] = 1.0
                if j == self._player.rect.x // MINIMAP_ONE_PIXEL and i == self._player.rect.y // MINIMAP_ONE_PIXEL:
                    mini_map[i, j] = 0.6
                    if i < mini_height - 1:
                        mini_map[i+1, j] = 0.6
        self._environment_state = mini_map.reshape(mini_height, mini_width, 1)
        return mini_map

    def update_player_state(self, mini_map):
        mini_height, mini_width = mini_map.shape
        find_plr = False
        for i in range(mini_height):
            for j in range(mini_width):
                if mini_map[i, j] == 0.6:
                    find_plr = True
                    break  # to go to next line
                if find_plr and mini_map[i, j] == 0.4:
                    if self._player.direction:
                        pos_start = min(j+self._player.rect.x//MINIMAP_ONE_PIXEL, mini_width-1)
                        pos_stop = min(pos_start+5, mini_width-1)
                        for k in range(pos_start, pos_stop):
                            if mini_map[i, k] == 0:
                                # print("R ", (k * MINIMAP_ONE_PIXEL - self._player.rect.x) / MINIMAP_ONE_PIXEL)
                                return (k * MINIMAP_ONE_PIXEL - self._player.rect.x) / MINIMAP_ONE_PIXEL
                        return 5.
                    else:
                        # print("L ", (self._player.rect.x - j * MINIMAP_ONE_PIXEL) / MINIMAP_ONE_PIXEL)
                        return (self._player.rect.x - j * MINIMAP_ONE_PIXEL) / MINIMAP_ONE_PIXEL
        return 5.

    def add_reward(self, reward: float):
        self._score += reward

    @property
    def points_score(self):
        return self._score

    @property
    def life_score(self):
        return self._player.MAX_LIFE - self._player.life

    @property
    def game_state(self) -> bool:  # check if game should be finish
        play_time = pygame.time.get_ticks() - self._play_time_start
        return self.is_game_over()  # or play_time > 100000

    @property
    def environment_state(self):
        mini_map = self.update_environment_state()
        distance_to_hole = self.update_player_state(mini_map)
        return self._environment_state, self._player.player_state  # (*self._player.player_state, distance_to_hole)

    def is_game_over(self):
        return self._game_state == GameState.END.value

    def is_game_paused(self):
        return self._game_state == GameState.PAUSE.value

    def is_game_running(self):
        return self._game_state == GameState.RUN.value




