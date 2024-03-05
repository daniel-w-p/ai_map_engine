import pygame
from pygame.sprite import Sprite
from enum import Enum

from ..consts import SCREEN_SIDE_MARGIN


class ImagePart(Enum):
    PEAR = 0
    APPLE = 1
    WATER = 2


class Rewards(Sprite):
    def __init__(self):
        super().__init__()

        self._img = pygame.image.load("new_game/media/images/items.png").convert_alpha()

        self._subsurface_rect = None
        self._scroll_value = 0

        self._image_part = ImagePart.PEAR
        self._img_frame_width = self._img.get_width() / 3

        self._rect = pygame.Rect(0, 0, self._img_frame_width, self._img.get_rect().height)

    def set_frame(self, frame: ImagePart):
        self._subsurface_rect = pygame.Rect(frame.value * self._img_frame_width, 0, self._img_frame_width, self._img.get_rect().height)

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


class Pear(Rewards):
    def __init__(self):
        super().__init__()
        self.set_frame(ImagePart.PEAR)


class Apple(Rewards):
    def __init__(self):
        super().__init__()
        self.set_frame(ImagePart.APPLE)


class Water(Rewards):
    def __init__(self):
        super().__init__()
        self.set_frame(ImagePart.WATER)
