import multiprocessing as mp
import os
import queue
import sys

import numpy as np
import pygame
import tensorflow as tf

from a3c import Agent, A3CModel
from environment import Environment
from new_game import Game, GameCrl
from new_game.figures import Player

import setup


def main():
    env_state_shape = Game.env_state_size()
    plr_state_shape = Player.plr_state_size()
    action_space = GameCrl.action_space_size()
    num_agents = 10
    epochs = 15
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
    actor_losses = []
    critic_losses = []
    total_losses = []

    for i in range(epochs):
        print("Creating Agents")
        weights_queue = manager.Queue()
        experience_queue = manager.Queue()
        agents = []
        main_model_weights = main_model.get_weights()

        # Prepare and run agents (multiprocessing)
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

        # For progress monitoring
        total_steps = Agent.EXP_COUNTER * num_agents
        step_size = total_steps // 100
        last_step = 0

        while True:
            try:
                data = experience_queue.get(timeout=60)
                experiences.append(data)
            except queue.Empty:
                print("Empty queue")
            except EOFError:
                print("Queue read error")

            actual_step = len(experiences)

            if actual_step >= total_steps:
                print(f'\rEpoch: {i} --> 100% Complete ')
                print("Total experiences:", len(experiences))
                break  # when collect all

        # Fin
        for agent in agents:
            agent.join()

        # Some logs.
        print(f'Epoch {i} finished. Updating main model weights')
        rewards = [reward for _, _, _, _, reward, _ in experiences]
        print(f'Mean reward: {np.mean(rewards)}')
        print(f'Max reward: {np.max(rewards)}')

        # Update the main model based on the experiences collected from agents.
        actor_loss, critic_loss, total_loss = Agent.unpack_exp_and_step(main_model, experiences, action_space)
        actor_losses.append(actor_loss)
        critic_losses.append(critic_loss)
        total_losses.append(total_loss)

        print(f"Losses:\n t - {total_losses} ;\n a - {actor_losses} ;\n c - {critic_losses}")

        if i > 0 and i % 5 == 0:  # save interval - 5 epochs
            epoch_dir = f'epoch_{i}/'
            main_model.save_weights(Agent.SAVE_DIR+epoch_dir+Agent.SAVE_FILE)
            # Plotting features (CNN)
            if setup.ProjectSetup.MODES["map_nn_mode"] == setup.MapNN.CNN.value:
                Agent.visualize_feature_maps(main_model, tf.convert_to_tensor([env_state], dtype=tf.float32))

    # Save last epoch in main localization
    main_model.save_weights(Agent.SAVE_DIR + Agent.SAVE_FILE)
    # Save losses
    Agent.save_losses_csv(actor_losses, critic_losses, total_losses)
    # Plotting losses and features (CNN)
    Agent.plot_losses(actor_losses, critic_losses, total_losses)
    if setup.ProjectSetup.MODES["map_nn_mode"] == setup.MapNN.CNN.value:
        Agent.visualize_feature_maps(main_model, tf.convert_to_tensor([env_state], dtype=tf.float32))


if __name__ == "__main__":
    print("This module is not fully implemented yet")
    setup.ProjectSetup.set_api_mode(setup.GameMode.API_LEARN)
    mp.set_start_method('spawn')

    pygame.init()
    pygame.display.set_mode((1, 1), pygame.NOFRAME)

    main()

    pygame.quit()

    print("Done!")
