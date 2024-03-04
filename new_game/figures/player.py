import pygame
from pygame.sprite import Sprite


class Player(Sprite):
    INIT_GRAVITY = 100
    INIT_JUMP_VELOCITY = 100

    def __init__(self):
        super().__init__()

        self._image_move = pygame.image.load("new_game/media/images/figureR.png").convert_alpha()
        self._image_jump = pygame.image.load("new_game/media/images/jumpR.png").convert_alpha()

        self._animation_index = 0
        self._max_anim_index = 6
        self._move_width = self._image_move.get_rect().width / 6
        self._jump_width = self._image_jump.get_rect().width / 12
        self._rect_m = pygame.Rect(0, 0, self._move_width, self._image_move.get_rect().height)
        self._rect_j = pygame.Rect(0, 0, self._jump_width, self._image_jump.get_rect().height)

        self._life = 20
        self._velocity = 0
        self._gravity = self.INIT_GRAVITY
        self._jump_v = self.INIT_JUMP_VELOCITY
        self._right_direction = True
        self._position = []

        self.group = pygame.sprite.GroupSingle()
        self.group.add(self)

    def jump(self):
        pass

    def move(self, to_right: bool):
        pass

    def animation(self):
        if self._velocity > 0:
            pass

    def draw(self, screen):
        self.group.draw(screen)
