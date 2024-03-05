import pygame
from pygame.sprite import Sprite

from ..consts import SCREEN_SIDE_MARGIN


class Obstacles(Sprite):
    def __init__(self):
        super().__init__()

        self._img = None
        self._rect = None
        self._subsurface_rect = None
        self._is_visible = False
        self._scroll_value = 0

        self._animation_index = 0
        self._max_anim_index = 3
        self._img_frame_width = None

    def update_animation(self):
        self._animation_index += 1
        if self._animation_index >= self._max_anim_index:
            self._animation_index = 0
        self._subsurface_rect = pygame.Rect(self._animation_index * self._img_frame_width,
                                            0,
                                            self._img_frame_width + self._animation_index * self._img_frame_width,
                                            self._img.get_rect().height)

    def update_position(self):
        pass

    def scroll_screen(self):
        if self._scroll_value == 0:
            self._scroll_value = SCREEN_SIDE_MARGIN
        else:
            self._rect.x -= 2

    def destruct(self):
        if self._rect.x < -SCREEN_SIDE_MARGIN:
            self.kill()

    def update(self):
        if self._is_visible:
            self.update_animation()
            self.update_position()
        self.destruct()

    def set_visible(self, visible):
        self._is_visible = visible

    @property
    def image(self):
        return self._img.subsurface(self._subsurface_rect)

    @property
    def rect(self):
        return self._rect


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

    def update_position(self):
        self._rect.x -= 1
        self._rect.y += 1
