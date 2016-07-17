# coding=utf-8
import pygame
from pygame.locals import *
from random import randint, choice
from gameobjects.vector2 import Vector2
from sys import exit
SCREEN_SIZE = (640, 480)

class Game(object):
	def __init__(self, screen):
		self.screen = screen
		self.entities = {}
		self.entity_id = 0		# last entity id assigned
		self.background = pygame.surface.Surface(SCREEN_SIZE).convert()
		self.background.fill((255, 255, 255))
		pygame.draw.line(self.background, (0, 0, 0), (0, 240), (640, 240), 2)

	def process(self, time_passed):
		time_passed_seconds = time_passed / 1000.0
		for entity in self.entities.itervalues():
			entity.process(time_passed_seconds)

	def render(self):
		self.screen.blit(self.background, (0, 0))
		for entity in self.entities.itervalues():
			entity.render(self.screen)

	def add_entity(self, *entity):
		# 增加一个新的实体
		for en in entity:
			self.entities[self.entity_id] = en
			en.id = self.entity_id
			self.entity_id += 1

	def get(self, entity_id):
		# 通过id给出实体， 没有的话返回None
		if entity_id in self.entities:
			return self.entities[entity_id]
		else:
			return None

class GameEntity(object):
	def __init__(self, name, word, image, speed, location):
		self.name = name
		self.word = word
		self.image = image
		self.location = location
		self.destination = location
		self.speed = speed

	def render(self, surface):
		x, y = self.location
		w, h = self.image.get_size()
		surface.blit(self.image, (x-w/2, y-h/2))

	def process(self, time_passed):
		if self.speed > 0 and self.location != self.destination:
			vec_to_destination = self.destination - self.location
			distance_to_destination = vec_to_destination.get_length()
			heading = vec_to_destination.get_normalised()
			travel_distance = min(distance_to_destination, time_passed*self.speed)
			self.location += travel_distance * heading


class Bat(GameEntity):

	def left(self):
		self.destination = self.location+Vector2(-10, 0)

	def right(self):
		self.destination = self.location+Vector2(10, 0)

	def process(self, time_passed):
		if self.destination.get_x() > SCREEN_SIZE[0]:
			self.destination.set_x(SCREEN_SIZE[0])
		elif self.destination.get_x() < 0:
			self.destination.set_x(0)
		GameEntity.process(self, time_passed)


class Ball(GameEntity):
	def __init__(self, name, word, image, speed, location, direction):
		GameEntity.__init__(self, name, word, image, speed, location)
		self.direction = direction

	def process(self, time_passed):
		self.location += time_passed * self.speed * self.direction
		if self.location.get_x() > SCREEN_SIZE[0] or self.location.get_x() < 0:
			self.direction = Vector2(-self.direction.get_x(), self.direction.get_y())
		elif self.location.get_y() > SCREEN_SIZE[1] or self.location.get_y() < 0:
			self.direction = Vector2(0, 0)
			self.location = Vector2(320, 240)
			exit()
			# font = pygame.font.SysFont("ubuntu", 40)
			# text_surface = font.render(u"GameOver", True, (0, 0, 255))
			# self.word.screen.blit(text_surface, (100, 100))
			# print(self.word.screen)
		if (abs(self.location.get_y()- 350))<2 and self.word.get(0).location.get_x()-30 < self.location.get_x() < self.word.get(0).location.get_x()+30:
			self.direction = Vector2(self.direction.get_x(), -self.direction.get_y())
			self.speed += 10
		if (abs(self.location.get_y()- 50))<2 and self.word.get(1).location.get_x()-30 < self.location.get_x() < self.word.get(1).location.get_x()+30:
			self.direction = Vector2(self.direction.get_x(), -self.direction.get_y())
			self.speed += 10


def run():
	pygame.init()
	screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

	game = Game(screen)

	clock = pygame.time.Clock()
	bat_image = pygame.image.load("ant.png").convert_alpha()
	ball_image = pygame.image.load("ball.png").convert_alpha()

	bat = Bat("p1", game, bat_image, 300, Vector2(320, 350))
	bat2 = Bat("p2", game, bat_image, 300, Vector2(320, 50))
	direction = Vector2(1, 1).get_normalised()
	ball = Ball("ball", game,  ball_image, 100, Vector2(300, 200), direction)
	game.add_entity(bat, bat2, ball)

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				return
		time_passed = clock.tick(30)
		pressed_keys = pygame.key.get_pressed()
		if pressed_keys[K_LEFT]:
			bat.left()
		elif pressed_keys[K_RIGHT]:
			bat.right()
		if pressed_keys[K_a]:
			bat2.left()
		elif pressed_keys[K_d]:
			bat2.right()

		game.process(time_passed)
		game.render()

		pygame.display.update()

if __name__ == "__main__":
	run()

