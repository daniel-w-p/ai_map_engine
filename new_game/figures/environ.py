import pygame
from enum import Enum

from .a_particles import Particles


class ImagePart(Enum):
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2


class Environ(Particles):
    def __init__(self):
        super().__init__()

        self._frames = len(ImagePart)
        self._img_frame_width = None

    def set_frame(self, part: ImagePart) -> None:
        self._subsurface_rect = pygame.Rect(part.value * self._img_frame_width, 0, self._img_frame_width, self._img.get_rect().height)


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

