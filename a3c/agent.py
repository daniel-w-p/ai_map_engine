import tensorflow as tf

from a3c import A3CModel


class Agent:
    EXP_COUNTER = 250  # how many experiences (game from start to end)
    SAVE_DIR = './saves/a3c_model'

    def __init__(self, env_state_shape, player_state_shape, action_space):
        # self.env_state_shape = env_state_shape
        # self.player_state_shape = player_state_shape
        # self.action_space = action_space
        self.model = A3CModel(env_state_shape, player_state_shape, action_space)

    def save_model(self):
        self.model.save_weights(self.SAVE_DIR)

    def load_model(self):
        self.model.load_weights(self.SAVE_DIR)

    def learn(self, agent_id, model_weights_queue, experience_queue):
        # Set weights as in main model
        self.model.set_weights(model_weights_queue.get())

        # Simulation
        # TODO first need to work on environment 
        for _ in range(self.EXP_COUNTER):
            # TODO State and predict

            # TODO Interaction and experience

            # TODO Collect experience
            experience_queue.put(agent_id)  # data (id, state, action, value))
