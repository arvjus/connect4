#!/usr/bin/env python3

import sys
import numpy as np
from config import Config
from base import Connect4Base
from random_agent import RandomAgent
from simple_agent import SimpleAgent
from one_step_lookahead_agent import OneStepLookaheadAgent
from n_steps_lookahead_agent import NStepsLookaheadAgent
from cnn_agent import CNNAgent
from network_128x4_64_64 import Network1

class Tournament(Connect4Base):
	def __init__(self, config, agent1, agent2):
		super().__init__(config)
		self.agent1 = agent1
		self.agent2 = agent2
		self.agent1.setup(1)
		self.agent2.setup(2)
		print("Player 1 - {}".format(agent1.name()))
		print("Player 2 - {}".format(agent2.name()))

	def run(self):
		board = np.full((self.config.rows, self.config.columns), 0, np.int)
		piece = 1 # starts first
		winner = 0
		while len(self.valid_moves(board)) > 0:
			agent = self.agent1 if piece == 1 else self.agent2
			col = agent.move(board)
			board = self.drop_piece(board, col, piece)
			if self.check_if_winning(board, piece):
				winner = piece
				break
			piece = piece%2+1
		self.agent1.game_over(winner)
		self.agent2.game_over(winner)
		return winner

	def end(self):
		self.agent1.teardown()
		self.agent2.teardown()

# run agents
nruns = 100 if len(sys.argv) < 2 else int(sys.argv[1])
print("Number of runs", nruns)
winners = list()
config = Config(6, 7, 4)
#tournament = Tournament(config, RandomAgent(config), SimpleAgent(config))
#tournament = Tournament(config, SimpleAgent(config), NStepsLookaheadAgent(config, 1))
#tournament = Tournament(config, RandomAgent(config), CNNAgent(config, Network1(), 'rnd'))
#tournament = Tournament(config, OneStepLookaheadAgent(config), CNNAgent(config, Network1(), '1sla'))
tournament = Tournament(config, NStepsLookaheadAgent(config, 3), CNNAgent(config, Network1(), '3sla'))
#tournament = Tournament(config, CNNAgent(config, Network1(), 'cnn'), CNNAgent(config, Network1(), 'cnn'))
for n in range(nruns):
	winner = tournament.run()
	winners.append(winner)
	print("Game", n, ", player", winner, "wins")
tournament.end()

draw = len([n for n in winners if n == 0])
won_1 = len([n for n in winners if n == 1])
won_2 = len([n for n in winners if n == 2])
print("player1:", won_1, ", player2:", won_2, ", draw:", draw)
