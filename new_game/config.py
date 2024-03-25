from enum import Enum


class GameMode(Enum):
    NORMAL = 1
    API_PLAY = 2
    API_LEARN = 3


class MapNN(Enum):
    CNN = 1
    DNN = 2


class TimeEvents(Enum):
    OBSTACLE_EVENT = 1
    ELAPSED_EVENT = 2


class ProjectSetup:
    MODES = {"play_mode": GameMode.API_PLAY.value,
             "map_nn_mode": MapNN.DNN.value}

    @classmethod
    def set_api_mode(cls, mode: GameMode):
        cls.MODES["play_mode"] = mode.value

    @classmethod
    def set_map_mode(cls, mode: MapNN):
        cls.MODES["map_nn_mode"] = mode.value


GAME_TITLE = "Blue Drop Journey"

FRAME_RATE = 60

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
MINIMAP_ONE_PIXEL = 25
SCREEN_SIDE_MARGIN = SCREEN_WIDTH / 4

# BG_COLOR = ()

FONT_COLOR_DARK = "BROWN"
FONT_COLOR_LIGHT = "GOLD"
FONT_PATH = "new_game/media/fonts/Lato-Regular.ttf"
BOLD_FONT_PATH = "new_game/media/fonts/Lato-Bold.ttf"
