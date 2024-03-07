import pygame
from enum import Enum

from .a_particles import Particles


class ImagePart(Enum):
    PEAR = 0
    APPLE = 1
    WATER = 2


class Rewards(Particles):
    def __init__(self):
        super().__init__()

        self._img = pygame.image.load("new_game/media/images/items.png").convert_alpha()

        self._image_part = ImagePart.PEAR
        self._img_frame_width = self._img.get_width() / 3

        self._rect = pygame.Rect(0, 0, self._img_frame_width, self._img.get_rect().height)

    def set_frame(self, frame: ImagePart):
        self._subsurface_rect = pygame.Rect(frame.value * self._img_frame_width, 0, self._img_frame_width, self._img.get_rect().height)


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
