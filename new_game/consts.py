from enum import Enum


class GameMode(Enum):
    NORMAL = 1
    API_PLAY = 2
    API_LEARN = 3


GAME_MODE = GameMode.NORMAL.value

GAME_TITLE = "Blue Drop Journey"

FRAME_RATE = 60

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# BG_COLOR = ()

FONT_COLOR_DARK = "BROWN"
FONT_COLOR_LIGHT = "GOLD"
FONT_PATH = "new_game/media/fonts/Lato-Regular.ttf"
BOLD_FONT_PATH = "new_game/media/fonts/Lato-Bold.ttf"
