import tensorflow as tf

from a3c import A3CModel


class Agent:
    EXP_COUNTER = 100  # how many experiences

    def __init__(self, env_state_shape, player_state_shape, action_space):
        self.model = A3CModel(env_state_shape, player_state_shape, action_space)

    def learn(self, agent_id, model_weights_queue, experience_queue):
        # Set weights as in main model
        self.model.set_weights(model_weights_queue.get())

        # Simulation
        for _ in range(self.EXP_COUNTER):
            # TODO State and predict

            # TODO Interaction and experience

            # TODO Collect experience
            experience_queue.put(agent_id)  # data (id, state, action, value))
