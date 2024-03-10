# The idea is to get data from environment as 40x30 'image' (real is 1000x750 but one pixel from map is 25 size)
# This image is analyzed via CNN and data about player (velocity, direction, position etc.) are analyzed via DNN

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Conv2D, Flatten, Concatenate


class A3CModel(Model):
    def __init__(self, cnn_input_shape, dnn_input_shape, action_space):
        super(A3CModel, self).__init__()
        self.cnn = self.create_cnn(cnn_input_shape)
        self.dnn = self.create_dnn(dnn_input_shape)
        self.action_space = action_space

        # Create actor critic
        # TODO
        self.actor_dense = Dense(action_space, activation='softmax')
        self.critic_dense = Dense(1)

    def call(self, inputs):
        cnn_input, dnn_input = inputs

        # Inputs goes thru both nn
        cnn_output = self.cnn(cnn_input)
        dnn_output = self.dnn(dnn_input)

        combined_output = Concatenate()([cnn_output, dnn_output])

        # Actor & critic
        # TODO
        actor_output = self.actor_dense(combined_output)
        critic_output = self.critic_dense(combined_output)

        return actor_output, critic_output

    def create_cnn(self, input_shape):
        # TODO
        inputs = Input(shape=input_shape)
        x = Conv2D(32, (3, 3), activation='relu')(inputs)
        x = Conv2D(64, (3, 3), activation='relu')(x)
        x = Flatten()(x)
        return Model(inputs, x, name='cnn_submodel')

    def create_dnn(self, input_shape):
        # TODO
        inputs = Input(shape=(input_shape,))
        x = Dense(64, activation='relu')(inputs)
        x = Dense(64, activation='relu')(x)
        return Model(inputs, x, name='dnn_submodel')