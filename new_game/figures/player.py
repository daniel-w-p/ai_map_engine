import numpy as np
import pygame
import math
from pygame.sprite import Sprite
from enum import Enum

from ..config import SCREEN_SIDE_MARGIN, MINIMAP_ONE_PIXEL


class ObstaclesDamage(Enum):
    FIRE_DAMAGE = 1
    METEOR_DAMAGE = 2
    OUT_OF_SCREEN = 10


class Player(Sprite):
    MAX_GRAVITY = 0.65
    MAX_VELOCITY = 5
    MAX_JUMP_VELOCITY = 16
    MAX_LIFE = 21

    def __init__(self):
        super().__init__()

        self._image_move = pygame.image.load("new_game/media/images/figure.png").convert_alpha()

        self._scroll_value = 0
        self._scroll_right = True
        self._is_visible = True
        self._animation_index = 0
        self._max_anim_index = 3
        self._life = 0
        self._rect = None

        self._move_width = self._image_move.get_rect().width // self._max_anim_index
        self._subsurface_rect = pygame.Rect(0, 0, self._move_width, self._image_move.get_rect().height)

        self.live_reset()
        self.position_reset()

        self._velocity = 0
        self._momentum = 0
        self._gravity = self.MAX_GRAVITY
        self._jump_v = -1
        self._right_direction = True
        self._on_ground = False

        self.state_series = []

        self.group = pygame.sprite.GroupSingle()
        self.group.add(self)

    @staticmethod
    def plr_state_size():
        return 7  # position_x, position_y, velocity, momentum, jump_velocity, direction,     distance (from map)

    @property
    def image(self):
        subsurface = self._image_move.subsurface(self._subsurface_rect)
        if self._right_direction:
            return subsurface
        else:
            return pygame.transform.flip(subsurface, True, False)

    @property
    def rect(self):
        return self._rect

    @property
    def is_dead(self):
        return self._life <= 0

    @property
    def life(self):
        return self._life

    @property
    def animated_move(self):
        return self._scroll_value > 0

    @property
    def direction(self):
        return self._right_direction

    @property
    def player_state_now(self):
        return (self.rect.x / MINIMAP_ONE_PIXEL, self.rect.y / MINIMAP_ONE_PIXEL, self._velocity, self._momentum,
                self._jump_v, int(self._right_direction))

    @property
    def player_state(self):
        return self.state_series

    def live_reset(self):
        self._life = self.MAX_LIFE

    def position_reset(self):
        self._rect = pygame.Rect(110, 500, self._move_width, self._image_move.get_rect().height)

    def movement_reset(self):
        self._velocity = 0
        self._momentum = 0
        self._jump_v = -1
        self._right_direction = True
        self._on_ground = False

    def reset(self):
        self.live_reset()
        self.position_reset()
        self.movement_reset()

        states = np.array(self.player_state_now)
        self.state_series = np.tile(states[np.newaxis, :], (10, 1))

    def update_animation(self, delta_move):
        self._animation_index += math.fabs(delta_move)
        if delta_move == 0 and self._animation_index:
            self._animation_index += 1
        if self._animation_index >= self._max_anim_index or self._animation_index < 0:
            self._animation_index = 0
        if self._jump_v:
            self._animation_index = 1

        self._subsurface_rect = pygame.Rect(math.floor(self._animation_index) * self._move_width,
                                            0,
                                            self._move_width,
                                            self._image_move.get_rect().height)

    def jump(self):
        if self._on_ground and self._jump_v == 0:
            self._on_ground = False
            self._jump_v = self.MAX_JUMP_VELOCITY - 0.5 * self._velocity

    def move(self, to_right: bool):
        if to_right != self._right_direction:
            self._velocity = 0
            self._momentum = 0
        self._right_direction = to_right
        self._velocity += 1

    def retard(self):
        self._velocity = 0
        self._momentum = self.MAX_VELOCITY - 1

    def scroll_screen(self, to_right: bool):
        if self._scroll_value == 0:
            if to_right:
                self._scroll_right = True
            else:
                self._scroll_right = False
            self._scroll_value = SCREEN_SIDE_MARGIN

    def animation(self):
        if self._is_visible:
            velocity_factor = self._velocity + self._momentum
            animation_factor = self._velocity - math.fabs(self._jump_v // 4) + self._momentum

            self.update_animation(animation_factor * 0.05)

            if self._momentum > 0:
                self._momentum -= 0.5
            else:
                self._momentum = 0

            if self._right_direction:
                self._rect.x += velocity_factor
            else:
                self._rect.x -= velocity_factor

            jump_factor = self._jump_v
            if jump_factor:
                jump_factor -= math.fabs(self._velocity)

            self._rect.y -= jump_factor
            self._jump_v -= self._gravity

            if self._jump_v > self.MAX_JUMP_VELOCITY:
                self._jump_v = self.MAX_JUMP_VELOCITY
            elif self._jump_v < -self.MAX_JUMP_VELOCITY:
                self._jump_v = -self.MAX_JUMP_VELOCITY
            if self._velocity > 0:
                self._velocity += 0.1
            if self._velocity > self.MAX_VELOCITY:
                self._velocity = self.MAX_VELOCITY

    def stop(self, on_ground: bool, ground: float):
        if on_ground:
            self._jump_v = 0
            self._rect.y = ground
        else:
            self._jump_v = -0.5
            self._rect.y += 1
        self._on_ground = on_ground

    def hurt(self, is_fire: bool):
        if is_fire:
            self._life -= ObstaclesDamage.FIRE_DAMAGE.value
        else:
            self._life -= ObstaclesDamage.METEOR_DAMAGE.value
        self._momentum -= self.MAX_VELOCITY - 1
        if self._right_direction:
            self._rect.x -= self._velocity * 1.5
        else:
            self._rect.x += self._velocity * 1.5

    def fall_out(self):
        self._rect.y = -100
        self._jump_v = 1
        self._life -= ObstaclesDamage.OUT_OF_SCREEN.value

    def draw(self, screen):
        self.group.draw(screen)

    def update(self):
        if self._scroll_value:
            step = 10
            if self._scroll_right:
                self._rect.x -= step
            else:
                self._rect.x += step
            self._scroll_value -= step
            if self._scroll_value < 0:
                self._scroll_value = 0
        self.animation()

        self.state_series = np.vstack([self.state_series[1:], self.player_state_now])


