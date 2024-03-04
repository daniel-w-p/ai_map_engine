import pygame
from .consts import FONT_COLOR_DARK, FONT_COLOR_LIGHT, FONT_PATH, BOLD_FONT_PATH, SCREEN_WIDTH, SCREEN_HEIGHT


class Drawing:
    def __init__(self):
        self._background = None
        self._stats_panel = None
        self._intro_panel = None

        self._game_map_text = None
        self._game_level_text = None
        self._game_score_text = None
        self._game_high_score_text = None
        self._player_life_text = None

        self._game_map_label = None
        self._game_level_label = None
        self._game_score_label = None
        self._game_high_score_label = None
        self._player_life_label = None

        self._intro_label = None

        self._dynamic_text_font = pygame.font.Font(FONT_PATH, 22)

        self.load_background("new_game/media/images/back.png")
        self.load_panel("new_game/media/images/panel.png")
        self.load_intro_panel("new_game/media/images/window.png")
        self.init_all_texts()

    def load_background(self, value: str):
        self._background = pygame.image.load(value).convert()

    def load_panel(self, value: str):
        self._stats_panel = pygame.image.load(value).convert()

    def load_intro_panel(self, value: str):
        self._intro_panel = pygame.image.load(value).convert()

    def set_game_map_text(self, value: str):
        self._game_map_text = self._dynamic_text_font.render(value, True, FONT_COLOR_DARK)

    def set_game_level_text(self, value: str):
        self._game_level_text = self._dynamic_text_font.render(value, True, FONT_COLOR_DARK)

    def set_game_score_text(self, value: str):
        self._game_score_text = self._dynamic_text_font.render(value, True, FONT_COLOR_DARK)

    def set_game_high_score_text(self, value: str):
        self._game_high_score_text = self._dynamic_text_font.render(value, True, FONT_COLOR_DARK)

    def set_player_life_text(self, value: str):
        self._player_life_text = self._dynamic_text_font.render(value, True, FONT_COLOR_DARK)

    def init_static_labels(self):
        font = pygame.font.Font(FONT_PATH, 15)
        self._player_life_label = font.render("LIVE", True, FONT_COLOR_LIGHT)
        self._game_level_label = font.render("LEVEL", True, FONT_COLOR_LIGHT)
        self._game_map_label = font.render("MAP", True, FONT_COLOR_LIGHT)
        self._game_score_label = font.render("SCORE", True, FONT_COLOR_LIGHT)
        self._game_high_score_label = font.render("HIGH SCORE", True, FONT_COLOR_LIGHT)

    def init_all_texts(self):
        self.set_game_map_text('0')
        self.set_game_level_text('0')
        self.set_game_score_text('0')
        self.set_game_high_score_text('0')
        self.set_player_life_text('0')

    def draw_intro(self, screen):
        screen.fill((120, 178, 141))
        intro_rect = self._intro_panel.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(self._intro_panel, intro_rect)
        font = pygame.font.Font(BOLD_FONT_PATH, 20)
        self._intro_label = font.render("PRESS SPACE", True, FONT_COLOR_DARK)
        screen.blit(self._intro_label, self._intro_label.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 12)))
        self._intro_label = font.render("TO START", True, FONT_COLOR_DARK)
        screen.blit(self._intro_label, self._intro_label.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 12)))

    def draw_statics(self, screen):
        left_margin = 50
        upper_margin = 0
        label_space = 200

        screen.blit(self._background, (0, 0))
        screen.blit(self._stats_panel, (0, 0))

        self.init_static_labels()

        screen.blit(self._player_life_label, (left_margin, upper_margin))
        screen.blit(self._game_level_label, (left_margin + 1 * label_space, upper_margin))
        screen.blit(self._game_map_label, (left_margin + 2 * label_space, upper_margin))
        screen.blit(self._game_score_label, (left_margin + 3 * label_space, upper_margin))
        screen.blit(self._game_high_score_label, (left_margin + 4 * label_space, upper_margin))

    def refresh_on_screen(self, screen):
        left_margin = 100
        upper_margin = 12
        text_space = 200

        screen.blit(self._player_life_text, (left_margin, upper_margin))
        screen.blit(self._game_level_text, (left_margin + 1 * text_space, upper_margin))
        screen.blit(self._game_map_text, (left_margin + 2 * text_space, upper_margin))
        screen.blit(self._game_score_text, (left_margin + 3 * text_space, upper_margin))
        screen.blit(self._game_high_score_text, (left_margin + 4 * text_space, upper_margin))
