import pygame
import math
from pygame.sprite import Sprite
from ..consts import SCREEN_HEIGHT


class Player(Sprite):
    MAX_GRAVITY = 0.65
    MAX_VELOCITY = 5
    MAX_JUMP_VELOCITY = 20

    def __init__(self):
        super().__init__()

        self._image_move = pygame.image.load("new_game/media/images/figureP.png").convert_alpha()
        # self._image_jump = pygame.image.load("new_game/media/images/jumpP.png").convert_alpha()

        self._is_visible = True
        self._animation_index = 0
        self._max_anim_index = 6
        self._move_width = self._image_move.get_rect().width // self._max_anim_index
        self._rect = pygame.Rect(110, 500, self._move_width, self._image_move.get_rect().height)
        self._subsurface_rect = pygame.Rect(0, 0, self._move_width, self._image_move.get_rect().height)

        self._life = 20
        self._velocity = 0
        self._momentum = 0
        self._gravity = self.MAX_GRAVITY
        self._jump_v = 0
        self._right_direction = True
        self._on_ground = False

        self.group = pygame.sprite.GroupSingle()
        self.group.add(self)

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

    def update_animation(self, delta_move):
        self._animation_index += math.fabs(delta_move)
        if delta_move == 0 and self._animation_index:
            self._animation_index += 1
        if self._animation_index >= self._max_anim_index or self._animation_index < 0:
            self._animation_index = 0
        # if self._momentum:
        #     self._animation_index %= 2
        if self._jump_v:
            self._animation_index = 4

        self._subsurface_rect = pygame.Rect(math.floor(self._animation_index) * self._move_width,
                                            0,
                                            self._move_width,
                                            self._image_move.get_rect().height)

    def jump(self):
        if self._on_ground:
            self._on_ground = False
            self._jump_v = self.MAX_JUMP_VELOCITY - 0.5 * self._velocity

    def move(self, to_right: bool):
        self._right_direction = to_right
        self._velocity += 1

    def retard(self):
        self._velocity = 0
        self._momentum += self.MAX_VELOCITY - 1

    def animation(self):
        if self._is_visible:
            velocity_factor = self._velocity + self._momentum
            animation_factor = self._velocity - math.fabs(self._jump_v // 4) + self._momentum

            self.update_animation(animation_factor * 0.1)

            if self._momentum > 0:
                self._momentum -= 0.5
            else:
                self._momentum = 0

            if self._right_direction:
                self._rect.x += velocity_factor
            else:
                self._rect.x -= velocity_factor

            jump_factor = self._jump_v
            if not self._on_ground:
                jump_factor //= 2

            self._rect.y -= jump_factor
            self._jump_v -= self._gravity

            if self._jump_v > self.MAX_JUMP_VELOCITY:
                self._jump_v = self.MAX_JUMP_VELOCITY
            if self._velocity > 0:
                self._velocity += 0.1
            if self._velocity > self.MAX_VELOCITY:
                self._velocity = self.MAX_VELOCITY

    def stop(self, on_ground: bool):
        if on_ground:
            self._jump_v = 0
        else:
            self._jump_v = -0.5
            self._rect.y += 1
        self._on_ground = on_ground

    def hurt(self):
        self._momentum -= self.MAX_VELOCITY - 1
        if self._right_direction:
            self._rect.x -= self._velocity * 1.5
        else:
            self._rect.x += self._velocity * 1.5

    def draw(self, screen):
        self.group.draw(screen)

    def update(self):
        if self._rect.y < 0 or self._rect.y > SCREEN_HEIGHT:
            self._is_visible = False
        else:
            self._is_visible = True

        self.animation()


