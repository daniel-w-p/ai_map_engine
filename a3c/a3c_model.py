import os
os.environ['TF_GPU_ALLOCATOR'] = 'cuda_malloc_async'
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, GRU, Conv2D, MaxPool2D, Flatten, Concatenate, LeakyReLU, BatchNormalization
from tensorflow.keras.preprocessing.image import img_to_array, load_img

import setup


# The idea is to get data from environment as 40x30 'image' (real is 1000x750 but one pixel from map is 25 size)
# This image is analyzed via CNN and data about player (velocity, direction, position etc.) are analyzed via DNN


class A3CModel(Model):
    LEARNING_RATE = 0.001
    LEARNING_RATE_DECAY_FACTOR = 0.98
    CLIP_NORM = 20.0

    def __init__(self, map_input_shape, plr_input_shape, action_space_size):
        super(A3CModel, self).__init__()

        self.last_epoch = 0
        self.learning_rate = self.LEARNING_RATE
        self.action_space_size = action_space_size

        # map network
        if setup.ProjectSetup.MODES["map_nn_mode"] == setup.MapNN.DNN.value:
            self.map_nn = self.create_map_nn(map_input_shape)
        else:
            self.map_nn = self.create_map_cnn(map_input_shape)

        # player network
        self.gru = GRU(64, return_sequences=True, return_state=False)
        self.gru_out = GRU(32)

        self.p_dense = Dense(64)
        self.p_activ = LeakyReLU(alpha=0.2)
        self.p_norm = BatchNormalization()

        # Create layers for join both NN
        self.combined_output = Concatenate()
        self.flatten = Flatten()

        # Actor-Critic output
        self.actor_dense = Dense(16)
        self.actor_activation = LeakyReLU(alpha=0.1)
        self.actor_norm = BatchNormalization()
        self.actor_out = Dense(1, activation='sigmoid')

        self.critic_dense = Dense(16)
        self.critic_activation = LeakyReLU(alpha=0.1)
        self.critic_norm = BatchNormalization()
        self.critic_out = Dense(1, activation='linear')

        self.optimizer = tf.keras.optimizers.Adam(learning_rate=self.LEARNING_RATE)

    # TODO change if cnn stay
    def call(self, inputs: tuple) -> tuple:
        cnn_input, dnn_input = inputs  # states

        if setup.ProjectSetup.MODES["map_nn_mode"] == setup.MapNN.DNN.value:
            flatten = self.flatten(cnn_input)
            cnn_output = self.map_nn(flatten)
        else:
            cnn_output = self.map_nn(cnn_input)
            cnn_output = self.flatten(cnn_output)

        dnn_output = self.gru(dnn_input)
        dnn_output = self.gru_out(dnn_output)

        dnn_output = self.p_dense(dnn_output)
        dnn_output = self.p_activ(dnn_output)
        dnn_output = self.p_norm(dnn_output)

        combined_output = self.combined_output([cnn_output, dnn_output])
        common_output = self.common_dense(combined_output)

        # Actor & critic output - Policy & Value
        a_out = self.actor_dense(common_output)
        a_out = self.actor_activation(a_out)
        a_out = self.actor_norm(a_out)

        c_out = self.critic_dense(common_output)
        c_out = self.critic_activation(c_out)
        c_out = self.critic_norm(c_out)

        actor_output = self.actor_out(a_out)
        critic_output = self.critic_out(c_out)
        return actor_output, critic_output

    def actor_loss(self, advantages, actions, action_probs, entropy_beta=0.01):
        action_probs = tf.clip_by_value(action_probs, 1e-8, 1 - 1e-8)
        log_probs = tf.math.log(action_probs)

        selected_log_probs = tf.reduce_sum(log_probs * actions, axis=1, keepdims=True)

        entropy = -tf.reduce_sum(action_probs * log_probs, axis=1)
        mean_entropy = tf.reduce_mean(entropy)

        policy_loss = -tf.reduce_mean(selected_log_probs * advantages)
        loss = policy_loss - entropy_beta * mean_entropy

        return loss

    def critic_loss(self, true_values, estimated_values):
        return tf.keras.losses.mean_squared_error(true_values, estimated_values)

    @tf.function(reduce_retracing=True)
    def train_step(self, env_state, plr_state, one_hot_action, advantages, rewards, next_values, epoch=0, gamma=0.98):
        if epoch != self.last_epoch:
            self.learning_rate = self.learning_rate * (self.LEARNING_RATE_DECAY_FACTOR ** epoch)
            self.optimizer.learning_rate.assign(self.learning_rate)
            self.last_epoch = epoch

        with tf.GradientTape() as tape:
            action_probs, values = self.call((env_state, plr_state))

            actor_loss = self.actor_loss(advantages, one_hot_action, action_probs)

            true_values = rewards + gamma * tf.squeeze(next_values)
            critic_loss = self.critic_loss(true_values, tf.squeeze(values))

            total_loss = actor_loss + critic_loss

        grads = tape.gradient(total_loss, self.trainable_variables)
        grads, _ = tf.clip_by_global_norm(grads, clip_norm=self.CLIP_NORM)
        self.optimizer.apply_gradients(zip(grads, self.trainable_variables))

        return actor_loss, critic_loss, total_loss

    @staticmethod
    def create_map_nn(input_shape):
        input_size = input_shape[0] * input_shape[1] * input_shape[2]
        inputs = Input(shape=(input_size,))
        x = Dense(1024)(inputs)
        x = BatchNormalization()(x)
        x = LeakyReLU(alpha=0.1)(x)
        x = Dense(256)(x)
        x = BatchNormalization()(x)
        x = LeakyReLU(alpha=0.1)(x)
        x = Dense(64)(x)
        x = BatchNormalization()(x)
        x = LeakyReLU(alpha=0.1)(x)
        return Model(inputs, x, name='map_nn_submodel')

    @staticmethod
    # def create_map_cnn(input_shape):
    #     inputs = Input(shape=input_shape)
    #     x = Conv2D(32, (3, 3), padding="SAME")(inputs)
    #     x = Conv2D(64, (3, 3), padding="SAME", strides=2)(x)
    #     x = BatchNormalization()(x)
    #     x = LeakyReLU(alpha=0.1)(x)
    #     x = MaxPool2D()(x)
    #     x = Conv2D(64, (1, 1))(x)
    #     return Model(inputs, x, name='map_cnn_submodel')
    def create_map_cnn(input_shape):
        inputs = Input(shape=input_shape)
        x = Conv2D(32, (3, 3), padding="SAME")(inputs)
        x = Conv2D(64, (3, 3), padding="SAME", strides=2)(x)
        x = BatchNormalization()(x)
        x = LeakyReLU(alpha=0.1)(x)
        x = MaxPool2D()(x)
        x = Conv2D(64, (3, 3), padding="SAME")(x)
        x = Conv2D(128, (3, 3), padding="SAME", strides=2)(x)
        x = BatchNormalization()(x)
        x = LeakyReLU(alpha=0.1)(x)
        x = MaxPool2D()(x)
        x = Conv2D(256, (1, 1))(x)
        return Model(inputs, x, name='map_cnn_submodel')

