import multiprocessing as mp
import os
import queue

import tensorflow as tf

from a3c import Agent
from new_game.consts import SCREEN_WIDTH, SCREEN_HEIGHT, MINIMAP_ONE_PIXEL


def update_model(experiences, model):
    """
    Updates the main model based on the experiences collected from agents.

    Args:
    experiences (list): A list of experiences collected by agents. Each experience is a tuple
    (state, action, advantage, reward).
    model (A3CModel): An instance of the A3C model that will be updated.
    """
    # Prepare data
    states, actions, advantages, rewards = zip(*experiences)
    env_state, plr_state = zip(*states)
    state_env_tensor = tf.convert_to_tensor([env_state], dtype=tf.float32)
    state_plr_tensor = tf.convert_to_tensor([plr_state], dtype=tf.float32)
    actions = tf.convert_to_tensor(actions, dtype=tf.int32)
    advantages = tf.convert_to_tensor(advantages, dtype=tf.float32)
    rewards = tf.convert_to_tensor(rewards, dtype=tf.float32)

    print(f'Rewards: {rewards}')

    with tf.GradientTape() as tape:
        action_probs, values = model((state_env_tensor, state_plr_tensor), training=True)

        # actor loss
        action_log_probs = tf.math.log(action_probs)
        action_indices = tf.range(0, tf.shape(action_log_probs)[0]) * tf.shape(action_log_probs)[1] + actions
        selected_action_log_probs = tf.gather(tf.reshape(action_log_probs, [-1]), action_indices)
        actor_loss = -tf.reduce_mean(selected_action_log_probs * advantages)

        # critic loss
        critic_loss = tf.keras.losses.mean_squared_error(rewards, tf.squeeze(values))

        total_loss = actor_loss + critic_loss

    grads = tape.gradient(total_loss, model.trainable_variables)
    grads, _ = tf.clip_by_global_norm(grads, clip_norm=1.0)
    model.optimizer.apply_gradients(zip(grads, model.trainable_variables))


def main():
    env_state_shape = (SCREEN_WIDTH // MINIMAP_ONE_PIXEL, SCREEN_HEIGHT // MINIMAP_ONE_PIXEL, 1)
    plr_state_shape = 5  # position_x, position_y, velocity, jump_velocity, direction
    action_space = 5  # NO_ACTION = 0 STOP_MOVE = 1 RUN_LEFT = 2 RUN_RIGHT = 3 JUMP = 4
    num_agents = 16

    main_model = Agent(env_state_shape, plr_state_shape, action_space)
    weights_queue = mp.Queue()
    experience_queue = mp.Queue()

    print("Creating Agents")
    agents = []
    for i in range(num_agents):
        weights_queue.put(main_model.model.get_weights())
        agent = Agent(env_state_shape, plr_state_shape, action_space)
        agent_process = mp.Process(target=agent.learn,
                                   args=(i, weights_queue, experience_queue))
        agents.append(agent_process)
        agent_process.start()

    print("Starting training")
    experiences = []
    while True:
        try:
            data = experience_queue.get_nowait()
            experiences.append(data)
        except queue.Empty:
            print("Kolejka jest pusta")
        except EOFError:
            print("Błąd EOF przy próbie odczytu z kolejki")

        if len(experiences) == main_model.EXP_COUNTER * num_agents:
            break  # when collect all

        new_weights = main_model.model.get_weights()
        for _ in range(num_agents):
            weights_queue.put(new_weights)

    # Fin
    for agent in agents:
        agent.join()

    update_model(experiences, main_model.model)


if __name__ == "__main__":
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    print("This module is not fully implemented yet")
    main()
