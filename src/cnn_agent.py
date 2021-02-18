
from agent import Agent
import random
import numpy as np

class CNNAgent(Agent):
    def __init__(self, config, network, op_player):
        super().__init__(config)
        self.network = network
        self.op_player = op_player
        self.discount_factor = 0.7
        self.current_game_moves = []
        self.current_batch_board_states = []
        self.current_batch_rewards = []
        self.current_game_rewards = []
        self.batch_size = 100

    def name(self):
        return "CNN"

    def move(self, board):
        move_scores = {}
        valid_moves = self.valid_moves(board)
        for move in valid_moves:
            next_board = self.drop_piece(board, move, self.piece)
            board_state = self._build_board_state(next_board)
            score = self.network.predict(board_state)
            move_scores[move] = (score, board_state)

        max_score = max(move_scores.values(), key=lambda k: k[0])[0]
        moves_with_max_scores = [move for move in move_scores.keys() if move_scores.get(move)[0] == max_score]
        move_to_play = random.choice(moves_with_max_scores)
        board_state = move_scores[move_to_play][1]
        self.current_game_moves.append(board_state)
        return move_to_play

    def game_over(self, winner):
        reward = 1 if winner == self.piece else 0 if winner == 0 else -1

        self.current_game_rewards.append(reward)
        if len(self.current_game_rewards) >= 100:
            self._log_statistics()

        for board_state in reversed(self.current_game_moves):
            self.current_batch_board_states.append(board_state)
            self.current_batch_rewards.append(reward)
            reward *= self.discount_factor
        self.current_game_moves = []

        if len(self.current_batch_rewards) >= self.batch_size:
            self.network.update(self.current_batch_board_states, self.current_batch_rewards)
            self.current_batch_board_states = []
            self.current_batch_rewards = []

    def setup(self, piece):
        super(CNNAgent, self).setup(piece)
        self.network.setup(piece)

    def teardown(self):
        #self.network.update(self.current_batch_board_states, self.current_batch_rewards)
        #self._log_statistics()
        self.network.teardown()

    def _log_statistics(self):
        normalized_rewards = list(map(lambda v: 1 if v == 1 else 0.5 if v == 0 else 0, self.current_game_rewards))
        self.network.log('{},{}'.format(self.op_player, round(np.mean(normalized_rewards), 2)))
        self.current_game_rewards = []

    def _build_board_state(self, board):
        return list(map(lambda row: list(map(lambda v: 1 if v == self.piece else 0 if v == 0 else -1, row)), board))
