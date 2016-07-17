# coding=utf8
import pygame
import sys
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Hello World!')
while True:		# 游戏循环
	for event in pygame.event.get():
		if event.type == QUIT:
			sys.exit()
	pygame.display.update()