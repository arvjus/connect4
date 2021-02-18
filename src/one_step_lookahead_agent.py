
from lookahead_agent import LookaheadAgent
import random

class OneStepLookaheadAgent(LookaheadAgent):
    def __init__(self, config):
        super().__init__(config)

    def name(self):
        return "One step lookahead"

    # Calculates score if agent drops piece in selected column
    def score_move(self, grid, col):
        next_grid = self.drop_piece(grid, col, self.piece)
        return self.get_heuristic(next_grid, self.piece)
