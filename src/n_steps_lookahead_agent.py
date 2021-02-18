
from lookahead_agent import LookaheadAgent
import numpy as np

class NStepsLookaheadAgent(LookaheadAgent):
    def __init__(self, config, nsteps):
        super().__init__(config)
        self.nsteps = nsteps

    def name(self):
        return "N steps lookahead"

    # Uses minimax to calculate value of dropping piece in selected column
    def score_move(self, grid, col):
        next_grid = self.drop_piece(grid, col, self.piece)
        score = self.minimax(next_grid, self.nsteps - 1, False, self.piece)
        # print("minimax, score=", score, ", col=", col)
        return score

    # Helper function for minimax: checks if agent or opponent has four in a row in the window
    def is_terminal_window(self, window):
        return window.count(1) == self.config.inarow or window.count(2) == self.config.inarow

    # Helper function for minimax: checks if game has ended
    def is_terminal_node(self, grid):
        # Check for draw
        if list(grid[0, :]).count(0) == 0:
            return True

        # Check for win: horizontal, vertical, or diagonal
        # horizontal
        for row in range(self.config.rows):
            for col in range(self.config.columns - (self.config.inarow - 1)):
                window = list(grid[row, col:col + self.config.inarow])
                if self.is_terminal_window(window):
                    return True
        # vertical
        for row in range(self.config.rows - (self.config.inarow - 1)):
            for col in range(self.config.columns):
                window = list(grid[row:row + self.config.inarow, col])
                if self.is_terminal_window(window):
                    return True
        # positive diagonal
        for row in range(self.config.rows - (self.config.inarow - 1)):
            for col in range(self.config.columns - (self.config.inarow - 1)):
                window = list(grid[range(row, row + self.config.inarow), range(col, col + self.config.inarow)])
                if self.is_terminal_window(window):
                    return True
        # negative diagonal
        for row in range(self.config.inarow - 1, self.config.rows):
            for col in range(self.config.columns - (self.config.inarow - 1)):
                window = list(grid[range(row, row - self.config.inarow, -1), range(col, col + self.config.inarow)])
                if self.is_terminal_window(window):
                    return True
        return False

    # Minimax implementation
    def minimax(self, node, depth, maximizingPlayer, mark):
        is_terminal = self.is_terminal_node(node)
        valid_moves = [c for c in range(self.config.columns) if node[0][c] == 0]
        if depth == 0 or is_terminal:
            return self.get_heuristic(node, mark)
        if maximizingPlayer:
            value = -np.Inf
            for col in valid_moves:
                child = self.drop_piece(node, col, mark)
                value = max(value, self.minimax(child, depth - 1, False, mark))
            # print("max, value=", value, ", depth=", depth)
            return value
        else:
            value = np.Inf
            for col in valid_moves:
                child = self.drop_piece(node, col, mark % 2 + 1)
                value = min(value, self.minimax(child, depth - 1, True, mark))
            # print("min, value=", value, ", depth=", depth)
            return value
