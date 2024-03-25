# The idea is to get data from environment as 40x30 'image' (real is 1000x750 but one pixel from map is 25 size)
# This image is analyzed via CNN and data about player (velocity, direction, position etc.) are analyzed via DNN
import os

import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPool2D, Flatten, Concatenate, LeakyReLU
from tensorflow.keras.preprocessing.image import img_to_array, load_img


class A3CModel(Model):
    LEARNING_RATE = 0.001
    CLIP_NORM = 10.0
    COMMON_LAYER_UNITS = 32
    COMMON_LAYER_ACTIVATION = 'relu'

    def __init__(self, map_input_shape, plr_input_shape, action_space_size):
        super(A3CModel, self).__init__()
        self.map_nn = self.create_map_nn(map_input_shape)
        self.plr_nn = self.create_plr_nn(plr_input_shape)
        self.action_space_size = action_space_size

        # Create layers for join both NN
        self.combined_output = Concatenate()
        self.flatten = Flatten()

        # Create actor critic common and output layers
        self.common_dense = Dense(self.COMMON_LAYER_UNITS, activation=self.COMMON_LAYER_ACTIVATION)
        self.actor_out = Dense(action_space_size, activation='softmax')
        self.critic_out = Dense(1, activation='linear')

        self.optimizer = tf.keras.optimizers.Adam(learning_rate=self.LEARNING_RATE)

    # TODO change if cnn stay
    def call(self, inputs: tuple) -> tuple:
        cnn_input, dnn_input = inputs  # states

        flatten = self.flatten(cnn_input)

        # Inputs goes thru both nn
        cnn_output = self.map_nn(flatten)
        dnn_output = self.plr_nn(dnn_input)

        combined_output = self.combined_output([cnn_output, dnn_output])
        common_output = self.common_dense(combined_output)

        # Actor & critic output - Policy & Value
        actor_output = self.actor_out(common_output)
        critic_output = self.critic_out(common_output)

        return actor_output, critic_output

    def actor_loss(self, advantages, actions, action_probs):
        action_probs = tf.clip_by_value(action_probs, 1e-8, 1 - 1e-8)  # 1e-8 - to prevent log(0) error
        log_probs = tf.math.log(action_probs)
        selected_log_probs = tf.reduce_sum(log_probs * actions, axis=1, keepdims=True)
        advantages = tf.squeeze(advantages, axis=1)
        loss = -tf.reduce_mean(selected_log_probs * advantages)
        return loss

    def critic_loss(self, estimated_values, true_values):
        return tf.keras.losses.mean_squared_error(true_values, estimated_values)

    @tf.function(reduce_retracing=True)
    def train_step(self, experiences):
        env_state, plr_state, actions, advantages, rewards = zip(*experiences)

        one_hot_action = tf.one_hot(actions, depth=self.action_space_size)

        state_env_tensor = tf.convert_to_tensor(env_state, dtype=tf.float32)
        state_plr_tensor = tf.convert_to_tensor(plr_state, dtype=tf.float32)
        advantages = tf.convert_to_tensor(advantages, dtype=tf.float32)
        rewards = tf.convert_to_tensor(rewards, dtype=tf.float32)

        with tf.GradientTape() as tape:
            action_probs, values = self.call((state_env_tensor, state_plr_tensor))

            actor_loss = self.actor_loss(advantages, one_hot_action, action_probs)

            critic_loss = self.critic_loss(rewards, tf.squeeze(values))

            total_loss = actor_loss + critic_loss

        grads = tape.gradient(total_loss, self.trainable_variables)
        grads, _ = tf.clip_by_global_norm(grads, clip_norm=self.CLIP_NORM)
        self.optimizer.apply_gradients(zip(grads, self.trainable_variables))

    @staticmethod
    def create_map_nn(input_shape):
        input_size = input_shape[0]*input_shape[1]*input_shape[2]
        inputs = Input(shape=(input_size,))
        x = Dense(256)(inputs)
        x = LeakyReLU(alpha=0.1)(x)
        x = Dense(128)(x)
        x = LeakyReLU(alpha=0.1)(x)
        return Model(inputs, x, name='dnn_submodel')

    @staticmethod
    def create_map_cnn(input_shape):
        inputs = Input(shape=input_shape)
        x = Conv2D(16, (3, 3))(inputs)
        x = LeakyReLU(alpha=0.1)(x)
        x = Conv2D(32, (1, 1))(x)
        x = LeakyReLU(alpha=0.1)(x)
        x = MaxPool2D()(x)
        x = Conv2D(32, (1, 1))(x)
        x = LeakyReLU(alpha=0.1)(x)
        return Model(inputs, x, name='cnn_submodel')

    @staticmethod
    def create_plr_nn(input_shape):
        inputs = Input(shape=(input_shape,))
        x = Dense(64)(inputs)
        x = LeakyReLU(alpha=0.1)(x)
        x = Dense(64)(x)
        x = LeakyReLU(alpha=0.1)(x)
        return Model(inputs, x, name='dnn_submodel')

    @staticmethod
    def visualize_feature_maps(model, input_map, output_dir='feature_maps'):

        feature_maps = model.map_nn.predict(input_map)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for i in range(feature_maps.shape[-1]):
            plt.figure(figsize=(2, 2))
            plt.imshow(feature_maps[0, :, :, i], cmap='viridis')
            plt.axis('off')
            plt.savefig(f'{output_dir}/feature_map_{i}.png')
            plt.close()
