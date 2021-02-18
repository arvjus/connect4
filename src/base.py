
class Connect4Base:
    def __init__(self, config):
        self.config = config

    # Returns list of available moves
    def valid_moves(self, board):
        return [col for col in range(self.config.columns) if board[0][col] == 0]

    # Gets board at next step if agent drops piece in selected column
    def drop_piece(self, board, col, piece):
        next_board = board.copy()
        for row in range(self.config.rows - 1, -1, -1):
            if next_board[row][col] == 0:
                break
        next_board[row][col] = piece
        return next_board

    # Returns True if the piece has won
    def check_if_winning(self, board, piece):
        # horizontal
        for row in range(self.config.rows):
            for col in range(self.config.columns - (self.config.inarow - 1)):
                window = list(board[row, col:col + self.config.inarow])
                if window.count(piece) >= self.config.inarow:
                    return True
        # vertical
        for row in range(self.config.rows - (self.config.inarow - 1)):
            for col in range(self.config.columns):
                window = list(board[row:row + self.config.inarow, col])
                if window.count(piece) >= self.config.inarow:
                    return True
        # positive diagonal
        for row in range(self.config.rows - (self.config.inarow - 1)):
            for col in range(self.config.columns - (self.config.inarow - 1)):
                window = list(board[range(row, row + self.config.inarow), range(col, col + self.config.inarow)])
                if window.count(piece) >= self.config.inarow:
                    return True
        # negative diagonal
        for row in range(self.config.inarow - 1, self.config.rows):
            for col in range(self.config.columns - (self.config.inarow - 1)):
                window = list(board[range(row, row - self.config.inarow, -1), range(col, col + self.config.inarow)])
                if window.count(piece) >= self.config.inarow:
                    return True
        return False
