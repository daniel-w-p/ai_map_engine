import pygame
from pygame.sprite import Sprite
from enum import Enum


class ImagePart(Enum):
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2


class Environ(Sprite):
    def __init__(self):
        super().__init__()

        self._img = None

        self._image_part = ImagePart.LEFT
        self._frames = len(ImagePart)
        self._img_frame_width = None

        self._rect = None

    def set_frame(self, frame: ImagePart) -> None:
        self._rect = pygame.Rect(0, 0, self._img_frame_width, self._img.get_rect().height)


class Wood(Environ):
    def __init__(self):
        super().__init__()
        self._img = pygame.image.load("new_game/media/images/wood.png").convert_alpha()
        self._img_frame_width = self._img.get_rect().width / self._frames

        self._rect = pygame.Rect(0, 0, self._img_frame_width, self._img.get_rect().height)


class Cloud(Environ):
    def __init__(self):
        super().__init__()
        self._img = pygame.image.load("new_game/media/images/cloud.png").convert_alpha()
        self._img_frame_width = self._img.get_rect().width / self._frames

        self._rect = pygame.Rect(0, 0, self._img_frame_width, self._img.get_rect().height)

