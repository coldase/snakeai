import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
pygame.font.init()

myfont = pygame.font.SysFont('comicsans', 30)

class Direction(Enum):
	RIGHT = 1
	LEFT = 2
	UP = 3
	DOWN = 4

Point = namedtuple('Point', 'x, y')

BLOCK_SIZE = 20


BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)
BLUE1 = (0,0,255)
BLUE2 = (0,100,255)

class SnakeGame:

	def __init__(self, screen_width, screen_height):
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.speed = 10
		
		#init screen
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
		pygame.display.set_caption("Snake 1.0")
		
		self.clock = pygame.time.Clock()
		
		#init game state
		self.direction = Direction.RIGHT
		self.head = Point(self.screen_width / 2, self.screen_height / 2)
		self.snake = [self.head, Point(self.head.x - BLOCK_SIZE, self.head.y), Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

		self.score = 0
		self.food = None
		self._place_food()

	def _place_food(self):
		x = random.randint(0, (self.screen_width - BLOCK_SIZE ) //BLOCK_SIZE ) * BLOCK_SIZE
		y = random.randint(0, (self.screen_height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
		self.food = Point(x, y)
		if self.food in self.snake:
			self._place_food()

	def play_step(self):
		
		#increase speed
		if self.score >= 5 and self.score <= 10:
			self.speed = 15
		if self.score > 10 and self.score <= 20:
			self.speed = 20

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
					self.direction = Direction.LEFT
				if event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
					self.direction = Direction.RIGHT
				if event.key == pygame.K_UP and self.direction != Direction.DOWN:
					self.direction = Direction.UP
				if event.key == pygame.K_DOWN and self.direction != Direction.UP:
					self.direction = Direction.DOWN


		# Movement
		self._move(self.direction)
		self.snake.insert(0, self.head)

		# check if game over
		game_over = False
		if self._is_collision():
			game_over = True
			return game_over, self.score

		if self.head == self.food:
			self.score += 1
			self._place_food()

		else:
			self.snake.pop()

		self._update_ui()
		self.clock.tick(self.speed)
		return game_over, self.score

	def _is_collision(self):
    # hits boundary
		if self.head.x > self.screen_width - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.screen_height - BLOCK_SIZE or self.head.y < 0:
			return True
    # hits itself
		elif self.head in self.snake[1:]:
			return True
		return False

	def _update_ui(self):
		self.screen.fill(BLACK)

		for pt in self.snake:
			pygame.draw.rect(self.screen, BLUE1, (pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
			pygame.draw.rect(self.screen, BLUE2, (pt.x + 4, pt.y + 4, 12, 12))

		pygame.draw.rect(self.screen, RED, (self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

		text = myfont.render("Score: " + str(self.score), True, WHITE)
		self.screen.blit(text, [10,10])

		pygame.display.flip()

	def _move(self, direction):
		x = self.head.x
		y = self.head.y

		if direction == Direction.RIGHT:
			x += BLOCK_SIZE
		elif direction == Direction.LEFT:
			x -= BLOCK_SIZE
		elif direction == Direction.UP:
			y -= BLOCK_SIZE
		elif direction == Direction.DOWN:
			y += BLOCK_SIZE

		self.head = Point(x, y)

if __name__ == "__main__":
	game = SnakeGame(640, 480)

	#game loop
	while True:
		game_over, score = game.play_step()
		
		if game_over == True:
			break

	print("Final Score: ", score)
	pygame.quit()