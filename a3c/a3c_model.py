# The idea is to get data from environment as 40x30 'image' (real is 1000x750 but one pixel from map is 25 size)
# This image is analyzed via CNN and data about player (velocity, direction, position etc.) are analyzed via DNN

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Conv2D, Flatten, Concatenate


class A3CModel(Model):
    COMMON_LAYER_UNITS = 512
    COMMON_LAYER_ACTIVATION = 'relu'  # TODO later check tanh

    def __init__(self, cnn_input_shape, dnn_input_shape, action_space):
        super(A3CModel, self).__init__()
        self.cnn = self.create_cnn(cnn_input_shape)
        self.dnn = self.create_dnn(dnn_input_shape)
        self.action_space = action_space

        # Create actor critic
        self.common_dense = Dense(self.COMMON_LAYER_UNITS, activation=self.COMMON_LAYER_ACTIVATION)
        self.actor_out = Dense(action_space, activation='softmax')
        self.critic_out = Dense(1)

    def call(self, inputs: tuple):
        cnn_input, dnn_input = inputs

        # Inputs goes thru both nn
        cnn_output = self.cnn(cnn_input)
        dnn_output = self.dnn(dnn_input)

        combined_output = Concatenate()([cnn_output, dnn_output])
        common_output = self.common_dense(combined_output)

        # Actor & critic output
        actor_output = self.actor_out(common_output)
        critic_output = self.critic_out(common_output)

        return actor_output, critic_output

    def create_cnn(self, input_shape):
        # TODO need to do some experiments (MaxPool ?)
        inputs = Input(shape=input_shape)
        x = Conv2D(32, (3, 3), activation='relu')(inputs)
        x = Conv2D(64, (3, 3), activation='relu')(x)
        x = Flatten()(x)
        return Model(inputs, x, name='cnn_submodel')

    def create_dnn(self, input_shape):
        inputs = Input(shape=(input_shape,))
        x = Dense(512, activation='relu')(inputs)
        x = Dense(512, activation='relu')(x)
        return Model(inputs, x, name='dnn_submodel')
