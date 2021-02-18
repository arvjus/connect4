
from agent import Agent
import random

class SimpleAgent(Agent):
    def __init__(self, config):
        super().__init__(config)

    def name(self):
        return "Simple"

    def move(self, board):
        op_piece = self.piece % 2 + 1
        valid_moves = self.valid_moves(board)
        if len(valid_moves) == 0:
            return None
        for col in valid_moves:
            if self.check_if_winning(self.drop_piece(board, col, self.piece), self.piece) or \
                    self.check_if_winning(self.drop_piece(board, col, op_piece), op_piece):
                return col
        return random.choice(valid_moves)
