#!/usr/bin/env python3

import numpy as np
from gui import Gui, RED, YELLOW, WHITE
from config import Config
from base import Connect4Base
from random_agent import RandomAgent
from simple_agent import SimpleAgent
from one_step_lookahead_agent import OneStepLookaheadAgent
from cnn_agent import CNNAgent
from network_128x4_64_64 import Network1

class Connect4(Connect4Base):
	def __init__(self, config, agent1, agent2):
		super().__init__(config)
		self.agent1 = agent1
		self.agent2 = agent2
		self.agent1.setup(1)
		self.agent2.setup(2)
		self.gui = Gui(config)

	# player 1 - red, player 2 - yellow
	def run(self, step_wait):
		while True:
			board = np.full((config.rows, config.columns), 0, np.int)
			self.gui.draw_board(board)
			self.gui.display(10, 10, RED, "Player 1 - {}".format(self.agent1.name()), True)
			self.gui.display(10, 50, YELLOW, "Player 2 - {}".format(self.agent2.name()), False)
			piece = 1 # starts first
			while True:
				if len(self.valid_moves(board)) == 0:
					self.gui.display(10, 10, WHITE, "Draw", False)
					break
				agent = self.agent1 if piece == 1 else self.agent2
				col = agent.move(board)
				board = self.drop_piece(board, col, piece)
				self.gui.draw_board(board)
				if self.check_if_winning(board, piece):
					self.gui.display(10, 10, RED if piece == 1 else YELLOW, "Player {} wins".format(piece), True)
					break
				piece = piece%2+1
				self.gui.wait_for_event(step_wait)
			self.gui.wait_for_event(10000)

	def end(self):
		self.agent1.teardown()
		self.agent2.teardown()

# run agents
config = Config(6, 7, 4)
#game = Connect4(config, SimpleAgent(config), OneStepLookaheadAgent(config))
game = Connect4(config, OneStepLookaheadAgent(config), CNNAgent(config, Network1(), '1sla'))
game.run(100)
game.end()
