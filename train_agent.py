import multiprocessing as mp
import queue

import pygame

import tensorflow as tf

from a3c import Agent, A3CModel
from new_game import config
from environment import Environment


def update_model(experiences, model):
    """
    Updates the main model based on the experiences collected from agents.

    Args:
    experiences (list): A list of experiences collected by agents. Each experience is a tuple
    (states, action, advantage, reward).
    model (A3CModel): An instance of the A3C model that will be updated.
    """
    # Prepare data
    env_state, plr_state, actions, advantages, rewards = zip(*experiences)
    state_env_tensor = tf.convert_to_tensor(env_state, dtype=tf.float32)
    state_plr_tensor = tf.convert_to_tensor(plr_state, dtype=tf.float32)
    actions = tf.convert_to_tensor(actions, dtype=tf.int32)
    advantages = tf.convert_to_tensor(advantages, dtype=tf.float32)
    rewards = tf.convert_to_tensor(rewards, dtype=tf.float32)

    print(f'Rewards: {rewards}')

    with tf.GradientTape() as tape:
        action_probs, values = model((state_env_tensor, state_plr_tensor), training=True)

        # actor loss
        action_log_probs = tf.math.log(action_probs)
        action_indices = tf.range(0, tf.shape(action_log_probs)[0]) * tf.shape(action_log_probs)[1] + actions
        selected_action_log_probs = tf.gather(action_log_probs, action_indices)
        advantages = tf.squeeze(advantages, axis=1)
        actor_loss = -tf.reduce_mean(selected_action_log_probs * advantages)

        # critic loss
        critic_loss = tf.keras.losses.mean_squared_error(rewards, tf.squeeze(values))

        total_loss = actor_loss + critic_loss

    grads = tape.gradient(total_loss, model.trainable_variables)
    grads, _ = tf.clip_by_global_norm(grads, clip_norm=1.0)
    model.optimizer.apply_gradients(zip(grads, model.trainable_variables))


def main():
    env_state_shape = (config.SCREEN_WIDTH // config.MINIMAP_ONE_PIXEL, config.SCREEN_HEIGHT // config.MINIMAP_ONE_PIXEL, 1)
    plr_state_shape = 5  # position_x, position_y, velocity, jump_velocity, direction
    action_space = 5  # NO_ACTION = 0 STOP_MOVE = 1 RUN_LEFT = 2 RUN_RIGHT = 3 JUMP = 4
    num_agents = 8
    start_from_checkpoint = True

    # Dynamic GPU memory allocation for TensorFlow
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError as e:
            print(e)

    main_model = A3CModel(env_state_shape, plr_state_shape, action_space)
    if start_from_checkpoint:
        print("Loading checkpoint...")
        main_model.load_weights(Agent.SAVE_DIR)

    manager = mp.Manager()
    weights_queue = manager.Queue()
    experience_queue = manager.Queue()

    print("Creating Agents")
    agents = []
    main_model_weights = main_model.get_weights()
    for i in range(num_agents):
        weights_queue.put(main_model_weights)
        print("Creating Agent ", i)
        agent = Agent(env_state_shape, plr_state_shape, action_space)
        agent_process = mp.Process(target=Agent.learn,
                                   args=(i, agent.shapes, weights_queue, experience_queue))
        agents.append(agent_process)
        agent_process.start()

    print("Starting training")
    experiences = []
    while True:
        try:
            data = experience_queue.get(timeout=60)
            experiences.append(data)
        except queue.Empty:
            print("Empty queue")
        except EOFError:
            print("Queue read error")

        if len(experiences) == Agent.EXP_COUNTER * num_agents:
            break  # when collect all

    # Fin
    for agent in agents:
        agent.join()

    update_model(experiences, main_model)
    main_model.save_weights(Agent.SAVE_DIR)


if __name__ == "__main__":
    print("This module is not fully implemented yet")
    mp.set_start_method('spawn')

    pygame.init()
    pygame.display.set_mode((1, 1), pygame.NOFRAME)

    main()

    pygame.quit()

    print("Done!")
