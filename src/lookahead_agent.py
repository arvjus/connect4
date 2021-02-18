
from agent import Agent
import random

class LookaheadAgent(Agent):
    def __init__(self, config):
        super().__init__(config)

    def score_move(self, grid, col):
        pass

    # Helper function for get_heuristic: checks if window satisfies heuristic conditions
    def check_window(self, window, num_discs, piece):
        return (window.count(piece) == num_discs and window.count(0) == self.config.inarow - num_discs)

    # Helper function for get_heuristic: counts number of windows satisfying specified heuristic conditions
    def count_windows(self, grid, num_discs, piece):
        num_windows = 0
        # horizontal
        for row in range(self.config.rows):
            for col in range(self.config.columns - (self.config.inarow - 1)):
                window = list(grid[row, col:col + self.config.inarow])
                if self.check_window(window, num_discs, piece):
                    num_windows += 1
        # vertical
        for row in range(self.config.rows - (self.config.inarow - 1)):
            for col in range(self.config.columns):
                window = list(grid[row:row + self.config.inarow, col])
                if self.check_window(window, num_discs, piece):
                    num_windows += 1
        # positive diagonal
        for row in range(self.config.rows - (self.config.inarow - 1)):
            for col in range(self.config.columns - (self.config.inarow - 1)):
                window = list(grid[range(row, row + self.config.inarow), range(col, col + self.config.inarow)])
                if self.check_window(window, num_discs, piece):
                    num_windows += 1
        # negative diagonal
        for row in range(self.config.inarow - 1, self.config.rows):
            for col in range(self.config.columns - (self.config.inarow - 1)):
                window = list(grid[range(row, row - self.config.inarow, -1), range(col, col + self.config.inarow)])
                if self.check_window(window, num_discs, piece):
                    num_windows += 1
        return num_windows

    # Helper function for score_move: calculates value of heuristic for grid
    def get_heuristic(self, grid, mark):
        num_twos = self.count_windows(grid, 2, mark)
        num_threes = self.count_windows(grid, 3, mark)
        num_fours = self.count_windows(grid, 4, mark)
        num_fives = self.count_windows(grid, 5, mark)
        num_twos_opp = self.count_windows(grid, 2, mark % 2 + 1)
        num_threes_opp = self.count_windows(grid, 3, mark % 2 + 1)
        num_fours_opp = self.count_windows(grid, 4, mark % 2 + 1)
        num_fives_opp = self.count_windows(grid, 5, mark % 2 + 1)
        return 1e5 * num_fives + 1e5 * num_fours + 10 * num_threes + num_twos - num_twos_opp - 100 * num_threes_opp - 1e4 * num_fours_opp - 1e4 * num_fives_opp

    def move(self, board):
        # Get list of valid moves
        valid_moves = self.valid_moves(board)
        if len(valid_moves) == 0:
            return None
        # Use the heuristic to assign a score to each possible board in the next turn
        scores = dict(zip(valid_moves, [self.score_move(board, col) for col in valid_moves]))
        # Get a list of columns (moves) that maximize the heuristic
        max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
        # Select at random from the maximizing columns
        return random.choice(max_cols)
