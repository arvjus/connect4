
import pygame
import sys, math
from base import Connect4Base

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)

class Gui(Connect4Base):
	def __init__(self, config):
		super().__init__(config)
		pygame.init()
		pygame.display.set_caption('Connect four')
		self.config = config
		self.screen = pygame.display.set_mode((config.columns * SQUARESIZE, (config.rows + 1) * SQUARESIZE))
		self.myfont = pygame.font.SysFont("monospace", 25)

	def draw_board(self, board):
		pygame.draw.rect(self.screen, BLUE, (0, SQUARESIZE, self.config.columns * SQUARESIZE, self.config.rows * SQUARESIZE))
		for r in range(self.config.rows):
			for c in range(self.config.columns):
				pygame.draw.circle(self.screen, RED if board[r][c] == 1 else YELLOW if board[r][c] == 2 else BLACK,
								   (int(c * SQUARESIZE + SQUARESIZE / 2), SQUARESIZE + int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
		pygame.display.update()

	def display(self, x, y, colour, text, clear):
		if clear:
			pygame.draw.rect(self.screen, BLACK, (0, 0, self.config.columns * SQUARESIZE, SQUARESIZE))
		label = self.myfont.render(text, 1, colour)
		self.screen.blit(label, (x, y))
		pygame.display.update()

	def wait_for_event(self, millis):
		for n in range(int(millis / 100)):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					return True
				elif event.type == pygame.KEYDOWN:
					return event.key != pygame.K_q
			pygame.time.wait(100)

	def drop_piece(self, colour):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(self.screen, BLACK, (0, 0, self.config.columns * SQUARESIZE, SQUARESIZE))
					posx = event.pos[0]
					pygame.draw.circle(self.screen, colour, (posx, int(SQUARESIZE/2)), RADIUS)
					pygame.display.update()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					pygame.draw.rect(self.screen, BLACK, (0, 0, self.config.columns * SQUARESIZE, SQUARESIZE))
					pygame.time.wait(100)
					return int(math.floor(event.pos[0]/SQUARESIZE))
			pygame.time.wait(50)
