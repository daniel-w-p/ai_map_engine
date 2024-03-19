import tensorflow as tf

from a3c import A3CModel
from environment import Environment


class Agent:
    EXP_COUNTER = 2  # how many experiences (game from start to end)
    SAVE_DIR = './saves/a3c_model'

    def __init__(self, env_state_shape, player_state_shape, action_space):
        self.env_state_shape = env_state_shape
        self.player_state_shape = player_state_shape
        self.action_space = action_space

    @property
    def shapes(self):
        return self.env_state_shape, self.player_state_shape, self.action_space

    @staticmethod
    def save_model(model, save_dir):
        model.save_weights(save_dir)

    @staticmethod
    def load_model(model, save_dir):
        model.load_weights(save_dir)

    @staticmethod
    def choose_action(states, model):
        env_state, plr_state = states
        state_env_tensor = tf.convert_to_tensor([env_state], dtype=tf.float32)
        state_plr_tensor = tf.convert_to_tensor([plr_state], dtype=tf.float32)
        action_probs, _ = model((state_env_tensor, state_plr_tensor))
        action = tf.random.categorical(tf.math.log(action_probs), 1)[0, 0]
        return action.numpy()

    @staticmethod
    def learn(agent_id, shapes, model_weights_queue, experience_queue, gamma=0.99):
        env_state_shape, player_state_shape, action_space = shapes
        print("Agent ", agent_id, " coping weights from main model")
        model = A3CModel(env_state_shape, player_state_shape, action_space)
        env = Environment()
        model.set_weights(model_weights_queue.get(timeout=60))
        print("Agent ", agent_id, " start learning")
        for episode in range(Agent.EXP_COUNTER):
            print("episode ", episode, " start")
            done = False
            states = env.reset()
            env_state, plr_state = states
            while not done:
                action = Agent.choose_action(states, model)
                next_env_state, next_plr_state, reward, done = env.step(action)
                value, _ = model((tf.convert_to_tensor([env_state], dtype=tf.float32), tf.convert_to_tensor([plr_state], dtype=tf.float32)))
                next_value, _ = model((tf.convert_to_tensor([next_env_state], dtype=tf.float32), tf.convert_to_tensor([next_plr_state], dtype=tf.float32)))

                if done:
                    reward -= 10  # end game punishment

                target_value = reward + (1 - done) * gamma * next_value
                advantage = target_value - value

                experience = (env_state, plr_state, action, advantage.numpy(), reward)
                experience_queue.put(experience)  # ((agent_id, experience))

                states = (next_env_state, next_plr_state)

