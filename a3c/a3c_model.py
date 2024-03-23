# The idea is to get data from environment as 40x30 'image' (real is 1000x750 but one pixel from map is 25 size)
# This image is analyzed via CNN and data about player (velocity, direction, position etc.) are analyzed via DNN

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPool2D, Flatten, Concatenate


class A3CModel(Model):
    LEARNING_RATE = 0.0005
    COMMON_LAYER_UNITS = 32
    COMMON_LAYER_ACTIVATION = 'relu'

    def __init__(self, cnn_input_shape, dnn_input_shape, action_space_size):
        super(A3CModel, self).__init__()
        self.cnn = self.create_cnn(cnn_input_shape)
        self.dnn = self.create_dnn(dnn_input_shape)
        self.action_space_size = action_space_size

        # Create actor critic common and output layers
        self.common_dense = Dense(self.COMMON_LAYER_UNITS, activation=self.COMMON_LAYER_ACTIVATION)
        self.actor_out = Dense(action_space_size, activation='softmax')
        self.critic_out = Dense(1)

        self.optimizer = tf.keras.optimizers.Adam(learning_rate=self.LEARNING_RATE)

    def call(self, inputs: tuple) -> tuple:
        cnn_input, dnn_input = inputs  # states

        # Inputs goes thru both nn
        cnn_output = self.cnn(cnn_input)
        dnn_output = self.dnn(dnn_input)

        combined_output = Concatenate()([cnn_output, dnn_output])
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

    @tf.function
    def train_step(self, experiences):
        env_state, plr_state, actions, advantages, rewards = zip(*experiences)

        state_env_tensor = tf.convert_to_tensor(env_state, dtype=tf.float32)
        state_plr_tensor = tf.convert_to_tensor(plr_state, dtype=tf.float32)
        advantages = tf.convert_to_tensor(advantages, dtype=tf.float32)
        rewards = tf.convert_to_tensor(rewards, dtype=tf.float32)

        with tf.GradientTape() as tape:
            action_probs, values = self.call((state_env_tensor, state_plr_tensor))

            actor_loss = self.actor_loss(advantages, actions, action_probs)

            critic_loss = self.critic_loss(rewards, tf.squeeze(values))

            total_loss = actor_loss + critic_loss

        grads = tape.gradient(total_loss, self.trainable_variables)
        grads, _ = tf.clip_by_global_norm(grads, clip_norm=1.0)
        self.optimizer.apply_gradients(zip(grads, self.trainable_variables))

    @staticmethod
    def create_cnn(input_shape):
        # TODO need to do some experiments (MaxPool ?)
        inputs = Input(shape=input_shape)
        x = Conv2D(32, (3, 3), activation='relu')(inputs)
        x = Conv2D(32, (3, 3), activation='relu')(x)
        x = MaxPool2D()(x)
        x = Conv2D(16, (3, 3), activation='relu')(x)
        x = Flatten()(x)
        return Model(inputs, x, name='cnn_submodel')

    @staticmethod
    def create_dnn(input_shape):
        inputs = Input(shape=(input_shape,))
        x = Dense(128, activation='relu')(inputs)
        x = Dense(64, activation='relu')(x)
        return Model(inputs, x, name='dnn_submodel')
