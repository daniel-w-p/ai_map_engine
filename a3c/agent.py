import os
import numpy as np
import pandas as pd
import tensorflow as tf
from matplotlib import pyplot as plt

from a3c import A3CModel
from environment import Environment


class Agent:
    EXP_COUNTER = 2000  # how many experiences (actions in game)
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
    def save_model(model, save_file=SAVE_DIR+SAVE_FILE):
        model.save_weights(save_file)

    @staticmethod
    def load_model(model, load_file=SAVE_DIR+SAVE_FILE):
        if os.path.exists(load_file+'.index'):
            model.load_weights(load_file)
            print("Weights loaded successfully.")
        else:
            print("Weights file does not exist.")

    @staticmethod
    def choose_action(states, model, play=False, epsilon=0.15):
        env_state, plr_state = states
        state_env_tensor = tf.convert_to_tensor([env_state], dtype=tf.float32)
        state_plr_tensor = tf.convert_to_tensor([plr_state], dtype=tf.float32)

        action_probs, value = model((state_env_tensor, state_plr_tensor), training=False)
        random_value = tf.random.uniform([], minval=0, maxval=1, dtype=tf.float32)

        if play or random_value > epsilon * 2:
            # action = tf.random.categorical(tf.math.log(action_probs), 1)[0, 0]
            action = tf.argmax(action_probs, axis=-1)[0]
        else:
            if random_value < epsilon:
                action = tf.random.uniform([1], minval=0, maxval=action_probs.shape[-1], dtype=tf.int64)[0]
            else:
                action = tf.random.categorical(tf.math.log(action_probs), 1)[0, 0]
        return action.numpy(), value

    @staticmethod
    def unpack_exp_and_step(model, experiences, action_space, epoch):
        env_state, plr_state, actions, advantages, rewards, next_val = zip(*experiences)

        # one_hot_action = tf.one_hot(actions, depth=action_space)
        # env_state = tf.convert_to_tensor(env_state, dtype=tf.float32)
        # plr_state = tf.convert_to_tensor(plr_state, dtype=tf.float32)
        # advantages = tf.convert_to_tensor(advantages, dtype=tf.float32)
        # rewards = tf.convert_to_tensor(rewards, dtype=tf.float32)
        # next_val = tf.convert_to_tensor(next_val, dtype=tf.float32)

        actions = np.array(actions)
        advantages = np.array(advantages)
        rewards = np.array(rewards)
        next_val = np.array(next_val)
        e_states = np.array(env_state)
        p_states = np.array(plr_state)

        actions = actions.reshape(-1, 1).astype(np.float32)
        advantages = advantages.reshape(-1, 1).astype(np.float32)
        rewards = rewards.reshape(-1, 1).astype(np.float32)
        next_val = next_val.reshape(-1, 1).astype(np.float32)

        e_states = e_states.reshape(-1, e_states.shape[-3], e_states.shape[-2], e_states.shape[-1])
        p_states = p_states.reshape(-1, p_states.shape[-2], p_states.shape[-1])

        # create training batches
        dim = len(experiences)
        shuffled_indices = np.random.permutation(dim)
        shuffled_actions = actions[shuffled_indices]
        shuffled_advantages = advantages[shuffled_indices]
        shuffled_rewards = rewards[shuffled_indices]
        shuffled_next_val = next_val[shuffled_indices]
        shuffled_e_states = e_states[shuffled_indices]
        shuffled_p_states = p_states[shuffled_indices]
        split_actions = np.array_split(shuffled_actions, 10)
        split_advantages = np.array_split(shuffled_advantages, 10)
        split_rewards = np.array_split(shuffled_rewards, 10)
        split_next_val = np.array_split(shuffled_next_val, 10)
        split_e_states = np.array_split(shuffled_e_states, 10)
        split_p_states = np.array_split(shuffled_p_states, 10)

        actor_loss, critic_loss, total_loss = [], [], []
        for e_states, p_states, action, advantages, rewards, next_val in zip(split_e_states, split_p_states, split_actions, split_advantages,
                                                                    split_rewards, split_next_val):
            one_hot_action = tf.one_hot(action, depth=action_space)

            a, c, t = model.train_step(e_states, p_states, one_hot_action, advantages, rewards, next_val, epoch)
            actor_loss.append(a)
            critic_loss.append(c)
            total_loss.append(t)
        return np.mean(actor_loss), np.mean(critic_loss), np.mean(total_loss)

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
        end_game_penalty = -15
        local_experience = []

        while episode < Agent.EXP_COUNTER:
            states = env.reset()
            action, value = Agent.choose_action(states, model)
            next_env_state, next_plr_state, reward, done = env.step(action)
            last_reward = reward
            while not done and episode < Agent.EXP_COUNTER:
                action, value = Agent.choose_action(states, model)
                next_env_state, next_plr_state, reward, done = env.step(action)
                _, next_value = model((tf.convert_to_tensor([next_env_state], dtype=tf.float32),
                                       tf.convert_to_tensor([next_plr_state], dtype=tf.float32)))

                # reward, last_reward = reward - last_reward, reward  # check without of this

                target_value = reward + (1 - done) * gamma * next_value + int(done) * end_game_penalty
                advantage = target_value - value

                env_state, plr_state = states
                experience = (env_state, plr_state, action, advantage.numpy(), reward, next_value)
                experience_queue.put(experience)  # ((agent_id, experience))
                local_experience.append(experience)

                states = (next_env_state, next_plr_state)
                episode += 1

        tf.keras.backend.clear_session()

    @staticmethod
    def save_losses_csv(actor_losses, critic_losses, total_losses, output_dir='data/losses'):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        losses_df = pd.DataFrame({
            'Actor Loss': actor_losses,
            'Critic Loss': critic_losses,
            'Total Loss': total_losses
        })
        file = os.path.join(output_dir, 'losses.csv')
        # save to file
        losses_df.to_csv(file, index=False)

    @staticmethod
    def plot_losses(actor_losses, critic_losses, total_losses, output_dir='data/losses'):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file = os.path.join(output_dir, 'losses.png')

        plt.figure(figsize=(5, 5))
        plt.plot(actor_losses, label='Actor Loss')
        plt.plot(critic_losses, label='Critic Loss')
        plt.plot(total_losses, label='Total Loss')
        plt.xlabel('Steps')
        plt.ylabel('Loss')
        plt.title('Losses over Time')
        plt.legend()
        plt.savefig(file)
        plt.close()

    @staticmethod
    def visualize_feature_maps(model, input_map, output_dir='data/feature_maps'):

        feature_maps = model.map_nn.predict(input_map)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for i in range(feature_maps.shape[-1]):
            plt.figure(figsize=(2, 2))
            plt.imshow(feature_maps[0, :, :, i], cmap='viridis')
            plt.axis('off')
            plt.savefig(f'{output_dir}/feature_map_{i}.png')
            plt.close()

