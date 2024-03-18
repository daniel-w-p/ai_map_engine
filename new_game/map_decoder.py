import numpy as np
from PIL import Image
from enum import Enum
from .config import MINIMAP_ONE_PIXEL


class GameParticles(Enum):
    WOOD_START = 0
    WOOD_MIDDLE = 1
    WOOD_END = 2
    CLOUD_START = 3
    CLOUD_MIDDLE = 4
    CLOUD_END = 5
    APPLE = 6
    PEAR = 7
    WATER = 8
    FIRE = 9
    METEOR = 10
    FINISH = 11


class MapDecoder:
    PARTICLES_DICTIONARY = {(170, 0, 0): GameParticles.WOOD_START,
                            (0, 0, 0): GameParticles.WOOD_MIDDLE,
                            (0, 0, 170): GameParticles.WOOD_END,
                            (0, 255, 0): GameParticles.CLOUD_START,
                            (0, 0, 255): GameParticles.CLOUD_MIDDLE,
                            (0, 255, 255): GameParticles.CLOUD_END,
                            (255, 0, 0): GameParticles.APPLE,
                            (255, 255, 0): GameParticles.PEAR,
                            (255, 0, 255): GameParticles.WATER,
                            (255, 170, 0): GameParticles.FIRE,
                            (240, 160, 0): GameParticles.METEOR,
                            (0, 170, 0): GameParticles.FINISH}

    def __init__(self):
        self._img = Image.open("new_game/media/images/map.png")
        self._img_width, self.img_height = self._img.size
        self._img_array = np.array(self._img)
        self._one_pixel = MINIMAP_ONE_PIXEL
        self._elements_dict = {}  # key: position (in game)  value: environment particle

    def prepare_map(self):
        for i, row in enumerate(self._img_array):
            for j, pixel in enumerate(row):
                if not tuple(pixel) == (255, 255, 255):
                    self._elements_dict[(j * self._one_pixel, i * self._one_pixel)] = self.PARTICLES_DICTIONARY[tuple(pixel)]

    @property
    def elements_dictionary(self):
        return self._elements_dict

    @property
    def map_real_width(self):
        return self._img_width * self._one_pixel

