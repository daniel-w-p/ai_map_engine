import pygame
from new_game import config, GameCrl, Game
from new_game.figures import Player
from a3c import A3CModel, Agent


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption(config.GAME_TITLE)
    clock = pygame.time.Clock()

    game_control = GameCrl()
    background = game_control.back
    # only for AI
    model = None
    play_from_checkpoint = True
    e_state, p_state, reward, done = None, None, None, False

    if config.ProjectSetup.MODES["play_mode"] == config.GameMode.API_PLAY.value:
        print("Start game in AI mode (model control)")
        env_state_shape = Game.env_state_size()
        plr_state_shape = Player.plr_state_size()
        action_space = GameCrl.action_space_size()
        model = A3CModel(env_state_shape, plr_state_shape, action_space)
        if play_from_checkpoint:
            Agent.load_model(model)
        e_state, p_state, reward, done = game_control.game_action_api(0)

    while True:
        if config.ProjectSetup.MODES["play_mode"] == config.GameMode.NORMAL.value:
            game_control.normal_loop_body()
        elif config.ProjectSetup.MODES["play_mode"] == config.GameMode.API_PLAY.value:
            action, _ = Agent.choose_action((e_state, p_state), model, True)
            e_state, p_state, reward, done = game_control.game_action_api(action)
            game_control.api_loop_body()
        # draw all
        if game_control.game.is_game_running():
            background.draw_statics(screen)
            background.refresh_on_screen(screen)
            game_control.game.draw_stage(screen)
        else:
            background.draw_intro(screen)
        # control environ
        clock.tick(config.FRAME_RATE)

        pygame.display.update()


if __name__ == '__main__':
    run_game()
