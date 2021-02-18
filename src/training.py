#!/usr/bin/env python3

import numpy as np
from config import Config
from base import Connect4Base
from random_agent import RandomAgent
from simple_agent import SimpleAgent
from one_step_lookahead_agent import OneStepLookaheadAgent
from n_steps_lookahead_agent import NStepsLookaheadAgent
from cnn_agent import CNNAgent
from network_128x4_64_64 import Network1

class Training(Connect4Base):
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
config = Config(6, 7, 4)
agents = [
	(RandomAgent(config), "rnd", 5000),
	(SimpleAgent(config), "simple", 5000),
	(OneStepLookaheadAgent(config), "1sla", 5000),
	(OneStepLookaheadAgent(config), "1sla", 5000),
	(OneStepLookaheadAgent(config), "1sla", 5000),
	(NStepsLookaheadAgent(config, 2), "2sla", 3000),
	(NStepsLookaheadAgent(config, 3), "3sla", 5000)
]
for agent, agent_name, nruns in agents:
	training = Training(config, agent, CNNAgent(config, Network1(), agent_name))
	for n in range(nruns):
		winner = training.run()
		print("Agent", agent_name, ", game", n, "- player", winner, "wins")
	training.end()

