import pygame
from pygame.sprite import Sprite

from ..config import SCREEN_WIDTH
from .a_particles import Particles


class Obstacles(Particles):
    def __init__(self):
        super().__init__()

        self._is_visible = None
        self._animation_index = 0
        self._max_anim_index = 3
        self._img_frame_width = None

    def update_animation(self):
        if self._is_visible:
            self._animation_index += 1
            if self._animation_index >= self._max_anim_index:
                self._animation_index = 0
            self._subsurface_rect = pygame.Rect(self._animation_index * self._img_frame_width,
                                                0,
                                                self._img_frame_width,
                                                self._img.get_rect().height)

    def update_position(self):
        pass

    def update(self):
        if 0 < self._rect.x < SCREEN_WIDTH:
            self._is_visible = True
        else:
            self._is_visible = False
        if self._is_visible:
            self.update_position()
        super().update()

    def set_visible(self, visible):
        self._is_visible = visible


class Fire(Obstacles):
    def __init__(self):
        super().__init__()

        self._max_anim_index = 6

        self._img = pygame.image.load("new_game/media/images/fire.png").convert_alpha()
        self._img_frame_width = self._img.get_rect().width // self._max_anim_index

        self._rect = pygame.Rect(0, 0, self._img_frame_width, self._img.get_rect().height)
        self._subsurface_rect = pygame.Rect(0,
                                            0,
                                            self._img_frame_width,
                                            self._img.get_rect().height)


class Meteor(Obstacles):
    def __init__(self):
        super().__init__()

        self._img = pygame.image.load("new_game/media/images/meteor.png").convert_alpha()
        self._img_frame_width = self._img.get_rect().width // self._max_anim_index

        self._rect = pygame.Rect(0, 0, self._img_frame_width, self._img.get_rect().height)
        self._subsurface_rect = pygame.Rect(0,
                                            0,
                                            self._img_frame_width,
                                            self._img.get_rect().height)

    def update_position(self):
        self._rect.x -= 1
        self._rect.y += 1
