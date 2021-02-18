
import os
import numpy as np
from tensorflow import keras

datadir = "../data"

class Network:
    def __init__(self, model):
        self.model = model

    def setup(self, piece):
        self.model_path = os.path.join(datadir, '{}_{}.h5'.format(self.name(), piece))
        self.log_path = os.path.join(datadir, '{}_{}.csv'.format(self.name(), piece))
        if not os.path.isdir(datadir):
            os.makedirs(datadir)
        if os.path.isfile(self.model_path):
            self.model = keras.models.load_model(self.model_path)
            print('Loaded model from', self.model_path)
        self.log_handle = open(self.log_path, 'a')

    def teardown(self):
        self.model.save(self.model_path)
        print('Model saved to', self.model_path)
        self.log_handle.close()

    def update(self, board_states, rewards):
        inputs = self._board_states_to_inputs(board_states)
        outputs = np.array(rewards)
        self.model.train_on_batch(inputs, outputs)

    def predict(self, board_state):
        input = self._board_states_to_inputs([board_state])
        result = self.model.predict(input)
        return result

    def log(self, text):
        self.log_handle.write(text+'\n')

    def _board_states_to_inputs(self, board_states):
        inputs = np.array(board_states)
        inputs = np.expand_dims(inputs, axis=3)
        return inputs

    def name(self):
        pass
