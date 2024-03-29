from enum import Enum


class GameMode(Enum):
    NORMAL = 1
    API_PLAY = 2
    API_LEARN = 3


class MapNN(Enum):
    CNN = 1
    DNN = 2


class ProjectSetup:
    MODES = {"play_mode": GameMode.API_PLAY.value,
             "map_nn_mode": MapNN.CNN.value}

    @classmethod
    def set_api_mode(cls, mode: GameMode):
        cls.MODES["play_mode"] = mode.value

    @classmethod
    def set_map_mode(cls, mode: MapNN):
        cls.MODES["map_nn_mode"] = mode.value
