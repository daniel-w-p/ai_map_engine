# The idea is to get data from environment as 40x30 'image' (real is 1000x750 but one pixel from map is 25 size)
# This image is analyzed via CNN and data about player (velocity, direction, position etc.) are analyzed via DNN

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPool2D, Flatten, Concatenate, LeakyReLU, BatchNormalization
from tensorflow.keras.preprocessing.image import img_to_array, load_img

import setup


class A3CModel(Model):
    LEARNING_RATE = 0.001
    CLIP_NORM = 10.0
    COMMON_LAYER_UNITS = 64
    COMMON_LAYER_ACTIVATION = 'tanh'

    def __init__(self, map_input_shape, plr_input_shape, action_space_size):
        super(A3CModel, self).__init__()
        if setup.ProjectSetup.MODES["map_nn_mode"] == setup.MapNN.DNN:
            self.map_nn = self.create_map_nn(map_input_shape)
        else:
            self.map_nn = self.create_map_cnn(map_input_shape)

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

        if setup.ProjectSetup.MODES["map_nn_mode"] == setup.MapNN.DNN:
            flatten = self.flatten(cnn_input)

            # Inputs goes thru both nn
            cnn_output = self.map_nn(flatten)
            dnn_output = self.plr_nn(dnn_input)
        else:
            cnn_output = self.map_nn(cnn_input)
            dnn_output = self.plr_nn(dnn_input)

            cnn_output = self.flatten(cnn_output)

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
    def train_step(self, env_state, plr_state, one_hot_action, advantages, rewards):

        with tf.GradientTape() as tape:
            action_probs, values = self.call((env_state, plr_state))

            actor_loss = self.actor_loss(advantages, one_hot_action, action_probs)

            critic_loss = self.critic_loss(rewards, tf.squeeze(values))

            total_loss = actor_loss + critic_loss

        grads = tape.gradient(total_loss, self.trainable_variables)
        grads, _ = tf.clip_by_global_norm(grads, clip_norm=self.CLIP_NORM)
        self.optimizer.apply_gradients(zip(grads, self.trainable_variables))

        return actor_loss, critic_loss, total_loss

    @staticmethod
    def create_map_nn(input_shape):
        input_size = input_shape[0]*input_shape[1]*input_shape[2]
        inputs = Input(shape=(input_size,))
        x = Dense(512)(inputs)
        x = LeakyReLU(alpha=0.1)(x)
        x = Dense(256)(x)
        x = LeakyReLU(alpha=0.1)(x)
        x = Dense(64)(x)
        x = LeakyReLU(alpha=0.1)(x)
        return Model(inputs, x, name='map_nn_submodel')

    @staticmethod
    def create_map_cnn(input_shape):
        inputs = Input(shape=input_shape)
        x = Conv2D(16, (5, 5))(inputs)
        x = BatchNormalization()(x)
        x = LeakyReLU(alpha=0.1)(x)
        x = MaxPool2D()(x)
        x = Conv2D(32, (3, 3))(x)
        x = BatchNormalization()(x)
        x = LeakyReLU(alpha=0.1)(x)
        x = MaxPool2D()(x)
        x = Conv2D(64, (1, 1))(x)
        # x = LeakyReLU(alpha=0.1)(x)
        return Model(inputs, x, name='map_cnn_submodel')

    @staticmethod
    def create_plr_nn(input_shape):
        inputs = Input(shape=(input_shape,))
        x = Dense(64)(inputs)
        x = LeakyReLU(alpha=0.1)(x)
        x = Dense(32)(x)
        x = LeakyReLU(alpha=0.1)(x)
        return Model(inputs, x, name='plr_nn_submodel')


