import multiprocessing as mp
import numpy as np

from a3c import A3CModel


EXP_COUNTER = 100


def agent_process(agent_id, env_state_shape, player_state_shape, action_space, model_weights_queue, experience_queue):
    # Build model and set weights as in main model
    model = A3CModel(env_state_shape, player_state_shape, action_space)
    model.set_weights(model_weights_queue.get())

    # Simulation
    for _ in range(EXP_COUNTER):
        # TODO State and predict

        # TODO Interaction and experience

        # TODO Collect experience
        experience_queue.put(agent_id)  # data (id, state, action, value))


def main():
    env_state_shape = (40, 30)
    plr_state_shape = (5,)  # position_x, position_y, velocity, jump_velocity, direction
    action_space = 6  # LEFT_DOWN, LEFT_UP, RIGHT_DOWN, RIGHT_UP, JUMP_DOWN, JUMP_UP
    num_agents = 16

    model = A3CModel(env_state_shape, plr_state_shape, action_space)
    weights_queue = mp.Queue()
    experience_queue = mp.Queue()

    # Agents initialization
    agents = []
    for i in range(num_agents):
        weights_queue.put(model.get_weights())
        agent = mp.Process(target=agent_process,
                           args=(i, env_state_shape, plr_state_shape, action_space, weights_queue, experience_queue))
        agents.append(agent)
        agent.start()

    # Collect data
    experiences = []
    while True:
        data = experience_queue.get()  # Block until data available
        experiences.append(data)

        if len(experiences) == EXP_COUNTER * num_agents:
            break  # when collect all

    # TODO Model actualization

    # Fin
    for agent in agents:
        agent.join()


if __name__ == "__main__":
    print("This module is not fully implemented yet")
    main()
