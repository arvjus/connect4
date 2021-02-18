
from agent import Agent
import random

class RandomAgent(Agent):
    def __init__(self, config):
        super().__init__(config)

    def name(self):
        return "Random"

    def move(self, board):
        valid_moves = self.valid_moves(board)
        return random.choice(valid_moves) if len(valid_moves) > 0 else None
