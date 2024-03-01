class Player:
    INIT_GRAVITY = 100
    INIT_JUMP_VELOCITY = 100

    def __init__(self):
        self._life = 20
        self._velocity = 0
        self._gravity = self.INIT_GRAVITY
        self._jump_v = self.INIT_JUMP_VELOCITY
        self._right_direction = True
        self._position = []

    def jump(self):
        pass

    def move(self, direction: bool):
        pass

    def animation(self):
        if self._velocity > 0:
            pass
