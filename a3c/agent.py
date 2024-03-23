import tensorflow as tf

from a3c import A3CModel
from environment import Environment


class Agent:
    EXP_COUNTER = 500  # how many experiences (actions in game)
    SAVE_DIR = './saves/'
    SAVE_FILE = 'a3c_model'

    def __init__(self, env_state_shape, player_state_shape, action_space):
        self.env_state_shape = env_state_shape
        self.player_state_shape = player_state_shape
        self.action_space = action_space

    @property
    def shapes(self):
        return self.env_state_shape, self.player_state_shape, self.action_space

    @staticmethod
    def save_model(model, save_dir=SAVE_DIR+SAVE_FILE):
        model.save_weights(save_dir)

    @staticmethod
    def load_model(model, save_dir=SAVE_DIR+SAVE_FILE):
        model.load_weights(save_dir)

    @staticmethod
    def choose_action(states, model):
        env_state, plr_state = states
        state_env_tensor = tf.convert_to_tensor([env_state], dtype=tf.float32)
        state_plr_tensor = tf.convert_to_tensor([plr_state], dtype=tf.float32)
        action_probs, value = model((state_env_tensor, state_plr_tensor), training=False)
        action = tf.random.categorical(tf.math.log(action_probs), 1)[0, 0]
        return action.numpy(), value

    @staticmethod
    def learn(agent_id, shapes, model_weights_queue, experience_queue, gamma=0.98):
        env_state_shape, player_state_shape, action_space = shapes
        model = A3CModel(env_state_shape, player_state_shape, action_space)
        env = Environment()
        env_state, plr_state = env.reset()
        model((tf.convert_to_tensor([env_state], dtype=tf.float32), tf.convert_to_tensor([plr_state], dtype=tf.float32)))
        new_weights = model_weights_queue.get(timeout=60)
        model.set_weights(new_weights)

        episode = 0
        while episode < Agent.EXP_COUNTER:
            done = False
            states = env.reset()
            env_state, plr_state = states
            while not done and episode < Agent.EXP_COUNTER:
                action, value = Agent.choose_action(states, model)
                next_env_state, next_plr_state, reward, done = env.step(action)
                _, next_value = model((tf.convert_to_tensor([next_env_state], dtype=tf.float32),
                                       tf.convert_to_tensor([next_plr_state], dtype=tf.float32)))

                if done:
                    reward -= 10

                target_value = reward + (1 - done) * gamma * next_value
                advantage = target_value - value

                one_hot_action = tf.one_hot(action, depth=action_space)

                experience = (env_state, plr_state, one_hot_action, advantage.numpy(), reward)
                experience_queue.put(experience)  # ((agent_id, experience))

                states = (next_env_state, next_plr_state)
                episode += 1

        tf.keras.backend.clear_session()

