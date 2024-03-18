import tensorflow as tf

from a3c import A3CModel
from environment import Environment


class Agent:
    EXP_COUNTER = 2  # how many experiences (game from start to end)
    SAVE_DIR = './saves/a3c_model'

    def __init__(self, env_state_shape, player_state_shape, action_space):
        self.model = A3CModel(env_state_shape, player_state_shape, action_space)
        self.env = Environment()

    def save_model(self):
        self.model.save_weights(self.SAVE_DIR)

    def load_model(self):
        self.model.load_weights(self.SAVE_DIR)

    def choose_action(self, states):
        env_state, plr_state = states
        state_env_tensor = tf.convert_to_tensor([env_state], dtype=tf.float32)
        state_plr_tensor = tf.convert_to_tensor([plr_state], dtype=tf.float32)
        action_probs, _ = self.model((state_env_tensor, state_plr_tensor))
        action = tf.random.categorical(tf.math.log(action_probs), 1)[0, 0]
        return action.numpy()

    def learn(self, agent_id, model_weights_queue, experience_queue, gamma=0.99):
        self.model.set_weights(model_weights_queue.get())
        print("Agent ", agent_id, " is running")
        for episode in range(self.EXP_COUNTER):
            print("episode ", episode, " start")
            done = False
            states = self.env.reset()
            env_state, plr_state = states
            while not done:
                action = self.choose_action(states)
                next_env_state, next_plr_state, reward, done = self.env.step(action)
                value, _ = self.model((tf.convert_to_tensor([env_state], dtype=tf.float32), tf.convert_to_tensor([plr_state], dtype=tf.float32)))
                next_value, _ = self.model((tf.convert_to_tensor([next_env_state], dtype=tf.float32), tf.convert_to_tensor([next_plr_state], dtype=tf.float32)))

                if done:
                    reward -= 10  # end game punishment

                target_value = reward + (1 - done) * gamma * next_value
                advantage = target_value - value

                experience = (states, action, advantage.numpy(), reward)
                experience_queue.put((agent_id, experience))

                states = (next_env_state, next_plr_state)

