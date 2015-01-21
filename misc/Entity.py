from misc.Constants import *
from event.EventHandler import *
from event.Events import *
import random
import pygame
import copy

# robot and treasure could inherit this and both contain an update method?
#class Entity

class Robot(pygame.sprite.Sprite):

	def __init__(self, parent, x=150, y=150):
		self.image = pygame.image.load("assets/img/plane.png")
		self.image_static = self.image.copy()
		self.rect = self.image.get_rect().copy()
		self.rect.x = 50
		self.rect.y = 50

		self.x = self.rect.x
		self.y = self.rect.y

		self.bearing = 135
		self.velocity = 10

		self.parent = parent

		self.previous_rect = self.rect.copy()

		# ai shit
		self.min_moves, self.max_moves = 10, 30
		self.angle_movement = 1
		#self.current_moves = random.randint(self.min_moves, self.max_moves)
		self.timer = 0

		self.collisioncount = 0

	def update(self, time, events, entities):

		self.previous_rect = self.rect.copy()
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.rect.collidepoint(event.pos):
					print("robot clicked")

		self.timer += time

		if self.timer > 2:
			self.set_bearing(self.bearing + self.angle_movement)
			if self.timer > random.uniform(3.0, 4.0):
				self.timer = 2
				self.angle_movement *= -1

		bearing = bearing_conversion(self.bearing, self.velocity * time)
		self.x += bearing[2]
		self.y += bearing[3]

		self.rect.x = self.x
		self.rect.y = self.y

		'''
		entities1 = copy.copy(entities)
		entities1.pop(entities.index(self))

		collision = pygame.sprite.spritecollide(self, entities1, False)
		if len(collision) > 0:
			#self.set_bearing(self.bearing + random.randint(45, 90))
			collision[0].set_bearing(self.bearing + 180)
			#self.set_bearing(self.bearing)
		else:
			self.collisioncount = 0
		'''

		self.image = pygame.transform.rotate(self.image_static, abs(360 - self.bearing))
		self.rect = self.image.get_rect(center=self.rect.center)

		update = False
		if self.rect.right > self.parent.rect.width: self.rect.right = self.parent.rect.width; self.x = self.parent.rect.width - self.rect.width; update = True
		if self.rect.left < 0: self.rect.left = 0; self.x = 0; update = True
		if self.rect.top < 0: self.rect.top = 0; self.y = 0; update = True
		if self.rect.bottom > self.parent.rect.height: self.rect.bottom = self.parent.rect.height; self.y = self.parent.rect.height - self.rect.height; update = True

		if update:
			#print("upadting")
			self.set_bearing(self.bearing + 45)

		self.parent.blit(self.image, self.rect)

	def set_bearing(self, value):
		if value > 360: value -= 360
		if value < 0: value += 360
		self.bearing = value


class Landmark(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)