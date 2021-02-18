#!/usr/bin/env python3

from network_128x4_64_64 import Network1
import numpy as np

def drop_piece(board, col, piece):
	next_board = board.copy()
	for row in range(5, -1, -1):
		if next_board[row][col] == 0:
			break
	next_board[row][col] = piece
	return next_board

def _build_board_state(piece, board):
	return list(map(lambda row: list(map(lambda v: 1 if v == piece else 0 if v == 0 else -1, row)), board))

current_batch_board_states = []
current_batch_rewards = []

# winning
moves_win = [
	(1,
	 np.array([[0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0]], np.int)),

	(2,
	 np.array([[0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 1, 0, 0, 0, 0, 2]], np.int)),

	(3,
	 np.array([[0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 1, 1, 0, 2, 0, 2]], np.int)),

	(0,
	 np.array([[0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 2, 0, 0, 0],
			   [0, 1, 1, 1, 2, 0, 2]], np.int))]

reward = 1
for move, board in reversed(moves_win):
	next_board = drop_piece(board, move, 1)
	board_state = _build_board_state(1, next_board)
	current_batch_board_states.append(board_state)
	current_batch_rewards.append(reward)
	reward *= 0.7

# loosing
moves_lose = [
	(6,
	 np.array([[0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 1, 0, 0, 0, 0, 0]], np.int)),

	(4,
	 np.array([[0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 1, 1, 0, 0, 0, 2]], np.int)),

	(3,
	 np.array([[0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0],
			   [0, 1, 1, 1, 2, 0, 2]], np.int))]

reward = -1
for move, board in reversed(moves_lose):
	next_board = drop_piece(board, move, 2)
	board_state = _build_board_state(2, next_board)
	current_batch_board_states.append(board_state)
	current_batch_rewards.append(reward)
	reward *= 0.7

network = Network1()
network.update(current_batch_board_states, current_batch_rewards)

# test predictions
for move, board in moves_win:
	print("win=", move)
	scores = []
	for col in range(7):
		next_board = drop_piece(board, col, 1)
		board_state = _build_board_state(1, next_board)
		score = network.predict(board_state)
		scores.append(round(score[0][0], 3))
	print("predicted=", scores.index(max(scores)), "scores=", scores )
	print("")

for move, board in moves_lose:
	print("lose=", move)
	scores = []
	for col in range(7):
		next_board = drop_piece(board, col, 2)
		board_state = _build_board_state(2, next_board)
		score = network.predict(board_state)
		scores.append(round(score[0][0], 3))
	print("predicted=", scores.index(max(scores)), "scores=", scores )
	print("")
