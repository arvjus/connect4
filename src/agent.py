
from base import Connect4Base

class Agent(Connect4Base):
    def __init__(self, config):
        super().__init__(config)
        self.piece = 0

    def name(self):
        pass

    def move(self, board):
        pass

    def game_over(self, winner):
        pass

    def setup(self, piece):
        self.piece = piece

    def teardown(self):
        pass
