import pygame
from pygame.sprite import Sprite
from enum import Enum


class ImagePart(Enum):
    PEAR = 0
    APPLE = 1
    WATER = 2


class Rewards(Sprite):
    def __init__(self):
        super().__init__()

        self._img = pygame.image.load("new_game/media/images/items.png").convert_alpha()

        self._image_part = ImagePart.PEAR
        self._img_frame_width = self._img.get_width() / 3

        self._rect = None

    def set_frame(self, frame: ImagePart) -> None:
        self._rect = pygame.Rect(frame.value * self._img_frame_width, 0, self._img_frame_width, self._img.get_rect().height)


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
