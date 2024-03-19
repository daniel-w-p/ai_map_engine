import pygame
from new_game import config
from new_game import GameCrl


class Environment:
    """
    The Environment class serves as an abstraction layer for interacting with the game using Pygame.
    It provides methods for initializing the game environment, performing actions in the game, and resetting the game state.

    Attributes:
        game_control (GameCrl): Game controller that manages the logic and state of the game.
    """

    def __init__(self):
        """
        Initializes the game environment.
        """
        try:
            pygame.init()
            pygame.display.set_mode((1, 1), pygame.NOFRAME)
            self.game_control = GameCrl()
        except Exception as e:
            print("Game initializing error: " + str(e))

    def step(self, action):
        """
        Executes an action in the game environment and returns the result.

        Args:
            action: Action to be performed in the game (defined by the model).

        Returns:
            tuple: A tuple containing the state of the environment after performing the action, the state of the player,
                   the reward for the performed action, and a flag indicating whether the game has ended.
        """
        e_state, p_state, reward, done = self.game_control.game_action_api(action)
        self.game_control.game.game_step()
        return e_state, p_state, reward, done

    def reset(self):
        """
        Resets the game state to its initial state.

        Returns:
            Object: The initial state of the game after the reset.
        """
        self.game_control.game.reset_game()
        return self.game_control.game.environment_state
