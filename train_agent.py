import multiprocessing as mp
import numpy as np

from a3c import A3CModel, Agent


def main():
    env_state_shape = (40, 30)
    plr_state_shape = (5,)  # position_x, position_y, velocity, jump_velocity, direction
    action_space = 5  # NO_ACTION = 0 STOP_MOVE = 1 RUN_LEFT = 2 RUN_RIGHT = 3 JUMP = 4
    num_agents = 16

    main_model = Agent(env_state_shape, plr_state_shape, action_space)
    weights_queue = mp.Queue()
    experience_queue = mp.Queue()

    # Agents initialization
    agents = []
    for i in range(num_agents):
        weights_queue.put(main_model.model.get_weights())
        agent = Agent(env_state_shape, plr_state_shape, action_space)
        agent_process = mp.Process(target=agent.learn,
                                   args=(i, weights_queue, experience_queue))
        agents.append(agent_process)
        agent_process.start()

    # Collect data
    experiences = []
    while True:
        data = experience_queue.get()  # Block until data available
        experiences.append(data)

        if len(experiences) == main_model.EXP_COUNTER * num_agents:
            break  # when collect all

    # TODO Model actualization

    # Fin
    for agent in agents:
        agent.join()


if __name__ == "__main__":
    print("This module is not fully implemented yet")
    main()
