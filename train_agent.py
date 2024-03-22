import multiprocessing as mp
import os
import queue

import pygame
import tensorflow as tf

from a3c import Agent, A3CModel
from environment import Environment
from new_game import Game, GameCrl, config
from new_game.figures import Player


def main():
    env_state_shape = Game.env_state_size()
    plr_state_shape = Player.plr_state_size()
    action_space = GameCrl.action_space_size()
    num_agents = 6
    epochs = 21
    start_from_checkpoint = True

    # Dynamic GPU memory allocation for TensorFlow
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError as e:
            print(e)

    env = Environment()
    main_model = A3CModel(env_state_shape, plr_state_shape, action_space)
    # Lazy build
    env_state, plr_state = env.reset()
    main_model((tf.convert_to_tensor([env_state], dtype=tf.float32), tf.convert_to_tensor([plr_state], dtype=tf.float32)))

    main_model.summary()

    if start_from_checkpoint and os.listdir(Agent.SAVE_DIR):
        print("Loading checkpoint...")
        main_model.load_weights(Agent.SAVE_DIR+Agent.SAVE_FILE)

    manager = mp.Manager()

    for i in range(epochs):
        print("Creating Agents")
        weights_queue = manager.Queue()
        experience_queue = manager.Queue()
        agents = []
        main_model_weights = main_model.get_weights()

        for a in range(num_agents):
            weights_queue.put(main_model_weights)
            print("Creating Agent ", a)
            agent = Agent(env_state_shape, plr_state_shape, action_space)
            agent_process = mp.Process(target=Agent.learn,
                                       args=(a, agent.shapes, weights_queue, experience_queue))
            agents.append(agent_process)
            agent_process.start()

        print(f"Starting training epoch: {i}")
        experiences = []
        while True:
            try:
                data = experience_queue.get(timeout=60)
                experiences.append(data)
            except queue.Empty:
                print("Empty queue")
            except EOFError:
                print("Queue read error")

            if len(experiences) >= Agent.EXP_COUNTER * num_agents:
                break  # when collect all

        # Fin
        for agent in agents:
            agent.join()

        # Update the main model based on the experiences collected from agents.
        print(f'Epoch {i} finished. Updating main model weights')
        main_model.train_step(experiences)

        if i > 0 and i % 5 == 0:  # save interval - 5 epochs
            epoch_dir = f'epoch_{i}/'
            main_model.save_weights(Agent.SAVE_DIR+epoch_dir+Agent.SAVE_FILE)

    # Save last epoch in main localization
    main_model.save_weights(Agent.SAVE_DIR + Agent.SAVE_FILE)


if __name__ == "__main__":
    print("This module is not fully implemented yet")
    config.GameSetup.set_mode(config.GameMode.API_LEARN)
    mp.set_start_method('spawn')

    pygame.init()
    pygame.display.set_mode((1, 1), pygame.NOFRAME)

    main()

    pygame.quit()

    print("Done!")
