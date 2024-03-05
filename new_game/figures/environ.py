import pygame
from pygame.sprite import Sprite
from enum import Enum

from ..consts import SCREEN_SIDE_MARGIN


class ImagePart(Enum):
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2


class Environ(Sprite):
    def __init__(self):
        super().__init__()

        self._img = None
        self._rect = None
        self._subsurface_rect = None
        self._scroll_value = 0

        self._frames = len(ImagePart)
        self._img_frame_width = None

    def set_frame(self, part: ImagePart) -> None:
        self._subsurface_rect = pygame.Rect(part.value * self._img_frame_width, 0, self._img_frame_width, self._img.get_rect().height)

    def scroll_screen(self):
        if self._scroll_value == 0:
            self._scroll_value = SCREEN_SIDE_MARGIN
        else:
            self._rect.x -= 2

    def destruct(self):
        if self._rect.x < -SCREEN_SIDE_MARGIN:
            self.kill()

    def update(self):
        self.destruct()

    @property
    def image(self):
        return self._img.subsurface(self._subsurface_rect)

    @property
    def rect(self):
        return self._rect


class Wood(Environ):
    def __init__(self, part: ImagePart):
        super().__init__()
        self._img = pygame.image.load("new_game/media/images/wood.png").convert_alpha()
        self._img_frame_width = self._img.get_rect().width / self._frames

        self._rect = pygame.Rect(0, 0, self._img_frame_width, self._img.get_rect().height)
        self._subsurface_rect = pygame.Rect(part.value * self._img_frame_width, 0, self._img_frame_width, self._img.get_rect().height)


class Cloud(Environ):
    def __init__(self, part: ImagePart):
        super().__init__()
        self._img = pygame.image.load("new_game/media/images/cloud.png").convert_alpha()
        self._img_frame_width = self._img.get_rect().width / self._frames

        self._rect = pygame.Rect(0, 0, self._img_frame_width, self._img.get_rect().height)
        self._subsurface_rect = pygame.Rect(part.value * self._img_frame_width, 0, self._img_frame_width, self._img.get_rect().height)

