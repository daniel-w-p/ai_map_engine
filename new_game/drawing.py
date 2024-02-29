import pygame
from .consts import UPPER_PANEL_FONT_SIZE, FONT_COLOR, STATS_PADDING_WIDTH


class Drawing:
    def __init__(self):
        self._background = None
        self._stats_panel = None
        self._game_map_text = None
        self._game_level_text = None
        self._game_score_text = None
        self._game_high_score_text = None
        self._player_life_text = None

        self.load_background("new_game/media/images/back.png")
        self.load_panel("new_game/media/images/panel.png")
        self.init_all_texts()

    @property
    def background(self):
        return self._background

    @property
    def stats_panel(self):
        return self._stats_panel

    @property
    def game_map_text(self):
        return self._game_map_text

    @property
    def game_level_text(self):
        return self._game_level_text

    @property
    def game_score_text(self):
        return self._game_score_text

    @property
    def game_high_score_text(self):
        return self._game_high_score_text

    @property
    def player_life_text(self):
        return self._player_life_text

    def load_background(self, value):
        self._background = pygame.image.load(value)

    def load_panel(self, value):
        self._stats_panel = pygame.image.load(value)

    def set_game_map_text(self, value):
        font = pygame.font.Font(None, UPPER_PANEL_FONT_SIZE)
        self._game_map_text = font.render(value, True, FONT_COLOR)

    def set_game_level_text(self, value):
        font = pygame.font.Font(None, UPPER_PANEL_FONT_SIZE)
        self._game_level_text = font.render(value, True, FONT_COLOR)

    def set_game_score_text(self, value):
        font = pygame.font.Font(None, UPPER_PANEL_FONT_SIZE)
        self._game_score_text = font.render(value, True, FONT_COLOR)

    def set_game_high_score_text(self, value):
        font = pygame.font.Font(None, UPPER_PANEL_FONT_SIZE)
        self._game_high_score_text = font.render(value, True, FONT_COLOR)

    def set_player_life_text(self, value):
        font = pygame.font.Font(None, UPPER_PANEL_FONT_SIZE)
        self._player_life_text = font.render(value, True, FONT_COLOR)

    def init_all_texts(self):
        self.set_game_map_text('0')
        self.set_game_level_text('0')
        self.set_game_score_text('0')
        self.set_game_high_score_text('0')
        self.set_player_life_text('0')

    def refresh_on_screen(self, screen):
        screen.blit(self.player_life_text, (100, 20))
        screen.blit(self.game_level_text, (100 + 1 * STATS_PADDING_WIDTH, 20))
        screen.blit(self.game_map_text, (100 + 2 * STATS_PADDING_WIDTH, 20))
        screen.blit(self.game_score_text, (100 + 3 * STATS_PADDING_WIDTH, 20))
        screen.blit(self.game_high_score_text, (100 + 4 * STATS_PADDING_WIDTH, 20))
