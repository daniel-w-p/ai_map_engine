import pygame
from pygame.sprite import Sprite


class Obstacles(Sprite):
    def __init__(self):
        super().__init__()

        self._img = None

        self._animation_index = 0
        self._max_anim_index = 3
        self._img_frame_width = None

        self._rect = None

    def update_animation(self):
        self._animation_index += 1
        if self._animation_index >= self._max_anim_index:
            self._animation_index = 0
        self._rect = pygame.Rect(self._animation_index * self._img_frame_width,
                                 0,
                                 self._img_frame_width + self._animation_index * self._img_frame_width,
                                 self._img.get_rect().height)


class Fire(Obstacles):
    def __init__(self):
        super().__init__()

        self._max_anim_index = 6

        self._img = pygame.image.load("new_game/media/images/fire.png").convert_alpha()
        self._img_frame_width = self._img.get_rect().width / self._max_anim_index

        self._rect = pygame.Rect(0, 0, self._img_frame_width, self._img.get_rect().height)


class Meteor(Obstacles):
    def __init__(self):
        super().__init__()

        self._img = pygame.image.load("new_game/media/images/meteor.png").convert_alpha()
        self._img_frame_width = self._img.get_rect().width / self._max_anim_index

        self._rect = pygame.Rect(0, 0, self._img_frame_width, self._img.get_rect().height)
