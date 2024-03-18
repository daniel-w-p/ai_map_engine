import pygame
from pygame.sprite import Sprite

from ..config import SCREEN_SIDE_MARGIN


class Particles(Sprite):
    def __init__(self):
        super().__init__()
        self._img = None
        self._subsurface_rect = None
        self._rect = None
        self._scroll_value = 0
        self._scroll_right = None

    def scroll_screen(self, to_right: bool):
        if self._scroll_value == 0:
            if to_right:
                self._scroll_right = True
            else:
                self._scroll_right = False
            self._scroll_value = SCREEN_SIDE_MARGIN

    def destruct(self):
        if self._rect.x < -SCREEN_SIDE_MARGIN:
            self.kill()

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
        self.destruct()

    @property
    def image(self):
        return self._img.subsurface(self._subsurface_rect)

    @property
    def rect(self):
        return self._rect
