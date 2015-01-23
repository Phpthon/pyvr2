from misc.Constants import *
from event.EventHandler import *
from event.Events import *
import random
import pygame
import copy

# robot and treasure could inherit this and both contain an update method?
#class Entity

class Landmark(object):
	def __init__(self, **landmark):
		self.name = landmark["name"]
		self.rect = pygame.Rect(landmark["coords"][0], landmark["coords"][1], landmark["dimensions"][0], landmark["dimensions"][1])

class Treasure(pygame.sprite.Sprite):
	def __init__(self, parent):
		pygame.sprite.Sprite.__init__(self)
		# treasure needs to collide with any of the
		self.init = False
		self.parent = parent
		# put the treasure at a random position on the map
		self.x = random.randint(50, self.parent.rect.width - 100)
		self.y = random.randint(50, self.parent.rect.height - 100)
		self.rect = pygame.Rect(self.x, self.y, 32, 32)
		self.image = pygame.image.load(json_settings["treasure_img"])

		self.score = 100

	def update(self, timer, events):

		if self.parent.display_treasures:

			if not self.init:
				self.init = True
				#self.blit(self.parent.initial_image.subsurface(self.rect), (0,0))
				#self.blit(self.sprite, (10, 10))
				#self.parent.mapimg.blit(self.image, self.rect)
			#self.image.set_alpha(math.ceil(self.current))
			self.parent.blit(self.image, self.rect)

class Robot(pygame.sprite.Sprite):

	def __init__(self, parent, x=150, y=150):
		self.type = "ai"

		self.image = pygame.image.load("assets/img/plane.png")
		self.image_static = self.image.copy()
		self.rect = self.image.get_rect().copy()
		self.rect.x = 50
		self.rect.y = 50

		self.x = self.rect.x
		self.y = self.rect.y

		self.bearing = 135
		self.velocity = 200

		self.parent = parent

		self.previous_rect = self.rect.copy()

		# ai shit
		self.min_moves, self.max_moves = 10, 30
		self.angle_movement = 1
		#self.current_moves = random.randint(self.min_moves, self.max_moves)
		self.timer = 0

		self.collisioncount = 0
		self.score = 0

	def update(self, time, events):

		self.previous_rect = self.rect.copy()
		'''
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.rect.collidepoint(event.pos):
					print("robot clicked")
		'''

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

		# draw the path behind the entity?
		#pygame.draw.line(self.parent.mapimg, (151,174,200), (self.x + self.rect.width/2, self.y + self.rect.height/2), (self.x + self.rect.width/2, self.y - 1 + self.rect.height/2))
		#pygame.draw.circle(self.parent.mapimg, (151,174,200), (self.rect.center[0], self.rect.center[1]), 1)

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