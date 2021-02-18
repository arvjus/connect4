#!/usr/bin/env python3

import numpy as np
from gui import Gui, RED, YELLOW, WHITE
from config import Config
from base import Connect4Base
from random_agent import RandomAgent
from simple_agent import SimpleAgent
from one_step_lookahead_agent import OneStepLookaheadAgent
from n_steps_lookahead_agent import NStepsLookaheadAgent
from cnn_agent import CNNAgent
from network_128x4_64_64 import Network1

class Connect4(Connect4Base):
	def __init__(self, config, agent):
		super().__init__(config)
		self.agent = agent
		self.agent.setup(2)
		self.gui = Gui(config)

	def draw_board_check_if_winning(self, board, piece):
		self.gui.draw_board(board)
		if self.check_if_winning(board, piece):
			self.gui.display(10, 10, RED if piece == 1 else YELLOW, "Player {} wins".format(piece), True)
			return True
		return False

	def run(self):
		while True:
			board = np.full((config.rows, config.columns), 0, np.int)
			self.gui.draw_board(board)
			while True:
				# human
				col = self.gui.drop_piece(RED)
				board = self.drop_piece(board, col, 1)
				if self.draw_board_check_if_winning(board, 1):
					self.agent.game_over(1)
					break

				# agent
				if len(self.valid_moves(board)) == 0:
					self.gui.display(10, 10, WHITE, "Draw", False)
					self.agent.game_over(0)
					break
				col = self.agent.move(board)
				board = self.drop_piece(board, col, 2)
				if self.draw_board_check_if_winning(board, 2):
					self.agent.game_over(2)
					break
			if self.gui.wait_for_event(10000) == False:
				break

	def end(self):
		self.agent.teardown()

# run agents
config = Config(6, 7, 4)
#game = Connect4(config, NStepsLookaheadAgent(config, 3))
game = Connect4(config, CNNAgent(config, Network1(), 'human'))
#game = Connect4(config, OneStepLookaheadAgent(config))
game.run()
#game.end()
