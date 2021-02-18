from network import Network
from tensorflow import keras
from tensorflow.keras import layers

class Network1(Network):
    def __init__(self):
        model = keras.Sequential([
            layers.Conv2D(128, (4, 4), input_shape=(6, 7, 1), activation='relu'),
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dense(64, activation='relu'),
            layers.Dense(1)
        ])
        model.compile(loss='mean_squared_error',
                      optimizer=keras.optimizers.Adam(),
                      metrics=['accuracy'])
        super().__init__(model)

    def name(self):
        return 'model_128x4_64_64'
